from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from startups.models import StartupProfile
from users.models import User
from jobs.models import Job

@staff_member_required
def admin_dashboard(request):
    startups_pending = StartupProfile.objects.filter(is_verified=False)
    total_users = User.objects.count()
    total_jobs = Job.objects.count()
    
    context = {
        'startups_pending': startups_pending,
        'total_users': total_users,
        'total_jobs': total_jobs,
    }
    return render(request, 'admin_dashboard.html', context)

@staff_member_required
def verify_startup(request, startup_id):
    startup = get_object_or_404(StartupProfile, id=startup_id)
    startup.is_verified = True
    startup.save()
    return redirect('admin_dashboard_custom')
