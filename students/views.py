from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import StudentProfile
from .forms import StudentProfileForm
from applications.models import Application

@login_required
def dashboard(request):
    if not request.user.is_student():
        return redirect('login')
    
    profile, created = StudentProfile.objects.get_or_create(user=request.user)
    applications = Application.objects.filter(student=profile).select_related('job', 'job__startup')
    
    # Phase 6 - Intelligence: Recommended Jobs
    from jobs.models import Job
    from django.db.models import Q
    
    recommended_jobs = Job.objects.none()
    if profile.skills:
        skill_list = [s.strip() for s in profile.skills.split(',') if s.strip()]
        if skill_list:
            query = Q()
            for skill in skill_list:
                query |= Q(title__icontains=skill) | Q(description__icontains=skill)
            
            # Filter recommended jobs (exclude already applied)
            applied_job_ids = applications.values_list('job_id', flat=True)
            recommended_jobs = Job.objects.filter(query, status='OPEN').exclude(id__in=applied_job_ids).distinct()[:5]
    
    context = {
        'profile': profile,
        'applications': applications,
        'recommended_jobs': recommended_jobs,
    }
    return render(request, 'students/student_dashboard.html', context)

@login_required
def profile_edit(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('student_dashboard')
    else:
        form = StudentProfileForm(instance=profile)
    return render(request, 'form_generic.html', {'form': form, 'title': 'Edit Profile'})
