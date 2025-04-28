from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id: Mapped[int] = mapped_column(primary_key=True)
    
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped["User"] = relationship(back_populates="favorites")

    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey('planet.id'), nullable=True)
    planet: Mapped[Optional["Planet"]] = relationship()

    person_id: Mapped[Optional[int]] = mapped_column(ForeignKey('person.id'), nullable=True)
    person: Mapped[Optional["Person"]] = relationship()

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "person_id": self.person_id
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    gravity: Mapped[str] = mapped_column(nullable=False)
    climate: Mapped[str] = mapped_column(nullable=False)
    terrain: Mapped[str] = mapped_column(nullable=False)
    diameter: Mapped[int] = mapped_column(nullable=False)
    
    favorites: Mapped[list["Favorite"]] = relationship()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gravity": self.gravity,
            "climate": self.climate,
            "terrain": self.terrain,
            "diameter": self.diameter
        }

class Person(db.Model):
    __tablename__ = 'person'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    height: Mapped[int] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    birthyear: Mapped[str] = mapped_column(nullable=False)
    eyecolor: Mapped[str] = mapped_column(nullable=False)

    favorites: Mapped[list["Favorite"]] = relationship()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "gender": self.gender,
            "birthyear": self.birthyear,
            "eyecolor": self.eyecolor
        }
