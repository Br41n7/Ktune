# from asyncio import events
from django.conf import Settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm,SettingsForm
from artist.forms import ArtistProfileForm
from django.contrib.auth.decorators import login_required
from artist.models import ArtistProfile
from reels.models import Reel
from events.models import Event

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    events=Event.objects.all().order_by('-created_at')[:5]
    reels=Reel.objects.order_by('-uploaded_at')[:5]
    return render(request, 'accounts/dashboard.html',{
        'events':events,
        'reels':reels
    })


@login_required
def settings_view(request):
    if request.method=='POST':
        form=SettingsForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
           form.save()
        return redirect('settings')
    else:
        form=SettingsForm(instance=request.user) 
    return render(request, 'accounts/settings.html')

@login_required
def migrate_to_host(request):
    if request.method=='POST':
       request.user.is_host=True
       request.user.save() 
    return redirect('settings')
