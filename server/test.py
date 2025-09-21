from app import app
from globals import db
from models import User, Image
from recommender import RoomRecommenderService

recommender = RoomRecommenderService()

def test1():
    with app.app_context():
        # grab testuser
        user = User.query.filter_by(username="testuser").first()
        print("Testuser liked:", [img.id for img in user.liked_images])

        # grab embeddings for liked images
        liked_vecs = [recommender.blob_to_vec(img.embedding) for img in user.liked_images]

        # compare with all other images in DB
        candidates = Image.query.all()
        scored = []
        for img in candidates:
            vec = recommender.blob_to_vec(img.embedding)
            # score = max similarity to any liked image
            score = max(recommender.cosine_similarity(vec, lv) for lv in liked_vecs)
            scored.append((img.id, score))

        # sort by score, drop already liked
        recs = sorted(scored, key=lambda x: x[1], reverse=True)
        recs = [iid for iid, _ in recs if iid not in [i.id for i in user.liked_images]]

        print("Top recommendations:", recs[:10])

def test2():
    with app.app_context():
        # grab testuser
        user = User.query.filter_by(username="testuser").first()
        print("Testuser liked:", [img.id for img in user.liked_images])
        recommender.get_generated_pref(user)
test2() 