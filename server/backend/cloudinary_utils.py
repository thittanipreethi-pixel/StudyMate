"""
Cloudinary utility functions for file upload and management
"""
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.conf import settings

# Configure Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

def upload_file_to_cloudinary(file, folder='studymate/materials', resource_type='auto'):
    """
    Upload a file to Cloudinary
    
    Args:
        file: Django UploadedFile object
        folder: Cloudinary folder path
        resource_type: 'auto', 'image', 'raw', 'video'
    
    Returns:
        dict: Cloudinary upload response with public_id, url, secure_url, etc.
    """
    try:
        # Ensure file pointer is at the beginning
        if hasattr(file, 'seek'):
            file.seek(0)
        
        # Validate file is not empty
        if hasattr(file, 'size') and file.size == 0:
            raise Exception("File is empty")
        
        # Read file content if it's a file-like object
        # Cloudinary can handle file objects directly, but we need to ensure it's readable
        if hasattr(file, 'read'):
            # Reset to beginning
            file.seek(0)
            # Upload file to Cloudinary
            upload_result = cloudinary.uploader.upload(
                file,
                folder=folder,
                resource_type=resource_type,
                use_filename=True,
                unique_filename=True,
                overwrite=False
            )
        else:
            # If it's not a file-like object, try to upload directly
            upload_result = cloudinary.uploader.upload(
                file,
                folder=folder,
                resource_type=resource_type,
                use_filename=True,
                unique_filename=True,
                overwrite=False
            )
        
        return upload_result
    except Exception as e:
        raise Exception(f"Cloudinary upload failed: {str(e)}")

def delete_file_from_cloudinary(public_id):
    """
    Delete a file from Cloudinary
    
    Args:
        public_id: Cloudinary public_id of the file
    
    Returns:
        dict: Cloudinary delete response
    """
    try:
        result = cloudinary.uploader.destroy(public_id)
        return result
    except Exception as e:
        raise Exception(f"Cloudinary delete failed: {str(e)}")

def get_cloudinary_url(public_id, resource_type='auto', transformation=None):
    """
    Get Cloudinary URL for a file
    
    Args:
        public_id: Cloudinary public_id
        resource_type: 'auto', 'image', 'raw', 'video'
        transformation: Optional transformation parameters
    
    Returns:
        str: Cloudinary URL
    """
    try:
        if transformation:
            url = cloudinary.utils.cloudinary_url(public_id, resource_type=resource_type, **transformation)[0]
        else:
            url = cloudinary.utils.cloudinary_url(public_id, resource_type=resource_type)[0]
        return url
    except Exception as e:
        raise Exception(f"Failed to generate Cloudinary URL: {str(e)}")

