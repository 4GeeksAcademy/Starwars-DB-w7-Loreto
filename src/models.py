from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey, Float, Table, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# --- Bridge tables ---
favorite_planets = Table(
    'favorite_planets',
    Base.metadata,
    Column('favorite_id', Integer, ForeignKey(
        'favorites.id'), primary_key=True, nullable=False),
    Column('planet_id',   Integer, ForeignKey(
        'planets.id'),   primary_key=True, nullable=False),
)

favorite_characters = Table(
    'favorite_characters',
    Base.metadata,
    Column('favorite_id',  Integer, ForeignKey(
        'favorites.id'),   primary_key=True, nullable=False),
    Column('character_id', Integer, ForeignKey(
        'characters.id'),  primary_key=True, nullable=False),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_name = Column(String(120), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(120), nullable=False)
    active = Column(Boolean, default=True)

    # relation 1*1
    favorites = relationship('Favorite', uselist=False, back_populates="user")


class Planet(Base):
    __tablename__ = "planets"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False, unique=True)
    population = Column(Integer, nullable=True)
    terrain = Column(String, nullable=True)
    rotation = Column(String, nullable=True)
    climate = Column(String, nullable=True)
    diameter = Column(Integer, nullable=True)

    # 1*N one planet in many favorite basket
    in_favorites = relationship(
        'Favorite', secondary=favorite_planets, back_populates='planets')


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False, unique=True)
    gender = Column(String, nullable=True)
    hair = Column(Text, nullable=True)
    eye_color = Column(String, nullable=True)
    skin_color = Column(String, nullable=True)
    day_of_birth = Column(String, nullable=True)
    height = Column(Integer, nullable=True)

    # 1*N one character in many favorite basket
    in_favorites = relationship(
        'Favorite', secondary=favorite_character, back_populates='characters')


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Enforce “one bucket per user”
    __table_args__ = (
        UniqueConstraint("user_id", name="uq_favorites_user_id"),
    )

    # 1*1
    user = relationship('User', back_populates="favorites")

    # *a* via bridge tables

    planets = relationship(
        "Planet", secondary=favorite_planets, back_populates='in_favorites')
    characters = relationship(
        "Character", secondary=favorite_characters, back_populates='in_favorites')
