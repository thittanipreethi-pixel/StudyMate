from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentManagementViewSet, AcademicStructureViewSet, StudyMaterialManagementViewSet

router = DefaultRouter()
router.register(r'students', StudentManagementViewSet, basename='student')
router.register(r'academic-structure', AcademicStructureViewSet, basename='academic-structure')
router.register(r'materials', StudyMaterialManagementViewSet, basename='material')

urlpatterns = [
    path('', include(router.urls)),
]



