from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ReelForm
from .models import Reel

@login_required
def upload_reel(request):
    if request.method == 'POST':
        form = ReelForm(request.POST, request.FILES)
        if form.is_valid():
            reel = form.save(commit=False)
            reel.artist = request.user
            reel.save()
            return redirect('reel_list')
    else:
        form = ReelForm()
    return render(request, 'reels/upload_reel.html', {'form': form})

def reel_list(request):
    reels = Reel.objects.all().order_by('-created_at')
    return render(request, 'reels/reel_list.html', {'reels': reels})
