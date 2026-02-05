from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import StartupProfile
from .forms import StartupProfileForm
from jobs.models import Job
from jobs.forms import JobForm
from applications.models import Application

@login_required
def dashboard(request):
    if not request.user.is_startup():
        return redirect('login')
        
    profile, created = StartupProfile.objects.get_or_create(user=request.user)
    jobs = Job.objects.filter(startup=profile).order_by('-created_at')
    
    # Simple analytics provided by counting
    total_applicants = Application.objects.filter(job__startup=profile).count()
    
    context = {
        'profile': profile,
        'jobs': jobs,
        'total_applicants': total_applicants
    }
    return render(request, 'startup_dashboard.html', context)

@login_required
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

@login_required
def job_create(request):
    if not request.user.is_startup(): 
        return redirect('login')
        
    # Check verification
    if not request.user.startup_profile.is_verified:
        return render(request, 'error.html', {'message': 'You must be verified to post jobs.'})

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.startup = request.user.startup_profile
            job.save()
            return redirect('startup_dashboard')
    else:
        form = JobForm()
    return render(request, 'form_generic.html', {'form': form, 'title': 'Post a Job'})

@login_required
def job_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, startup__user=request.user)
    applications = job.applications.all().select_related('student', 'student__user')
    return render(request, 'job_applicants.html', {'job': job, 'applications': applications})
