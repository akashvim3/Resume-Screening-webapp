from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='screening/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    
    # Job Description URLs
    path('jobs/create/', views.job_description_create, name='job_create'),
    path('jobs/', views.job_list, name='job_list'),
    
    # Resume URLs
    path('resumes/upload/', views.resume_upload, name='resume_upload'),
    path('resumes/', views.resume_list, name='resume_list'),
    
    # Screening URLs
    path('screen/<int:job_id>/', views.screen_resume, name='screen_resume'),
    path('results/<int:job_id>/', views.screening_results, name='screening_results'),
]
