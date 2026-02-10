from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import StudentProfile
from .forms import StudentProfileForm
from applications.models import Application

def student_required(view_func):
    """Decorator to check if user is a student"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_student():
            return HttpResponseForbidden("You don't have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper

@student_required
def dashboard(request):
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
    # Compute a simple skill match score based on open jobs containing student's skills.
    skill_match_score = 0
    skill_list = []
    if profile.skills:
        skill_list = [s.strip().lower() for s in profile.skills.split(',') if s.strip()]
    if skill_list:
        # look across open jobs to see which skills appear
        open_jobs = Job.objects.filter(status='OPEN')
        matched_skills = set()
        for job in open_jobs:
            text = (job.title or '') + ' ' + (job.description or '')
            text = text.lower()
            for s in skill_list:
                if s in text:
                    matched_skills.add(s)
        try:
            skill_match_score = int(len(matched_skills) / len(skill_list) * 100)
        except ZeroDivisionError:
            skill_match_score = 0
    else:
        skill_match_score = 0
    
    context = {
        'profile': profile,
        'applications': applications,
        'recommended_jobs': recommended_jobs,
        'skill_match_score': skill_match_score,
        'applications_sent': applications.count(),
        'invites_count': applications.filter(status='SHORTLISTED').count(),
        'profile_views_count': 0,
        'saved_jobs_count': 0,
        'profile_completion_total': 10,
        'profile_completion_done': sum([
            1 if profile.resume_url else 0,
            1 if profile.skills else 0,
            1 if profile.preferred_roles else 0,
            1 if profile.education else 0,
            1 if profile.portfolio_url else 0,
            1 if profile.weekly_hours else 0,
            1 if profile.availability else 0,
            1 if profile.work_mode else 0,
            1 if profile.start_date else 0,
            1 if profile.actively_looking else 0,
        ]),
        'profile_completion_pct': 0,
    }
    try:
        context['profile_completion_pct'] = int(context['profile_completion_done'] / context['profile_completion_total'] * 100)
    except Exception:
        context['profile_completion_pct'] = 0
    return render(request, 'students/student_dashboard.html', context)

@student_required
def profile_edit(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        old_photo = profile.photo  # 👈 capture BEFORE form binds

        form = StudentProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            new_profile = form.save()  # ✅ SAVE FIRST

            # ✅ Delete old photo ONLY if a new one was saved
            if (
                'photo' in request.FILES
                and old_photo
                and old_photo != new_profile.photo
            ):
                old_photo.delete(save=False)

            return redirect('student_dashboard')
    else:
        form = StudentProfileForm(instance=profile)

    return render(request, 'students/student_profile_edit.html', {'form': form})
