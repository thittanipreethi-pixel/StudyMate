from django.contrib import admin
from .models import Year, Semester, Subject, StudyMaterial

@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'created_at']
    list_filter = ['year']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'semester', 'created_at']
    list_filter = ['semester']

@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'material_type', 'uploaded_by', 'created_at']
    list_filter = ['material_type', 'created_at']



