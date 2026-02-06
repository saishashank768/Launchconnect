from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import FounderNeed, CollabRequest
from .forms import FounderNeedForm, CollabRequestForm

def founder_required(view_func):
    """Decorator to check if user is a founder"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_founder():
            return HttpResponseForbidden("You don't have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper

@founder_required
def feed(request):
    # Phase 4 - Trust Check
    is_verified = False
    if hasattr(request.user, 'startup_profile'):
        is_verified = request.user.startup_profile.is_verified
    
    # Check email verification status
    email_verified = request.user.is_email_verified
    
    # Fetch all founder needs from the network
    needs = FounderNeed.objects.all().select_related('founder').prefetch_related('requests')
    
    context = {
        'needs': needs,
        'is_verified': is_verified,
        'email_verified': email_verified,
    }
    return render(request, 'founder_collab/founder_feed.html', context)


@founder_required
def post_need(request):
    # Check email verification for founders
    if not request.user.is_email_verified:
        from django.contrib import messages
        messages.error(request, 'Please verify your email address before posting collaboration needs.')
        return redirect('verification_pending', username=request.user.username)
        
    if request.method == 'POST':
        form = FounderNeedForm(request.POST)
        if form.is_valid():
            need = form.save(commit=False)
            need.founder = request.user
            need.save()
            return redirect('founder_feed')
    else:
        form = FounderNeedForm()
    return render(request, 'form_generic.html', {'form': form, 'title': 'Post Collaboration Need'})

@founder_required
def send_request(request, need_id):
    need = get_object_or_404(FounderNeed, id=need_id)
    if request.method == 'POST':
        form = CollabRequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.need = need
            req.sender = request.user
            req.save()
            
            # Phase 5 - Notification
            from users.models import Notification
            Notification.objects.create(
                user=need.founder,
                title="New Collab Request",
                message=f"{request.user.username} wants to collaborate on: {need.title}",
                link="/founder-collab/manage-requests/"
            )
            return redirect('founder_feed')
    else:
        form = CollabRequestForm()
    return render(request, 'form_generic.html', {'form': form, 'title': f'Contact {need.founder.username}'})

@founder_required
def manage_requests(request):
    # Only show needs belonging to the current founder
    needs = FounderNeed.objects.filter(founder=request.user).prefetch_related('requests', 'requests__sender')
    
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action') # ACCEPT or DECLINE
        collab_req = get_object_or_404(CollabRequest, id=request_id, need__founder=request.user)
        
        if action == 'ACCEPT':
            collab_req.status = 'ACCEPTED'
            # Notify sender
            from users.models import Notification
            Notification.objects.create(
                user=collab_req.sender,
                title="Collab Request Accepted!",
                message=f"{request.user.username} accepted your collaboration request for {collab_req.need.title}",
                link="/founder-collab/"
            )
        elif action == 'DECLINE':
            collab_req.status = 'DECLINED'
            
        collab_req.save()
        return redirect('founder_manage_requests')
        
    return render(request, 'founder_collab/manage_requests.html', {'needs': needs})
