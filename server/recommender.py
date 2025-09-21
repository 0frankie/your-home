from globals import db
from models import Image
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity as sk_cosine

import numpy as np

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
    
    def kmeans_weighted_avg(vectors: list[np.ndarray]) -> np.ndarray:
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
        pass
