from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.views import CustomTokenObtainPairView

def home(request):
    from django.http import JsonResponse
    return JsonResponse({
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
    path('', home),
    path('admin/', admin.site.urls),
    path('api/admin/', include('adminpanel.urls')),
    path('api/student/', include('students.urls')),
    path('api/auth/', include('accounts.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



