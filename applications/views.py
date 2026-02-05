from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from .models import Application
from jobs.models import Job

@login_required
def apply_job(request, job_id):
    if not request.user.is_student():
        return HttpResponse("Unauthorized", status=403)
        
    job = get_object_or_404(Job, pk=job_id)
    # Check if already applied
    if Application.objects.filter(student=request.user.student_profile, job=job).exists():
        return HttpResponse('<button class="bg-gray-300 text-gray-600 px-6 py-3 rounded-lg font-semibold cursor-not-allowed" disabled><i class="fas fa-check mr-2"></i>Applied</button>')
        
    Application.objects.create(student=request.user.student_profile, job=job)
    
    # Phase 5 - Notification for Startup
    from users.models import Notification
    Notification.objects.create(
        user=job.startup.user,
        title="New Job Applicant",
        message=f"{request.user.username} applied for {job.title}",
        link=f"/startups/applicants/{job.id}/"
    )
    
    # Return HTMX partial
    return HttpResponse('<button class="bg-green-600 text-white px-6 py-3 rounded-lg font-semibold cursor-not-allowed" disabled><i class="fas fa-check mr-2"></i>Applied Successfully</button>')

@login_required
def update_status(request, application_id):
    if not request.user.is_startup():
        return HttpResponse("Unauthorized", status=403)
    
    app = get_object_or_404(Application, pk=application_id)
    # Ensure startup owns the job
    if app.job.startup.user != request.user:
        return HttpResponse("Unauthorized", status=403)
        
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            app.status = new_status
            app.save()
            
            # Phase 5 - Notification for Student
            from users.models import Notification
            Notification.objects.create(
                user=app.student.user,
                title="Application Status Updated",
                message=f"Your application for {app.job.title} is now {app.get_status_display()}",
                link="/students/dashboard/"
            )
            
            # Return Tailwind-styled badge based on status
            color_classes = {
                'HIRED': 'bg-green-100 text-green-700',
                'SHORTLISTED': 'bg-blue-100 text-blue-700',
                'REJECTED': 'bg-red-100 text-red-700',
                'PENDING': 'bg-gray-100 text-gray-700',
            }
            badge_class = color_classes.get(new_status, 'bg-gray-100 text-gray-700')
            return HttpResponse(f'<span class="px-3 py-1 text-sm rounded-full font-semibold {badge_class}">{app.get_status_display()}</span>')
            
    return HttpResponse(status=400)

@login_required
def convert_to_job(request, application_id):
    if not request.user.is_startup():
        return HttpResponse("Unauthorized", status=403)
        
    app = get_object_or_404(Application, pk=application_id)
    if app.job.startup.user != request.user:
        return HttpResponse("Unauthorized", status=403)
        
    if app.status != 'HIRED':
        return HttpResponse("Candidate must be hired first", status=400)
        
    app.is_conversion = True
    from django.utils import timezone
    app.conversion_date = timezone.now()
    app.save()
    
    return HttpResponse('<span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold bg-indigo-100 text-indigo-700"><i class="fas fa-check-circle mr-1"></i>Converted to Full-time</span>')
