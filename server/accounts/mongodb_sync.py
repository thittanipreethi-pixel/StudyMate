"""
Utility to sync Django users to MongoDB
"""
import sys
import os
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from backend.mongodb import get_collection
from datetime import datetime

User = get_user_model()

def sync_users_to_mongodb():
    """Sync all existing Django users to MongoDB"""
    users_collection = get_collection('users')
    
    # Get all users from Django
    django_users = User.objects.all()
    
    synced_count = 0
    for user in django_users:
        # Check if user already exists in MongoDB
        existing = users_collection.find_one({
            '$or': [
                {'username': user.username},
                {'email': user.email},
                {'django_user_id': user.id}
            ]
        })
        
        if not existing:
            # Create user document in MongoDB
            user_doc = {
                'username': user.username,
                'email': user.email,
                'password': user.password,  # Already hashed in Django
                'role': getattr(user, 'role', 'student'),
                'first_name': user.first_name or '',
                'last_name': user.last_name or '',
                'created_at': user.date_joined if hasattr(user, 'date_joined') else datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                'django_user_id': user.id
            }
            users_collection.insert_one(user_doc)
            synced_count += 1
            print(f"Synced user: {user.username}")
        else:
            # Update existing MongoDB user
            users_collection.update_one(
                {'django_user_id': user.id},
                {'$set': {
                    'username': user.username,
                    'email': user.email,
                    'password': user.password,
                    'role': getattr(user, 'role', 'student'),
                    'first_name': user.first_name or '',
                    'last_name': user.last_name or '',
                    'updated_at': datetime.utcnow()
                }}
            )
            print(f"Updated user: {user.username}")
    
    print(f"\nTotal users synced/updated: {synced_count}")
    return synced_count

if __name__ == '__main__':
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    django.setup()
    
    sync_users_to_mongodb()

