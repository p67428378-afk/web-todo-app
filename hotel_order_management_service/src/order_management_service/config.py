# Module: config.py
# Purpose: Configuration settings for the Hotel Order Management Service.
# Author: Architect Agent
# Created: 2024-03-02
# Notes: Loads environment variables for sensitive information.

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    """
    Configuration class for the Flask application and database connections.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'a_very_secret_key')
    
    # PostgreSQL Database for Order Data
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://user:password@localhost:5432/order_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MongoDB Database for Inventory Data
    MONGO_URI = os.getenv(
        'MONGO_URI',
        'mongodb://localhost:27017/inventory_db'
    )
