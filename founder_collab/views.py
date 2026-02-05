from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FounderNeed, CollabRequest
from .forms import FounderNeedForm, CollabRequestForm

@login_required
def feed(request):
    if not request.user.is_founder():
        return redirect('login')
        
    # Phase 4 - Trust Check
    is_verified = False
    if hasattr(request.user, 'startup_profile'):
        is_verified = request.user.startup_profile.is_verified
    
    # Fetch all founder needs from the network
    needs = FounderNeed.objects.all().select_related('founder').prefetch_related('requests')
    
    context = {
        'needs': needs,
        'is_verified': is_verified,
    }
    return render(request, 'founder_collab/founder_feed.html', context)


@login_required
def post_need(request):
    if not request.user.is_founder():
        return redirect('login')
        
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

@login_required
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

@login_required
def manage_requests(request):
    if not request.user.is_founder():
        return redirect('login')
        
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
