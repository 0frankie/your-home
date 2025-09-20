import os
from app import DB_PATH, app
from globals import db, hash_password
from models import *

def initialize_data():
    # Add initial data if needed
    password = "adminpass"
    hashed_pw = hash_password(password)

    user1 = User(username="admin", email="admin@adminmail.com", hashed_password=hashed_pw)

    db.session.add(user1)
    db.session.commit()

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