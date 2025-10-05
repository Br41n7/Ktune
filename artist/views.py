from django.shortcuts import render,redirect,get_object_or_404
from .models import ArtistProfile #,Follow
from .forms import ArtistProfileForm
from django.contrib.auth.decorators import  login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from reels.models import Reel 
from events.models import Event  # adjust path as needed


# Create your views here.
User=get_user_model
@login_required
def artist_profile(request,username):
    profile=ArtistProfile.objects.get(user=request.user)
    artist=get_object_or_404(User,username=username)
    events=Event.objects.filter(host=artist)
    reels=Reel.objects.filter(user=artist)

    return render(request,'artist/artist_profile.html',
                  {'profile':profile,
                   'artist':artist,
                   'events':events,
                   'reels':reels,
                   })


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

def artist_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(ArtistProfile, user=user)
    reels = Reel.objects.filter(user=user).order_by('-created_at')
    is_following = False
    if request.user.is_authenticated:
        is_following = profile.followers.filter(id=request.user.id).exists()
    context = {
        'profile': profile,
        'reels': reels,
        'is_following': is_following,
    }
    return render(request, 'artist/profile.html', context)

@login_required
def follow_artist(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    profile = get_object_or_404(ArtistProfile, user=user_to_follow)

    if request.user != user_to_follow:
        if profile.followers.filter(id=request.user.id).exists():
            profile.followers.remove(request.user)
        else:
            profile.followers.add(request.user)
    return redirect('artist_profile', username=username)

# @login_required
# def follow_artist(request,artist_id):
#     artist=get_object_or_404(User,id=artist_id)
#     if request.user !=artist:
#         Follow.objects.get_or_create(follower=request.user,artist=artist)
#     return redirect('artist_profile',artist=artist.id)
#
# @login_required
# def unfollow_artist(request,artist_id):
#     Follow.objects.filter(follower=request.user,
#                           artist_id=artist_id).delete()
#     return redirect('artist_profile',artist_id=artist_id)
