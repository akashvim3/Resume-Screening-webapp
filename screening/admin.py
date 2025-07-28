from django.contrib import admin
from .models import JobDescription, Resume, Screening, CandidateProfile

@admin.register(JobDescription)
class JobDescriptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('candidate_name', 'email', 'uploaded_by', 'uploaded_at')

@admin.register(Screening)
class ScreeningAdmin(admin.ModelAdmin):
    list_display = ('job', 'resume', 'overall_score', 'screened_at')

@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'experience', 'profile_image_preview')
    readonly_fields = ('profile_image_preview',)
    
    def profile_image_preview(self, obj):
        if obj.profile_image:
            return f'<img src="{obj.profile_image.url}" style="width:40px; height:40px; object-fit:cover; border-radius:50%;" />'
        return "No Image"
    profile_image_preview.allow_tags = True
    profile_image_preview.short_description = 'Profile Image'
