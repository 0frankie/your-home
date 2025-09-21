import os
from app import DB_PATH, IMAGES_DIR, app
from globals import db, hash_password
from models import *
import numpy as np
import csv
import ast
from sqlalchemy import select


DTYPE = np.float32

def normalize_image_path(image_path: str, old_prefix: str, new_base: str) -> str:
    if image_path.startswith(old_prefix):
        rel_path = image_path[len(old_prefix):]
        return os.path.join(new_base, rel_path)
    return image_path

def parse_embedding_cells(row, emb_start=0, embedding_key=None):
    if embedding_key and embedding_key in row and row[embedding_key]:
        cell = row[embedding_key].strip()
        try:
            vec_list = ast.literal_eval(cell)
        except Exception:
            import json
            vec_list = json.loads(cell)
        return np.array(vec_list, dtype=DTYPE)
    cells = row[emb_start:] if isinstance(row, list) else list(row.values())[emb_start:]
    return np.array([float(x) for x in cells], dtype=DTYPE)

def _first_present(d, keys):
    for k in keys:
        if isinstance(d, dict) and k in d and d[k]:
            return d[k]
    return None

def load_embeddings(csv_path, old_prefix, new_base, emb_start=0, embedding_key='embedding', id_key=None, path_key='image_path'):
    with open(csv_path, newline='', encoding='utf-8') as f:
        sample = f.read(2048)
        f.seek(0)
        has_header = csv.Sniffer().has_header(sample)
        if has_header:
            reader = csv.DictReader(f)
            for row in reader:
                image_path = _first_present(row, [path_key, 'filepath', 'file_path', 'path', 'filename', 'file', 'image', 'url'])
                raw_id = row.get(id_key) if id_key else None
                vec = parse_embedding_cells(row, emb_start=emb_start, embedding_key=embedding_key)
                blob = vec.tobytes()
                if image_path:
                    if old_prefix and new_base:
                        image_path = normalize_image_path(image_path, old_prefix, new_base)
                    img = db.session.execute(select(Image).where(Image.image_path == image_path)).scalar_one_or_none()
                    if img is None:
                        img = Image(image_path=image_path, embedding=blob)
                        db.session.add(img)
                    else:
                        img.embedding = blob
                elif raw_id is not None and str(raw_id).isdigit():
                    iid = int(raw_id)
                    img = db.session.get(Image, iid)
                    if img is None:
                        img = Image(id=iid, embedding=blob)
                        db.session.add(img)
                    else:
                        img.embedding = blob
                else:
                    img = Image(embedding=blob)
                    db.session.add(img)
        else:
            reader = csv.reader(f)
            for row in reader:
                vec = parse_embedding_cells(row, emb_start=emb_start, embedding_key=None)
                blob = vec.tobytes()
                img = Image(embedding=blob)
                db.session.add(img)
        db.session.commit()

def read_embedding_from_db(image_id):
    img = db.session.execute(select(Image).where(Image.id == image_id)).scalar_one()
    return np.frombuffer(img.embedding, dtype=DTYPE)


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
            old_prefix="/content/drive/MyDrive/1000 images/",
            new_base=IMAGES_DIR
        )
        initialize_data()
    # Replace new_base with folder name

    print(f"Created fresh database at {DB_PATH}")

if __name__ == "__main__":
	main()