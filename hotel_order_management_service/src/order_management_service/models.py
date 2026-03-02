# Module: models.py
# Purpose: Defines database models for Order Management (PostgreSQL) and Inventory (MongoDB).
# Author: Architect Agent
# Created: 2024-03-02

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from .config import Config

db = SQLAlchemy()
mongo_client = None

def init_db(app):
    """
    Initializes the SQLAlchemy and PyMongo instances with the Flask app.

    Args:
        app (Flask): The Flask application instance.
    """
    db.init_app(app)
    global mongo_client
    mongo_client = MongoClient(app.config['MONGO_URI'])
    
    with app.app_context():
        db.create_all()

# PostgreSQL Models (Order Management)
class Order(db.Model):
    """
    Represents a room service order in the PostgreSQL database.

    Attributes:
        order_id (str): Unique identifier for the order.
        guest_id (str): Identifier for the guest who placed the order.
        delivery_instructions (str): Special instructions for delivery.
        status (str): Current status of the order (e.g., Pending, In Progress, Delivered, Cancelled).
        created_at (datetime): Timestamp when the order was created.
        updated_at (datetime): Timestamp when the order was last updated.
        items (relationship): One-to-many relationship with OrderItem.
    """
    __tablename__ = 'orders'
    order_id = db.Column(db.String(100), primary_key=True)
    guest_id = db.Column(db.String(100), nullable=False)
    delivery_instructions = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(50), default='Pending', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Order {self.order_id}>'

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'guest_id': self.guest_id,
            'delivery_instructions': self.delivery_instructions,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'items': [item.to_dict() for item in self.items]
        }

class OrderItem(db.Model):
    """
    Represents an item within a room service order in the PostgreSQL database.

    Attributes:
        id (int): Primary key for the order item.
        order_id (str): Foreign key referencing the parent Order.
        item_id (str): Identifier for the menu item.
        quantity (int): Quantity of the item in the order.
        price (float): Price of a single unit of the item at the time of order.
    """
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(100), db.ForeignKey('orders.order_id'), nullable=False)
    item_id = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<OrderItem {self.item_id} in Order {self.order_id}>'

    def to_dict(self):
        return {
            'item_id': self.item_id,
            'quantity': self.quantity,
            'price': self.price
        }

# MongoDB Collection (Inventory Management)
def get_inventory_collection():
    """
    Returns the MongoDB inventory collection.

    Returns:
        Collection: The MongoDB collection for inventory items.
    """
    if mongo_client:
        return mongo_client.inventory_db.items
    return None
