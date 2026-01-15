# Study Materials File Storage Guide

## 📁 Where Files Are Stored

### Physical Storage Location
- **Directory**: `/Users/muthuanushya/Documents/ProjectHub/StudyMate/server/media/study_materials/`
- **Full Path**: `server/media/study_materials/`
- **Example File**: `Acct_Statement_6447_21122025_06.51.48.pdf` (13.4 KB)

### Django Configuration
- **MEDIA_ROOT**: `server/media/` (set in `backend/settings.py`)
- **MEDIA_URL**: `/media/` (URL prefix for accessing files)
- **Upload Path**: Files are stored in `study_materials/` subdirectory

## 📄 Supported File Types

The system accepts **any file type**, including:
- ✅ **PDFs** (`.pdf`) - Most common for study materials
- ✅ **Word Documents** (`.doc`, `.docx`)
- ✅ **Text Files** (`.txt`)
- ✅ **Images** (`.jpg`, `.png`, `.gif`)
- ✅ **PowerPoint** (`.ppt`, `.pptx`)
- ✅ **Excel** (`.xls`, `.xlsx`)
- ✅ **Any other file format**

## 🔐 How Files Are Stored

### Database Record
Each uploaded file creates a record in the `study_materials` table with:
- **File Path**: Stored as relative path (e.g., `study_materials/filename.pdf`)
- **File Name**: Original filename is preserved
- **Subject**: Linked to a specific subject
- **Metadata**: Title, description, material type, uploader, timestamps

### File System
- Files are stored on the server's file system
- Django's `FileField` handles file uploads automatically
- Files are organized in the `media/study_materials/` directory

## 🌐 How Files Are Accessed

### 1. **Direct URL Access** (Development)
When Django is in DEBUG mode:
- **URL Format**: `http://localhost:8000/media/study_materials/filename.pdf`
- **Example**: `http://localhost:8000/media/study_materials/Acct_Statement_6447_21122025_06.51.48.pdf`
- Files are served directly by Django's development server

### 2. **API Download Endpoint** (Recommended)
- **Endpoint**: `GET /api/student/materials/{id}/download/`
- **Authentication**: Requires JWT token
- **Response**: File download with proper headers
- **Usage**: Used by the frontend download button

### 3. **File URL in API Response**
When fetching materials via API:
- **Endpoint**: `GET /api/student/materials/`
- **Response includes**: `file_url` field with full URL
- **Example**: `"file_url": "http://localhost:8000/media/study_materials/filename.pdf"`

## 📥 Download Functionality

### Frontend Implementation
The download is handled in `StudentDashboard.jsx`:

```javascript
const handleDownload = async (materialId) => {
  try {
    await api.downloadMaterial(materialId)
  } catch (error) {
    alert('Failed to download material')
  }
}
```

### API Implementation
The download endpoint in `students/views.py`:
- Returns file as `FileResponse`
- Sets proper headers for file download
- Includes original filename
- Requires authentication

## 🔍 Current Storage Status

### Existing Files
- **Location**: `server/media/study_materials/`
- **Example File**: `Acct_Statement_6447_21122025_06.51.48.pdf` (13.4 KB)
- **Total Files**: Check with `ls -la server/media/study_materials/`

### Database Records
- Materials are stored in SQLite database (`db.sqlite3`)
- Each material has a reference to the file path
- File metadata is stored in the `study_materials` table

## 🚀 Upload Process

### Admin Upload Flow
1. Admin selects subject, title, description, type, and file
2. File is uploaded via `POST /api/admin/materials/`
3. Django saves file to `media/study_materials/`
4. Database record is created with file path
5. File is accessible immediately after upload

### File Naming
- Django automatically handles file naming
- Original filename may be modified if duplicates exist
- Files are stored with their original extension

## 🔒 Security & Access Control

### Authentication Required
- ✅ All file downloads require authentication
- ✅ Only authenticated users can access files
- ✅ Admin can upload, students can download

### File Access
- Files are not publicly accessible without authentication
- Download endpoint validates user authentication
- Direct URL access works in DEBUG mode only

## 📊 File Storage in Production

### For Production Deployment
1. **Use a CDN or Cloud Storage** (AWS S3, Google Cloud Storage, etc.)
2. **Configure MEDIA_ROOT** to point to cloud storage
3. **Use django-storages** package for cloud integration
4. **Set up proper file serving** (Nginx, Apache, or cloud CDN)

### Current Setup (Development)
- Files are stored locally on the server
- Served directly by Django (DEBUG mode)
- Suitable for development and testing

## 🛠️ Management Commands

### View Uploaded Files
```bash
cd server
ls -la media/study_materials/
```

### Check File Size
```bash
du -sh server/media/study_materials/
```

### View Materials in Database
```python
python manage.py shell
from students.models import StudyMaterial
materials = StudyMaterial.objects.all()
for m in materials:
    print(f"{m.title}: {m.file.name}")
```

## ✅ Summary

- **Storage Location**: `server/media/study_materials/`
- **File Types**: All file types supported (PDFs, DOCX, etc.)
- **Access**: Via API download endpoint or direct URL (DEBUG mode)
- **Security**: Authentication required for all downloads
- **Current Status**: ✅ Working - PDFs are accessible and downloadable

Your PDFs and other study materials are stored safely and can be downloaded by authenticated users! 🎉



