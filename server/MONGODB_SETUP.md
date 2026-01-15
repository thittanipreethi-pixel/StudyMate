# MongoDB Setup for StudyMate

## ✅ MongoDB Integration Complete

Your login credentials and user data are now being stored in **MongoDB**!

## 📍 Data Storage Locations

### 1. **MongoDB (Primary for User Credentials)**
- **Connection**: `mongodb+srv://nalliayanandhakumar_db_user:StudyMate@cluster0.giucynj.mongodb.net/studymate_db`
- **Database**: `studymate_db`
- **Collection**: `users`
- **Contains**: All user credentials (username, email, hashed passwords, role, etc.)

### 2. **SQLite (Django ORM - Still Used)**
- **Location**: `server/db.sqlite3`
- **Purpose**: Django's built-in features still use SQLite
- **Contains**: Users, Years, Semesters, Subjects, Study Materials

## 🔄 How It Works

1. **Registration**: When a new user registers:
   - User is created in SQLite (Django)
   - User credentials are **also stored in MongoDB**
   - Both databases stay in sync

2. **Login**: 
   - Authentication uses Django (SQLite)
   - MongoDB has a backup copy of all credentials

3. **Data Sync**: 
   - All 6 existing users have been synced to MongoDB
   - New registrations automatically sync to MongoDB

## 📊 Current Data Status

- **Users in MongoDB**: 6 users synced
- **Users in SQLite**: 6 users
- All credentials are stored in both locations

## 🛠️ Management Commands

### Sync Users to MongoDB
```bash
cd server
source venv/bin/activate
python accounts/mongodb_sync.py
```

### View MongoDB Data
```python
from backend.mongodb import get_collection
users = get_collection('users')
for user in users.find():
    print(user)
```

## 🔐 Security Notes

- Passwords are hashed using Django's password hashing
- MongoDB connection uses SSL (certificate verification disabled for development)
- In production, enable proper SSL certificate verification

## 📝 Next Steps

All new user registrations will automatically be stored in MongoDB. The system now maintains user credentials in both:
- SQLite (for Django compatibility)
- MongoDB (as requested)

Your MongoDB database is ready to use! 🎉



