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
        return HttpResponse('<button class="btn btn-secondary" disabled>Applied</button>')
        
    Application.objects.create(student=request.user.student_profile, job=job)
    
    # Return HTMX partial
    return HttpResponse('<button class="btn btn-success" disabled>Applied Successfully</button>')

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
            return HttpResponse(f'<span class="badge bg-secondary status-badge">{app.get_status_display()}</span>')
            
    return HttpResponse(status=400)
