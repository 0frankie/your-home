from flask import Flask, jsonify, request, send_file
import os
from globals import db, hash_password
from models import User, Image, user_likes
from sqlalchemy.exc import IntegrityError
from recommender import RoomRecommenderService
import base64

import io

# Create the Flask app
app = Flask(__name__, instance_relative_config=True)

DB_NAME = "app.db"
DB_PATH = os.path.join("./instance", DB_NAME)
IMAGES_DIR = "./images"
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
recommender_service = RoomRecommenderService()

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
    
    if device_id is not None and user:
        user.device_id = device_id
        db.session.commit()
    return jsonify(user.to_dict()), 200

@app.route("/api/get-image-likes/<image_id>", methods=["GET"])
def get_image_likes(image_id):
    stmt = db.select(db.func.count()).select_from(user_likes).where(user_likes.c.image_id == image_id)
    result = db.session.execute(stmt)
    count = result.scalar()
    return jsonify({"image_id": image_id, "like_count": count})

@app.route("/api/like-image", methods=["POST"])
def like_image():
    obj = request.get_json()
    user_id = obj.get("user_id")
    image_id = obj.get("image_id")

    user = db.session.get(User, int(user_id))
    image = db.session.get(Image, int(image_id))
    user.liked_images.append(image)
    try:
        db.session.commit()
        return jsonify({"message": "Image liked successfully"}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Image already liked"}), 400
    
@app.route("/api/get-image-metadata/<image_id>", methods=["GET"])
def get_image(image_id):
    image = db.session.get(Image, int(image_id))
    if image is None:
        return jsonify({"error": "Image not found"}), 404

    return jsonify({
        "id": image.id,
        "image_path": image.image_path,
        "liked_by": [user.username for user in image.liked_by]
    }), 200

@app.route("/api/get-image-file/<image_id>", methods=["GET"])
def get_image_file(image_id):
    image = db.session.get(Image, int(image_id))
    if image is None:
        return jsonify({"error": "Image not found"}), 404

    image_full_path = os.path.join(image.image_path)
    if not os.path.isfile(image_full_path):
        return jsonify({"error": "Image file not found"}), 404

    return send_file(image_full_path, mimetype='image/jpeg')

@app.route("/api/get-user-recommendations/<user_id>", methods=["GET"])
def get_user_recommendations(user_id):
    user = db.session.get(User, int(user_id))
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    recommendations = recommender_service.get_recommendations(user, top_k=10)
    return jsonify({"image_ids": recommendations}), 200


@app.route("/api/get-generated-preferences/<user_id>", methods=["GET"])
def get_generated_preferences(user_id):
    user = db.session.get(User, int(user_id))
    if user is None:
        return jsonify({"error": "User not found"}), 404

    if user.liked_images is None or len(user.liked_images) == 0:
        return jsonify({"error": "User has no liked images"}), 400
    
    response = recommender_service.get_generated_pref(user)
    if response.status_code != 200:
        return jsonify({"error": "Image generation failed", "details": response.text}), 500

    # Raw image bytes directly
    output_image = response.content  
    finish_reason = response.headers.get("finish-reason")
    seed = response.headers.get("seed")

    if finish_reason == "CONTENT_FILTERED":
        return jsonify({"error": "Image blocked by NSFW filter"}), 400

    # Return via Flask
    return send_file(
        io.BytesIO(output_image),
        mimetype=f"image/jpeg",
        as_attachment=False,
        download_name=f"room.jpeg"
    )


# Run the app
if __name__ == "__main__":

    app.run(debug=True, port=5000)
