from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

def home(request):
    return render(request, 'users/home.html')

@login_required
def mark_notifications_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'startup':
                return redirect('startup_dashboard')
            elif user.role == 'founder':
                return redirect('founder_feed')
            else:
                return redirect('admin_dashboard_custom')
    else:
        role = request.GET.get('role')
        initial_data = {}
        if role:
            initial_data['role'] = role
        form = CustomUserCreationForm(initial=initial_data)
    return render(request, 'users/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    
    def get_success_url(self):
        user = self.request.user
        if user.role == 'student':
            return '/students/dashboard/'
        elif user.role == 'startup':
            return '/startups/dashboard/'
        elif user.role == 'founder':
            return '/founder-collab/'
        elif user.is_staff or user.role == 'admin':
            return '/admin-panel/'
        return '/'
