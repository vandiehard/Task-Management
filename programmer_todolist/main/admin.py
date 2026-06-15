from django.contrib import admin
from .models import ProgrammerProfile, Project, ProjectSubmission

@admin.register(ProgrammerProfile)
class ProgrammerProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'email', 'is_available', 'created_at')
    list_filter = ('is_available', 'created_at')
    search_fields = ('full_name', 'email', 'user__username')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'assigned_to', 'deadline', 'created_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('title', 'description')

@admin.register(ProjectSubmission)
class ProjectSubmissionAdmin(admin.ModelAdmin):
    list_display = ('project', 'submitted_at', 'is_approved')
    list_filter = ('is_approved', 'submitted_at')
