from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm
from artist.forms import ArtistProfileForm
from django.contrib.auth.decorators import login_required
from artist.models import ArtistProfile
from reels.models import Reel

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
    reels=Reel.objects.order_by('-created_at')[:10]
    return render(request, 'accounts/dashboard.html')


@login_required
def settings_view(request):
    if request.method == 'POST':
        migrate = request.POST.get('migrate_to_host')
        if migrate == 'yes' and not request.user.is_host:
            request.user.is_host = True
            request.user.save()
        return redirect('settings')
    return render(request, 'accounts/settings.html')

