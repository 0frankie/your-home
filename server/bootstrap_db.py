import os
from app import DB_PATH, app
from globals import db, hash_password
from models import *
import numpy as np



def initialize_data():
    # Add initial data if needed
    password = "password"
    user1 = User(username="franklin", email="frank@lin.com", hashed_password=hash_password(password), device_id="device123")

    adminpw = "admin"
    admin = User(username="admin", email="admin@admin", hashed_password=hash_password(adminpw), device_id="admindevice")

    emb = np.array([0.1, 0.2, 0.3], dtype=np.float32)
    emb_bytes = emb.tobytes()
    image1 = Image(image_path="/path/to/image1.jpg", embedding=emb_bytes)
    image2 = Image(image_path="/path/to/image1.jpg", embedding=emb_bytes)
    image3 = Image(image_path="/path/to/image1.jpg", embedding=emb_bytes)
    image4 = Image(image_path="/path/to/image1.jpg", embedding=emb_bytes)

    liked_imgs = [image1, image2, image3, image4]
    user1.liked_images = liked_imgs

    db.session.add(admin)
    db.session.add(user1)
    db.session.commit()


    img = db.session.get(Image, 1)
    print(f"Image from DB: {img}, emb:{np.frombuffer(img.embedding, dtype=np.float32)}")


def main():
    # ensure instance directory exists
    instance_dir = os.path.dirname(DB_PATH)
    os.makedirs(instance_dir, exist_ok=True)

	# remove existing DB if present
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    with open(DB_PATH, 'w'):
        pass

	# create a new sqlite DB file (connect creates the file)
    with app.app_context():
        db.create_all()
        initialize_data()

    print(f"Created fresh database at {DB_PATH}")

if __name__ == "__main__":
	main()