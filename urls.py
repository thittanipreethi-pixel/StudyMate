from django.contrib import admin
from django.http import JsonResponse

from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from students.views import CustomTokenObtainPairView

def home(request):
    return HttpResponse("Django is running successfully 🚀")

def home(request):
    return JsonResponse({  # Change from HttpResponse to JsonResponse
        "message": "StudyMate Backend is running 🚀",
        "endpoints": {
            "admin": "/admin/",
            "api_token": "/api/token/",
            "api_token_refresh": "/api/token/refresh/",
            "api_student": "/api/student/",
            "api_admin": "/api/admin/"
        }
    })

urlpatterns = [
    path('', home),                                  # Home page
    path('admin/', admin.site.urls),                 # Django admin
    path('api/admin/', include('adminpanel.urls')),  # Admin APIs
    path('api/student/', include('students.urls')),
    path('', include('accounts.urls')),
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),

    

    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
