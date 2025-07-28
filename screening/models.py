from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class JobDescription(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.TextField()
    minimum_experience = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Resume(models.Model):
    candidate_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    resume_file = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.candidate_name}'s Resume"

class Screening(models.Model):
    job = models.ForeignKey(JobDescription, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    skills_match_score = models.FloatField()
    experience_match_score = models.FloatField()
    overall_score = models.FloatField()
    screened_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-overall_score']

    def __str__(self):
        return f"Screening for {self.resume.candidate_name} - {self.job.title}"

class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.OneToOneField(Resume, on_delete=models.SET_NULL, null=True, blank=True)
    skills = models.TextField(blank=True)
    experience = models.IntegerField(default=0)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_images/default.png', blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
