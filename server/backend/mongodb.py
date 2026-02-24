"""
MongoDB connection utility
"""
from pymongo import MongoClient
import os

# MongoDB connection
_client = None
_db = None

def get_mongodb_client():
    """Get MongoDB client connection"""
    global _client
    if _client is None:
        # Try to get from environment or Django settings
        mongodb_uri = os.getenv('MONGODB_URI')
        if not mongodb_uri:
            try:
                from django.conf import settings
                mongodb_uri = getattr(settings, 'MONGODB_URI', None)
            except:
                pass
        
        # Default MongoDB URI
        if not mongodb_uri:
            mongodb_uri = 'mongodb+srv://thittanipreethi_db_user:preethi@2006@cluster0.oepojpf.mongodb.net/studymate_db?retryWrites=true&w=majority'
        
        # Configure SSL for MongoDB Atlas
        import ssl
        _client = MongoClient(
            mongodb_uri,
            tlsAllowInvalidCertificates=True,  # For development - disable in production
            serverSelectionTimeoutMS=5000
        )
    return _client

def get_mongodb_db():
    """Get MongoDB database"""
    global _db
    if _db is None:
        client = get_mongodb_client()
        # Extract database name from URI or use default
        db_name = 'studymate_db'
        _db = client[db_name]
    return _db

def get_collection(collection_name):
    """Get a MongoDB collection"""
    db = get_mongodb_db()
    return db[collection_name]

