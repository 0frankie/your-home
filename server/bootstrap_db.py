import os
from app import DB_PATH, IMAGES_DIR, app
from globals import db, hash_password
from models import *
import numpy as np
import csv
import ast
from sqlalchemy import select
import pandas as pd


DTYPE = np.float32

def load_embeddings(csv_path, img_dir=IMAGES_DIR):
    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():
        img_path = os.path.join(img_dir, row["filename"])

        embedding_list = [float(x) for x in row["embedding"].strip("[]").split(",")]
        embedding_array = np.array(embedding_list, dtype=np.float32)

        embedding_bytes = embedding_array.tobytes()
        image_obj = Image(
            image_path=img_path,
            embedding=embedding_bytes,
        )
        db.session.add(image_obj)
    db.session.commit()

def initialize_data():
    # Add initial data if needed
    password = "password"
    user1 = User(username="franklin", email="frank@lin.com", hashed_password=hash_password(password), device_id="device123")

    adminpw = "admin"
    admin = User(username="admin", email="admin@admin", hashed_password=hash_password(adminpw), device_id="admindevice")

    test_user_pw = "test"
    test_user = User(username="testuser", email="test@test", hashed_password=hash_password(test_user_pw), device_id="testdevice")
    img_ids = [21, 173, 186, 225, 241, 271, 298, 301, 318, 334, 362, 379, 392, 394, 466, 560, 568, 585, 620, 685, 693, 717, 733, 826, 859]
    for img_id in img_ids:
        img = db.session.get(Image, img_id)
        if img:
            test_user.liked_images.append(img)
                                
    db.session.add(admin)
    db.session.add(user1)
    db.session.add(test_user)
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


    os.makedirs(IMAGES_DIR, exist_ok=True)   
    with app.app_context():
        db.create_all()
        load_embeddings(
            "image_embeddings.csv",
            IMAGES_DIR
        )
        initialize_data()
    # Replace new_base with folder name

    print(f"Created fresh database at {DB_PATH}")

if __name__ == "__main__":
	main()