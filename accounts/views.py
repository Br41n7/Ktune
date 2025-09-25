from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)  # Add request param
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, "Invalid email or password")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_host = form.cleaned_data['is_host']
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard_view(request):
    return render(request,'accounts/dashboard.html')


def settings_view(request):
    if request.method=='POST':
        migrate=request.POST.get(migrate_to_host)
        if migrate=='yes' and not request.user.is_host:
            request.user.is_host=True
            request.user.save()
        return redirect('accounts:settings')
    return render(request,'accounts/settings')
