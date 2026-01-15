from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, YearViewSet, SemesterViewSet, SubjectViewSet, StudyMaterialViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'years', YearViewSet, basename='year')
router.register(r'semesters', SemesterViewSet, basename='semester')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'materials', StudyMaterialViewSet, basename='material')

urlpatterns = [
    path('', include(router.urls)),
]

