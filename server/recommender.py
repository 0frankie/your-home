from globals import db
from models import Image

import numpy as np

def cosine_similarity(vec_a, vec_b):
    vec_a = np.asarray(vec_a, dtype=np.float32)
    vec_b = np.asarray(vec_b, dtype=np.float32)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))

class RoomRecommenderService:
    def __init__(self):
        pass


    def get_recommendations(self, user, top_k=5):

        if len(user.liked_images) == 0: # No preferences, so randomize images
            stmt = db.select(Image).order_by(db.func.random()).limit(top_k)
            images = db.session.execute(stmt).scalars().all()
            return [img.id for img in images]
        
        # compute average embedding of liked images
        
        # Placeholder recommendation logic
        return [f"room_{i}" for i in range(top_k)]