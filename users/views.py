from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from .forms import CustomUserCreationForm
from .models import User
import uuid

class EmailVerificationBackend(ModelBackend):
    """Custom authentication backend that checks email verification"""
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        
        if not user.is_email_verified:
            return None  # Reject login if email not verified
            
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

def send_verification_email(user, request):
    """Send email verification link to user"""
    token = str(uuid.uuid4())
    user.email_verification_token = token
    user.save()
    
    # Build verification link using SITE_URL if configured (avoids 'testserver' links), otherwise use request
    site_url = getattr(settings, 'SITE_URL', None)
    if site_url:
        verification_link = f"{site_url.rstrip('/')}/verify-email/{token}/"
    else:
        verification_link = request.build_absolute_uri(f'/verify-email/{token}/')
    subject = 'LaunchConnect - Verify Your Email'
    
    # Plain text version
    text_message = f'''Hello {user.username},

Thank you for registering with LaunchConnect!

Please verify your email by clicking the link below:
{verification_link}

This link will expire in 24 hours.

Best regards,
LaunchConnect Team'''
    
    # HTML version for better email client support
    html_message = f'''<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #6B3FA0 0%, #5A40A8 100%); color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
        .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; border-radius: 0 0 5px 5px; }}
        .button {{ display: inline-block; padding: 12px 24px; background: #6B3FA0; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; }}
        .footer {{ text-align: center; font-size: 12px; color: #666; margin-top: 20px; }}
        .link-section {{ background: #ffffff; padding: 15px; border: 1px dashed #ddd; border-radius: 3px; margin: 15px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Verify Your Email</h1>
        </div>
        <div class="content">
            <p>Hello <strong>{user.username}</strong>,</p>
            <p>Thank you for registering with <strong>LaunchConnect</strong>!</p>
            <p>Please verify your email by clicking the button below:</p>
            <center>
                <a href="{verification_link}" class="button">Verify Email Address</a>
            </center>
            <p style="text-align: center; margin: 20px 0;">OR</p>
            <p>Copy and paste this link in your browser:</p>
            <div class="link-section">
                <p style="word-break: break-all; margin: 0;"><code>{verification_link}</code></p>
            </div>
            <p>This link will expire in 24 hours.</p>
            <hr>
            <p><small>If you didn't create this account, you can safely ignore this email.</small></p>
        </div>
        <div class="footer">
            <p>LaunchConnect Team &copy; 2026</p>
        </div>
    </div>
</body>
</html>'''
    
    # Use EmailMessage for proper HTML support
    email = EmailMessage(
        subject=subject,
        body=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    email.content_subtype = 'html'  # This tells it to send as HTML
    email.send(fail_silently=False)

def home(request):
    # If user is authenticated, redirect to their respective dashboard
    if request.user.is_authenticated:
        if request.user.is_student():
            return redirect('student_dashboard')
        elif request.user.is_startup():
            return redirect('startup_dashboard')
        elif request.user.is_founder():
            return redirect('founder_feed')
        elif request.user.is_admin_role():
            return redirect('admin_dashboard_custom')
    
    # Public landing page for unauthenticated users
    return render(request, 'users/home.html')

@login_required
def mark_notifications_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            
            # Send verification email
            try:
                send_verification_email(user, request)
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.headers.get('Accept') == 'application/json':
                    return JsonResponse({
                        'success': True,
                        'redirect_url': reverse('verification_pending', kwargs={'username': user.username}),
                        'message': 'Registration successful! Please check your email to verify your account.'
                    })
                    
                messages.success(request, 'Registration successful! Please check your email to verify your account.')
                return redirect('verification_pending', username=user.username)
            except Exception as e:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.headers.get('Accept') == 'application/json':
                    user.delete()
                    return JsonResponse({
                        'success': False,
                        'errors': {'__all__': ['Error sending verification email. Please try again.']}
                    })
                
                messages.error(request, 'Error sending verification email. Please try again.')
                user.delete()
                return redirect('register')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.headers.get('Accept') == 'application/json':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
    else:
        role = request.GET.get('role')
        initial_data = {}
        if role:
            initial_data['role'] = role
        form = CustomUserCreationForm(initial=initial_data)
    
    # Pass role explicitly for template conditional logic
    role_param = request.GET.get('role')
    return render(request, 'users/register.html', {'form': form, 'role_param': role_param})

def verify_email(request, token):
    """Verify user email with token"""
    try:
        user = User.objects.get(email_verification_token=token)
        if user.is_email_verified:
            messages.info(request, 'Email already verified. Please login.')
            return redirect('login')
        
        user.is_email_verified = True
        user.email_verification_token = None
        user.save()
        messages.success(request, 'Email verified successfully! You can now login.')
        return redirect('login')
    except User.DoesNotExist:
        messages.error(request, 'Invalid or expired verification link.')
        return redirect('login')

def verification_pending(request, username):
    """Show pending verification page"""
    try:
        user = User.objects.get(username=username)
        return render(request, 'users/verification_pending.html', {'user': user})
    except User.DoesNotExist:
        return redirect('register')


def resend_verification(request, username):
    """Resend verification email to the given user's registered email"""
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('register')

    try:
        send_verification_email(user, request)
        messages.success(request, f'Verification email resent to {user.email}.')
    except Exception as e:
        messages.error(request, 'Error resending verification email. Please try again.')

    return redirect('verification_pending', username=username)

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
            # Only require email verification for Startup and Founder roles
            if user.role in ['startup', 'founder'] and not user.is_email_verified:
                messages.error(request, 'Please verify your email before logging in. Check your inbox for the verification link.')
                return redirect('verification_pending', username=username)
        except User.DoesNotExist:
            pass  # Let the parent class handle invalid credentials
        
        return super().post(request, *args, **kwargs)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)
    
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
