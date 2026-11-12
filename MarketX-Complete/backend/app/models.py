from sqlalchemy import String, Integer, Float, Boolean, ForeignKey, DateTime, Text, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base
class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    name: Mapped[str]=mapped_column(String(100))
    email: Mapped[str]=mapped_column(String(255), unique=True, index=True)
    phone: Mapped[str]=mapped_column(String(30), default="")
    password_hash: Mapped[str]=mapped_column(String(255))
    created_at: Mapped[object]=mapped_column(DateTime(timezone=True), server_default=func.now())
    listings=relationship("Listing", back_populates="seller")
class Listing(Base):
    __tablename__="listings"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    title: Mapped[str]=mapped_column(String(140), index=True)
    description: Mapped[str]=mapped_column(Text)
    price: Mapped[float]=mapped_column(Float)
    category: Mapped[str]=mapped_column(String(60), index=True)
    condition: Mapped[str]=mapped_column(String(30), default="Used")
    city: Mapped[str]=mapped_column(String(80), index=True)
    state: Mapped[str]=mapped_column(String(80), default="Telangana")
    image_url: Mapped[str]=mapped_column(String(500), default="")
    seller_id: Mapped[int]=mapped_column(ForeignKey("users.id"))
    is_active: Mapped[bool]=mapped_column(Boolean, default=True)
    created_at: Mapped[object]=mapped_column(DateTime(timezone=True), server_default=func.now())
    seller=relationship("User", back_populates="listings")
class Favorite(Base):
    __tablename__="favorites"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id"))
    listing_id: Mapped[int]=mapped_column(ForeignKey("listings.id"))
    __table_args__=(UniqueConstraint("user_id","listing_id"),)
