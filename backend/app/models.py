from sqlalchemy import Column, String, Integer, BigInteger, Text, ForeignKey, Enum, TIMESTAMP, func
from sqlalchemy.orm import relationship
from .db import Base
import enum

class OrderStatus(str, enum.Enum):
    NEW = "NEW"
    PAID = "PAID"
    CANCELLED = "CANCELLED"
    FULFILLED = "FULFILLED"

class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(191), unique=True, nullable=False)
    name = Column(String(191))
    password_hash = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

class Category(Base):
    __tablename__ = "categories"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(191), unique=True, nullable=False)

class Product(Base):
    __tablename__ = "products"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(191), nullable=False)
    description = Column(Text)
    price_cents = Column(Integer, nullable=False)
    image_url = Column(String(512))
    category_id = Column(BigInteger, ForeignKey("categories.id"))
    category = relationship("Category")

class Order(Base):
    __tablename__ = "orders"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_code = Column(String(24), unique=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    user = relationship("User")
    guest_email = Column(String(191))
    guest_name = Column(String(191))
    total_cents = Column(Integer, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.NEW, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_id = Column(BigInteger, ForeignKey("orders.id"), nullable=False)
    product_id = Column(BigInteger, ForeignKey("products.id"), nullable=False)
    qty = Column(Integer, nullable=False)
    price_cents = Column(Integer, nullable=False)
    order = relationship("Order", back_populates="items")
    product = relationship("Product")
