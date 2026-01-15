from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from backend.mongodb import get_collection
from datetime import datetime
from .serializers import CustomTokenObtainPairSerializer, UserSerializer

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new student"""
    data = request.data
    
    # Validate required fields
    required_fields = ['username', 'email', 'password']
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
        return Response({
            'error': f'Missing required fields: {", ".join(missing_fields)}'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if email already exists
    if User.objects.filter(email=data.get('email')).exists():
        return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if username already exists
    if User.objects.filter(username=data.get('username')).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Validate password length
    password = data.get('password', '')
    if len(password) < 6:
        return Response({'error': 'Password must be at least 6 characters long'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Validate email format
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(data.get('email'))
    except ValidationError:
        return Response({'error': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Create user in Django (SQLite)
        user = User.objects.create_user(
            username=data.get('username'),
            email=data.get('email'),
            password=password,
            role='student',
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', '')
        )
        
        # Also store in MongoDB
        users_collection = get_collection('users')
        user_doc = {
            'username': data.get('username'),
            'email': data.get('email'),
            'password': make_password(password),  # Hash password
            'role': 'student',
            'first_name': data.get('first_name', ''),
            'last_name': data.get('last_name', ''),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'django_user_id': user.id  # Link to Django user
        }
        users_collection.insert_one(user_doc)
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ValueError as e:
        return Response({
            'error': f'Validation error: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        import traceback
        return Response({
            'error': f'Registration failed: {str(e)}',
            'details': str(traceback.format_exc()) if settings.DEBUG else None
        }, status=status.HTTP_400_BAD_REQUEST)

