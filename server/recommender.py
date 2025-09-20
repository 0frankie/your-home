from globals import db
from models import Image



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