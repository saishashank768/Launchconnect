from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Job
from applications.models import Application
from students.models import StudentProfile


def job_list(request):
    jobs = (
        Job.objects
        .filter(status='OPEN')
        .select_related('startup')
        .order_by('-created_at')
    )

    # ---- Query params (cleaned) ----
    job_type = request.GET.get("type", "").strip()
    q = request.GET.get("q", "").strip()

    # ---- Filter: job type ----
    if job_type in ["internship", "job"]:
        jobs = jobs.filter(job_type=job_type)

    # ---- Search ----
    if q:
        jobs = jobs.filter(
            Q(title__icontains=q) |
            Q(startup__company_name__icontains=q)
        )
    
    # Phase 6 - Recommended Jobs
    recommended_jobs = Job.objects.none()
    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        skills = request.user.student_profile.skills.split(',')
        skills = [s.strip() for s in skills if s.strip()]
        if skills:
            pattern = Q()
            for skill in skills:
                pattern |= Q(description__icontains=skill) | Q(title__icontains=skill)
            recommended_jobs = Job.objects.filter(pattern, status='OPEN').exclude(id__in=jobs).distinct()[:3]

    context = {
        "jobs": jobs,
        "search_query": q,
        "selected_type": job_type,
        "is_internship": job_type == "internship",
        "is_job": job_type == "job",
        "recommended_jobs": recommended_jobs,
    }

    return render(request, "jobs/job_list.html", context)


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    has_applied = False

    if request.user.is_authenticated and request.user.is_student():
        try:
            student_profile = request.user.student_profile
            has_applied = Application.objects.filter(
                job=job,
                student=student_profile
            ).exists()
        except StudentProfile.DoesNotExist:
            pass

    context = {
        "job": job,
        "has_applied": has_applied,
    }

    return render(request, "jobs/job_detail.html", context)
