from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FounderNeed, CollabRequest
from .forms import FounderNeedForm, CollabRequestForm

@login_required
def feed(request):
    if not request.user.is_founder():
        return redirect('login')
        
    needs = FounderNeed.objects.filter(status='OPEN').exclude(founder=request.user).order_by('-created_at')
    
    context = {
        'needs': needs
    }
    return render(request, 'founder_feed.html', context)

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
            return redirect('founder_feed')
    else:
        form = CollabRequestForm()
    return render(request, 'form_generic.html', {'form': form, 'title': f'Contact {need.founder.username}'})
