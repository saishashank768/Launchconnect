from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import StartupProfile
from .forms import StartupProfileForm
from jobs.models import Job
from jobs.forms import JobForm
from applications.models import Application

def startup_required(view_func):
    """Decorator to check if user is a startup"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_startup():
            return HttpResponseForbidden("You don't have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper

@startup_required
def dashboard(request):
    # Check email verification status
    if not request.user.is_email_verified:
        from django.contrib import messages
        messages.warning(request, 'Please verify your email to unlock all features.')
        
    profile, created = StartupProfile.objects.get_or_create(user=request.user)
    jobs = Job.objects.filter(startup=profile).order_by('-created_at')
    
    # Simple analytics provided by counting
    total_applicants = Application.objects.filter(job__startup=profile).count()
    
    context = {
        'profile': profile,
        'jobs': jobs,
        'total_applicants': total_applicants,
        'email_verified': request.user.is_email_verified,
    }
    return render(request, 'startups/startup_dashboard.html', context)

@startup_required
def profile_edit(request):
    profile, created = StartupProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = StartupProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('startup_dashboard')
    else:
        form = StartupProfileForm(instance=profile)
    return render(request, 'form_generic.html', {'form': form, 'title': 'Edit Company Profile'})

@startup_required
def job_create(request):
    # Get or create startup profile
    profile, created = StartupProfile.objects.get_or_create(user=request.user)
    
    # Check email verification
    if not request.user.is_email_verified:
        from django.contrib import messages
        messages.error(request, 'Please verify your email address before posting jobs.')
        return redirect('verification_pending', username=request.user.username)
    
    # Check verification
    if not profile.is_verified:
        return render(request, 'error.html', {'message': 'Your company account is pending verification. An admin will review your application shortly.'})

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.startup = profile
            job.save()
            return redirect('startup_dashboard')
    else:
        form = JobForm()
    return render(request, 'form_generic.html', {'form': form, 'title': 'Post a Job'})

@startup_required
def job_applicants(request, job_id):
    # Ensure the job belongs to this startup
    job = get_object_or_404(Job, id=job_id, startup__user=request.user)
    applications = job.applications.all().select_related('student', 'student__user')
    return render(request, 'jobs/job_applicants.html', {'job': job, 'applications': applications})
