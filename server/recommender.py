from globals import db, STABILITY_KEY
from models import Image, CandidateText
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity as sk_cosine

import numpy as np

import requests

def send_generation_request(
    host,
    params,
    files = None
):
    headers = {
        "Accept": "image/*",
        "Authorization": f"Bearer {STABILITY_KEY}"
    }

    if files is None:
        files = {}

    # Encode parameters
    image = params.pop("image", None)
    mask = params.pop("mask", None)
    if image is not None and image != '':
        files["image"] = open(image, 'rb')
    if mask is not None and mask != '':
        files["mask"] = open(mask, 'rb')
    if len(files)==0:
        files["none"] = ''

    # Send request
    print(f"Sending REST request to {host}...")
    response = requests.post(
        host,
        headers=headers,
        files=files,
        data=params
    )
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    return response

class RoomRecommenderService:
    def __init__(self):
        pass

    @staticmethod
    def cosine_similarity(vec_a, vec_b):
        vec_a = np.asarray(vec_a, dtype=np.float32)
        vec_b = np.asarray(vec_b, dtype=np.float32)
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))

    @staticmethod
    def blob_to_vec(blob):
        return np.frombuffer(blob, dtype=np.float32).copy()

    @staticmethod
    def choose_k(n_likes: int, k_max: int = 5) -> int:
        # heuristic: sqrt of likes, capped at 5, min 1
        return int(max(1, min(k_max, round(np.sqrt(n_likes)))))
    
    def most_similar_rows(self, user_pref, rows):
        best_row = rows[0]
        vec0 = self.blob_to_vec(best_row.embedding)
        best_score = self.cosine_similarity(user_pref, vec0)

        for row in rows:
            vec = self.blob_to_vec(row.embedding)
            score = self.cosine_similarity(user_pref, vec)
            if score > best_score:
                best_score = score
                best_row = row
        return best_row
    
    def kmeans_weighted_avg(self, vectors: list[np.ndarray]) -> np.ndarray:
        L = normalize(np.stack(vectors).astype(np.float32), norm="l2")

        n_likes = L.shape[0]
        k = min(RoomRecommenderService.choose_k(n_likes), n_likes)

        if k == 1:
            centroids = L.mean(axis=0, keepdims=True)
            counts = np.array([n_likes], dtype=int)
        else:
            km = KMeans(n_clusters=k, n_init="auto", random_state=123)
            labels = km.fit_predict(L)
            centroids = km.cluster_centers_
            counts = np.bincount(labels, minlength=k)

        w = counts.astype(np.float32)
        w = w / (w.sum() + 1e-12)
        user_pref = (w[:, None] * centroids).sum(axis=0, keepdims=True)

        user_pref = normalize(user_pref, norm="l2")[0]
        return user_pref

    def get_recommendations(self, user, top_k=10):

        if len(user.liked_images) == 0: # No preferences, so randomize images
            stmt = db.select(Image).order_by(db.func.random()).limit(top_k)
            images = db.session.execute(stmt).scalars().all()
            return [img.id for img in images]
        # compute average embedding of liked images
        liked_imgs = list(user.liked_images)
        liked_vecs = []
        for img in liked_imgs:
            liked_vecs.append(self.blob_to_vec(img.embedding))
        # Call kmeans_weighted_avg
        user_pref = self.kmeans_weighted_avg(liked_vecs).reshape(1, -1)
        # ------------------------
        liked_ids = {img.id for img in user.liked_images}
        rows = db.session.execute(db.select(Image.id, Image.embedding)).all()
        cand_ids, cand_vecs = [], []
        for img_id, blob in rows:
            if img_id in liked_ids:
                continue
            v = self.blob_to_vec(blob)
            if v is None or v.size == 0:
                continue
            cand_ids.append(img_id)
            cand_vecs.append(v)
        if not cand_vecs:
            stmt = db.select(Image).order_by(db.func.random()).limit(top_k)
            images = db.session.execute(stmt).scalars().all()
            return [img.id for img in images]
        C = normalize(np.stack(cand_vecs).astype(np.float32), norm="l2")
        sims = sk_cosine(user_pref, C)[0]
        top_idx = np.argsort(-sims)[:top_k]
        return [cand_ids[i] for i in top_idx]


    def get_generated_pref(self, user):
        liked_imgs = list(user.liked_images)
        liked_vecs = []
        for img in liked_imgs:
            liked_vecs.append(self.blob_to_vec(img.embedding))
        # Call kmeans_weighted_avg
        user_pref = self.kmeans_weighted_avg(liked_vecs).reshape(1, -1)

        stmt = db.select(CandidateText).where(CandidateText.category == "style")
        style_rows = db.session.execute(stmt).scalars().all()

        stmt = db.select(CandidateText).where(CandidateText.category == "color scheme")
        color_rows = db.session.execute(stmt).scalars().all()

        stmt = db.select(CandidateText).where(CandidateText.category == "layout")
        layout_rows = db.session.execute(stmt).scalars().all()

        stmt = db.select(CandidateText).where(CandidateText.category == "materials")
        material_rows = db.session.execute(stmt).scalars().all()

        stmt = db.select(CandidateText).where(CandidateText.category == "lighting")
        lighting_rows = db.session.execute(stmt).scalars().all()

        stmt = db.select(CandidateText).where(CandidateText.category == "decor")
        decor_rows = db.session.execute(stmt).scalars().all()

        best_style = self.most_similar_rows(user_pref, style_rows)
        best_color = self.most_similar_rows(user_pref, color_rows)
        best_layout = self.most_similar_rows(user_pref, layout_rows)
        best_material = self.most_similar_rows(user_pref, material_rows)
        best_lighting = self.most_similar_rows(user_pref, lighting_rows)
        best_decor = self.most_similar_rows(user_pref, decor_rows)

        # print(best_style.text, best_color.text, best_layout.text, best_material.text, best_lighting.text, best_decor.text)
        description = (
            f"This {best_style.text.lower()} bedroom features a {best_color.text.lower()} palette, "
            f"with a {best_layout.text.lower()} design. "
            f"Materials include {best_material.text.lower()}, "
            f"illuminated by {best_lighting.text.lower()}. "
            f"Decor is styled with {best_decor.text.lower()}."
        )
        aspect_ratio = "16:9" 
        seed = 0 #@param {type:"integer"}
        output_format = "jpeg" 
        
        host = f"https://api.stability.ai/v2beta/stable-image/generate/core"
        params = {
            "prompt" : description,
            "aspect_ratio" : aspect_ratio,
            "seed" : seed,
            "output_format": output_format
        }

        response = send_generation_request(
            host,
            params
        )
        return response







