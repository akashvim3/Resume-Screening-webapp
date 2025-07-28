from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
from .models import JobDescription, Resume, Screening, CandidateProfile
from .forms import JobDescriptionForm, ResumeUploadForm, CandidateProfileForm, UserRegistrationForm
from .utils import ResumeParser, ResumeScorer

def home(request):
    return render(request, 'screening/home.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            CandidateProfile.objects.get_or_create(user=user)
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'screening/register.html', {'form': form})

@login_required
def profile(request):
    profile = get_object_or_404(CandidateProfile, user=request.user)
    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = CandidateProfileForm(instance=profile)
    return render(request, 'screening/profile.html', {'form': form, 'profile': profile})

@login_required
def dashboard(request):
    context = {
        'job_count': JobDescription.objects.filter(created_by=request.user).count(),
        'resume_count': Resume.objects.filter(uploaded_by=request.user).count(),
        'recent_screenings': Screening.objects.filter(
            job__created_by=request.user
        ).select_related('job', 'resume')[:5]
    }
    return render(request, 'screening/dashboard.html', context)

@login_required
def job_description_create(request):
    if request.method == 'POST':
        form = JobDescriptionForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            messages.success(request, 'Job description created successfully.')
            return redirect('job_list')
    else:
        form = JobDescriptionForm()
    return render(request, 'screening/job_form.html', {'form': form})

@login_required
def job_list(request):
    jobs = JobDescription.objects.filter(created_by=request.user)
    return render(request, 'screening/job_list.html', {'jobs': jobs})

@login_required
def resume_upload(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.uploaded_by = request.user
            resume.save()
            messages.success(request, 'Resume uploaded successfully.')
            return redirect('resume_list')
    else:
        form = ResumeUploadForm()
    return render(request, 'screening/resume_form.html', {'form': form})

@login_required
def resume_list(request):
    resumes = Resume.objects.filter(uploaded_by=request.user)
    return render(request, 'screening/resume_list.html', {'resumes': resumes})

@login_required
def screen_resume(request, job_id):
    job = get_object_or_404(JobDescription, id=job_id, created_by=request.user)
    
    if request.method == 'POST':
        resume_ids = request.POST.getlist('resumes')
        resumes = Resume.objects.filter(id__in=resume_ids)
        
        for resume in resumes:
            parser = ResumeParser(resume.resume_file.path)
            scorer = ResumeScorer(
                parser._extract_content(),
                {
                    'required_skills': job.required_skills,
                    'minimum_experience': job.minimum_experience
                }
            )
            
            skills_score, exp_score, overall_score = scorer.calculate_scores()
            
            Screening.objects.create(
                job=job,
                resume=resume,
                skills_match_score=skills_score,
                experience_match_score=exp_score,
                overall_score=overall_score
            )
        
        messages.success(request, 'Resumes screened successfully.')
        return redirect('screening_results', job_id=job.id)
    
    resumes = Resume.objects.filter(uploaded_by=request.user)
    return render(request, 'screening/screen_resume.html', {
        'job': job,
        'resumes': resumes
    })

@login_required
def screening_results(request, job_id):
    job = get_object_or_404(JobDescription, id=job_id, created_by=request.user)
    screenings = Screening.objects.filter(job=job).select_related('resume')
    return render(request, 'screening/screening_results.html', {
        'job': job,
        'screenings': screenings
    })
