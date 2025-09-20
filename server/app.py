from flask import Flask, jsonify, request
import os
from globals import db, hash_password
from models import User, user_likes


# Create the Flask app
app = Flask(__name__, instance_relative_config=True)

DB_NAME = "app.db"
DB_PATH = os.path.join("./instance", DB_NAME)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Define a route
@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/api")
def api():
    return "your home api"

@app.route("/api/authenticate", methods=["POST"])
def authenticate():
    data = request.get_json()

    device_id = data.get("device_id")
    if device_id is not None:
        stmt = db.select(User).where(User.device_id == device_id)
        result = db.session.execute(stmt)
        user = result.scalar_one_or_none()
        if user:
            return jsonify(user.to_dict())

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    # Query user with SQLAlchemy Core-style select
    stmt = db.select(User).where(User.username == username)
    result = db.session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        return jsonify({"error": "invalid credentials"}), 401

    hashed_pw = hash_password(password)
    if user.hashed_password != hashed_pw:
        return jsonify({"error": "invalid credentials"}), 401
    
    return jsonify(user.to_dict()), 200

@app.route("/api/get-image-likes/<image_id>", methods=["GET"])
def get_image_likes(image_id):
    stmt = db.select(user_likes).where(user_likes.c.image_id == image_id)
    result = db.session.execute(stmt)
    user = result.scalars().all()

    print(user[0])

    return "image likes"

# Run the app
if __name__ == "__main__":

    app.run(debug=True, port=5000)
