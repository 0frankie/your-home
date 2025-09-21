from flask_sqlalchemy import SQLAlchemy
import hashlib
from dotenv import load_dotenv
import os
db = SQLAlchemy()

load_dotenv()
STABILITY_KEY = os.getenv("STABILITY_KEY", "")
print(STABILITY_KEY)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()