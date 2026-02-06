from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from startups.models import StartupProfile
from users.models import User
from jobs.models import Job

def admin_required(view_func):
    """Decorator to check if user is admin"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_admin_role():
            return HttpResponseForbidden("You don't have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper

@admin_required
def admin_dashboard(request):
    startups_pending = StartupProfile.objects.filter(is_verified=False)
    total_users = User.objects.count()
    total_jobs = Job.objects.count()
    from applications.models import Application
    from founder_collab.models import FounderNeed
    total_conversions = Application.objects.filter(is_conversion=True).count()
    total_needs = FounderNeed.objects.count()
    
    context = {
        'startups_pending': startups_pending,
        'total_users': total_users,
        'total_jobs': total_jobs,
        'total_conversions': total_conversions,
        'total_needs': total_needs,
    }
    return render(request, 'admin_panel/admin_dashboard.html', context)

@admin_required
def verify_startup(request, startup_id):
    startup = get_object_or_404(StartupProfile, id=startup_id)
    startup.is_verified = True
    startup.save()
    
    if request.headers.get('HX-Request'):
        from django.http import HttpResponse
        return HttpResponse("")
        
    return redirect('admin_dashboard_custom')
