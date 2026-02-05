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
    
    context = {
        'profile': profile,
        'applications': applications,
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
