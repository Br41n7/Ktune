from django.shortcuts import render
from .forms import ContactForm

def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # TODO: Process email here
            return render(request, 'home.html', {
                'form': ContactForm(),  # reset form
                'success': True
            })
    else:
        form = ContactForm()
        
    return render(request, 'home.html', {'form': form})
