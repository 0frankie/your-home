# Your-Home Service

A Flask-based service for managing users, images, and generating personalized room recommendations.

## Project Structure

- `server/app.py`: Main Flask application.
- `server/bootstrap_db.py`: Script to initialize or reset the SQLite database.
- `server/models.py`: SQLAlchemy models for users, images, and relationships.
- `server/recommender.py`: Room recommender service using embeddings and KMeans clustering.
- `server/test.py`: Test script for ad-hoc testing of the recommender and API.
- `server/globals.py`: Global database and utility functions.
- `instance/`: Directory for the SQLite database (`app.db`).
- `images/`: Directory for storing image files.

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd your-home
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python3 -m venv venv
   source ./venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database**
   ```bash
   python server/bootstrap_db.py
   ```

5. **Run the Application**
   ```bash
   python server/app.py
   ```

   The app will be available at `http://localhost:5000`.

## API Endpoints

### Authentication
- **POST `/api/authenticate`**
  - Authenticate a user by username/password or device ID.
  - **Request Body**:
    ```json
    { "username": "testuser", "password": "password123" }
    ```
    or
    ```json
    { "device_id": "unique-device-id" }
    ```
  - **Response**: User object on success.

### Image Management
- **POST `/api/like-image`**
  - Like an image.
  - **Request Body**:
    ```json
    { "user_id": 1, "image_id": 5 }
    ```
  - **Response**: Success or error message.

- **GET `/api/get-image-likes/<image_id>`**
  - Get the like count for an image.
  - **Response**:
    ```json
    { "image_id": 5, "like_count": 10 }
    ```

- **GET `/api/get-image-metadata/<image_id>`**
  - Get metadata for an image, including users who liked it.
  - **Response**:
    ```json
    {
      "id": 5,
      "image_path": "images/room.jpg",
      "liked_by": ["user1", "user2"]
    }
    ```

- **GET `/api/get-image-file/<image_id>`**
  - Download the image file.
  - **Response**: Raw image bytes.

### Recommendations
- **GET `/api/get-user-recommendations/<user_id>`**
  - Get recommended image IDs for a user.
  - **Response**:
    ```json
    { "image_ids": [10, 12, 15] }
    ```

- **GET `/api/get-generated-preferences/<user_id>`**
  - Generate a personalized room image based on user preferences.
  - **Response**: Raw image bytes or error message.

## Notes
- Ensure the `instance/` directory exists before running the app. The database file (`app.db`) will be created there.
- Use `server/bootstrap_db.py` to reset the database if needed.
- The recommender service uses embeddings stored as float32 blobs in the database.

## Example Usage

### Authenticate a User
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "password123"}' \
http://localhost:5000/api/authenticate
```

### Like an Image
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"user_id": 1, "image_id": 5}' \
http://localhost:5000/api/like-image
```

### Get Recommendations
```bash
curl http://localhost:5000/api/get-user-recommendations/1
```



<!--ngrok http --url=electroluminescent-plagihedral-dane.ngrok-free.app 5000 -->
