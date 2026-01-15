from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Department, Year, Semester, Subject, StudyMaterial
from .serializers import DepartmentSerializer, YearSerializer, SemesterSerializer, SubjectSerializer, StudyMaterialSerializer

class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    """View all departments"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

class YearViewSet(viewsets.ReadOnlyModelViewSet):
    """View all years"""
    queryset = Year.objects.all()
    serializer_class = YearSerializer
    permission_classes = [IsAuthenticated]

class SemesterViewSet(viewsets.ReadOnlyModelViewSet):
    """View semesters with filters"""
    serializer_class = SemesterSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Semester.objects.all()
        
        # Filter by department
        department_id = self.request.query_params.get('department', None)
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        
        # Filter by year
        year_id = self.request.query_params.get('year', None)
        if year_id:
            queryset = queryset.filter(year_id=year_id)
        
        return queryset

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    """View subjects with filters"""
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Subject.objects.all()
        
        # Filter by semester
        semester_id = self.request.query_params.get('semester', None)
        if semester_id:
            queryset = queryset.filter(semester_id=semester_id)
        
        # Filter by department (through semester)
        department_id = self.request.query_params.get('department', None)
        if department_id:
            queryset = queryset.filter(semester__department_id=department_id)
        
        # Filter by year (through semester)
        year_id = self.request.query_params.get('year', None)
        if year_id:
            queryset = queryset.filter(semester__year_id=year_id)
        
        # Search by subject name
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(code__icontains=search)
            )
        
        return queryset

class StudyMaterialViewSet(viewsets.ReadOnlyModelViewSet):
    """Browse, search and download study materials"""
    serializer_class = StudyMaterialSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = StudyMaterial.objects.all()
        
        # Filter by subject
        subject_id = self.request.query_params.get('subject', None)
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        
        # Filter by department (through subject -> semester)
        department_id = self.request.query_params.get('department', None)
        if department_id:
            queryset = queryset.filter(subject__semester__department_id=department_id)
        
        # Filter by year (through subject -> semester)
        year_id = self.request.query_params.get('year', None)
        if year_id:
            queryset = queryset.filter(subject__semester__year_id=year_id)
        
        # Filter by semester (through subject)
        semester_id = self.request.query_params.get('semester', None)
        if semester_id:
            queryset = queryset.filter(subject__semester_id=semester_id)
        
        # Filter by material type
        material_type = self.request.query_params.get('type', None)
        if material_type:
            queryset = queryset.filter(material_type=material_type)
        
        # Search by title, description, or subject name
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(subject__name__icontains=search)
            )
        
        return queryset
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download a study material - redirect to Cloudinary URL"""
        from django.http import HttpResponseRedirect
        material = self.get_object()
        
        if material.cloudinary_secure_url:
            # Redirect to Cloudinary secure URL for download
            return HttpResponseRedirect(material.cloudinary_secure_url)
        elif material.cloudinary_url:
            return HttpResponseRedirect(material.cloudinary_url)
        elif material.file:
            # Fallback to local file if Cloudinary URL not available
            from django.http import FileResponse
            return FileResponse(material.file.open(), as_attachment=True, filename=material.file.name.split('/')[-1])
        return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

