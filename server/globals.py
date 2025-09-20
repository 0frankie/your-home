from flask_sqlalchemy import SQLAlchemy
import hashlib

db = SQLAlchemy()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()