# Cloudinary Setup Guide

This guide explains how to configure Cloudinary for storing study materials in the StudyMate application.

## Overview

StudyMate uses Cloudinary to store all uploaded study materials (PDFs, documents, etc.) in the cloud instead of local storage. File metadata is stored in both:
- **SQLite (Django ORM)**: For quick queries and relationships
- **MongoDB**: For full document storage and advanced queries

## Prerequisites

1. A Cloudinary account (free tier available at https://cloudinary.com)
2. Cloudinary credentials (Cloud Name, API Key, API Secret)

## Setup Steps

### 1. Create a Cloudinary Account

1. Go to https://cloudinary.com/users/register/free
2. Sign up for a free account
3. After registration, you'll be taken to your dashboard

### 2. Get Your Cloudinary Credentials

From your Cloudinary dashboard:

1. Click on **Settings** (gear icon) or go to **Dashboard**
2. You'll see:
   - **Cloud Name**: Your unique cloud name
   - **API Key**: Your API key
   - **API Secret**: Your API secret (click "Reveal" to see it)

### 3. Configure Environment Variables

Create a `.env` file in the `server/` directory (if it doesn't exist) and add:

```env
# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name_here
CLOUDINARY_API_KEY=your_api_key_here
CLOUDINARY_API_SECRET=your_api_secret_here

# MongoDB Configuration (already configured)
MONGODB_URI=mongodb+srv://nalliayanandhakumar_db_user:StudyMate@cluster0.giucynj.mongodb.net/studymate_db?retryWrites=true&w=majority
```

**Important**: Never commit your `.env` file to version control! It contains sensitive credentials.

### 4. Install Dependencies

The Cloudinary package is already in `requirements.txt`. If you haven't installed it yet:

```bash
cd server
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Verify Configuration

Test your Cloudinary connection by running:

```bash
python manage.py shell
```

Then in the Python shell:

```python
from backend.cloudinary_utils import cloudinary
print(f"Cloud Name: {cloudinary.config().cloud_name}")
```

If it prints your cloud name, the configuration is correct!

## How It Works

### File Upload Flow

1. **User uploads file** → Admin Dashboard
2. **Django receives file** → `StudyMaterialManagementViewSet.perform_create()`
3. **File uploaded to Cloudinary** → Stored in organized folders:
   ```
   studymate/materials/{department}/{year}/semester_{number}/{subject}/{filename}
   ```
4. **Metadata saved to SQLite** → Django ORM (StudyMaterial model)
5. **Metadata saved to MongoDB** → Full document with all details

### File Storage Structure

Files are organized in Cloudinary by:
- Department (e.g., CSE, EEE, ECE)
- Year (e.g., Year 1, Year 2)
- Semester (e.g., Semester 1, Semester 2)
- Subject (e.g., Applied Calculus, Computer Programming)

Example path:
```
studymate/materials/CSE/Year 1/semester_1/Applied Calculus/notes_abc123.pdf
```

### Data Storage

#### SQLite (Django ORM)
Stores:
- Material ID, title, description
- Cloudinary URLs and public_id
- File metadata (name, size, format)
- Relationships (subject, uploaded_by)

#### MongoDB
Stores complete document with:
- All SQLite data
- Additional metadata
- Full searchable text
- Timestamps

### File Download

When users download materials:
1. **Admin/Student clicks download**
2. **Backend redirects to Cloudinary secure URL**
3. **Cloudinary serves the file** directly to the user
4. **No server bandwidth used** - files served from Cloudinary CDN

### File Deletion

When admin deletes a material:
1. **Delete from Cloudinary** → Removes file from cloud storage
2. **Delete from MongoDB** → Removes document
3. **Delete from SQLite** → Removes database record
4. **All traces removed** → Complete permanent deletion

## Benefits

✅ **Scalability**: No server storage limits  
✅ **Performance**: Files served from Cloudinary's global CDN  
✅ **Reliability**: Cloudinary handles backups and redundancy  
✅ **Cost-effective**: Free tier includes 25GB storage and 25GB bandwidth/month  
✅ **Organization**: Automatic folder structure  
✅ **Security**: Secure URLs with access control  

## Troubleshooting

### Error: "Cloudinary upload failed"

**Possible causes:**
1. Invalid credentials in `.env`
2. Network connectivity issues
3. File size exceeds Cloudinary limits (free tier: 10MB per file)

**Solution:**
- Verify credentials in `.env` file
- Check Cloudinary dashboard for upload limits
- Ensure internet connection is stable

### Error: "Cloudinary delete failed"

**Possible causes:**
1. Invalid public_id
2. File already deleted
3. Network issues

**Solution:**
- Check if file exists in Cloudinary dashboard
- Verify public_id is correct
- Retry the operation

### Files not appearing in Cloudinary

**Check:**
1. Cloudinary dashboard → Media Library
2. Look in the `studymate/materials/` folder
3. Verify upload was successful (check Django logs)

## Migration from Local Storage

If you have existing materials stored locally:

1. **Keep local files** as backup
2. **Re-upload through admin dashboard** → Will automatically upload to Cloudinary
3. **Old local files** can be deleted after verification

## Security Best Practices

1. ✅ Keep `.env` file secure (never commit to git)
2. ✅ Use environment variables in production
3. ✅ Enable Cloudinary signed URLs for sensitive materials (optional)
4. ✅ Regularly rotate API keys
5. ✅ Monitor Cloudinary usage dashboard

## Support

- Cloudinary Documentation: https://cloudinary.com/documentation
- Cloudinary Support: https://support.cloudinary.com
- Django Cloudinary Integration: https://cloudinary.com/documentation/django_integration


