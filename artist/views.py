from django.shortcuts import render,redirect
from .models import ArtistProfile
from .forms import ArtistProfileForm
from django.contrib.auth.decorators import  login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from reels.models import Reel 
from events.models import Event  # adjust path as needed


# Create your views here.
User=get_user_model
@login_required
def artist_profile(request):
    profile=ArtistProfile.objects.get(user=request.user)
    return render(request,'artist/artist_profile.html',{'profile':profile})


@login_required
def edit_artist_profile(request):
    profile,created=ArtistProfile.objects.get_or_create(user=request.user)
    if request.method=='POST':
        form=ArtistProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('artist_profile')
    else:
        form=ArtistProfileForm(instance=profile)
    return render(request,'artist/edit_artist_profile.html',{'form':form})




def artist_list(request):
    artists = User.objects.filter(
        Q(reels_isnull=False) | Q(event_isnull=False)
    ).distinct()
    return render(request, 'artists/artist_list.html', {'artists': artists})

def artist_detail(request, artist_id):
    artist = get_object_or_404(User, id=artist_id)
    events = Event.objects.filter(creator=artist)
    reels = Reel.objects.filter(artist=artist)
    return render(request, 'artists/artist_detail.html', {
        'artist': artist,
        'events': events,
        'reels': reels
    })
