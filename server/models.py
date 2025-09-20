from globals import db
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, JSON, ForeignKey, Integer, LargeBinary
# Define models

#many to many
user_likes = db.Table(
    'user_to_image',
    db.Model.metadata,
    db.Column('username', String, ForeignKey('users.username'), primary_key=True),
    db.Column('image_id', Integer, ForeignKey('images.id'), primary_key=True)
)

class Image(db.Model):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    image_path: Mapped[str] = mapped_column(String, nullable=False)
    embedding: Mapped[list[bytes]] = mapped_column(LargeBinary, nullable=False)

    liked_by: Mapped[list["User"]] = relationship(
        back_populates="liked_images",
        secondary=user_likes
    )

    def __repr__(self):
        return f"<Image {self.id} by User >"

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    device_id: Mapped[str] = mapped_column(String, unique=True, nullable=True)

    liked_images: Mapped[list["Image"]] = relationship(
        back_populates="liked_by",
        secondary=user_likes
    )

    def __repr__(self):
        return f"<User {self.username}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "device_id": self.device_id
        }
