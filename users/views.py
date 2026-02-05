from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm

def home(request):
    return render(request, 'users/home.html')

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
                return redirect('admin:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    
    def get_success_url(self):
        user = self.request.user
        if user.role == 'student':
            return '/students/dashboard/' # Hardcoded for now, will use reverse later
        elif user.role == 'startup':
            return '/startups/dashboard/'
        elif user.role == 'founder':
            return '/founder-collab/'
        return '/admin/'
