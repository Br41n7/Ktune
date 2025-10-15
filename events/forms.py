from django import forms
from .models import Event,EventTicket,Category,Venue,Artist
from django.forms.widgets import DateTimeInput

class EventSearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=False,
        label="Search Events",
        widget=forms.TextInput(attrs={'placeholder': 'Search by name, artist, or venue'})
    )



class EventForm(forms.ModelForm):
    new_artist = forms.CharField(required=False, label="New Artist")
    new_venue = forms.CharField(required=False, label="New Venue")
    new_category = forms.CharField(required=False, label="New Category")

    class Meta:
        model = Event
        fields = ['title', 'artist', 'venue', 'category', 'description', 'date', 'start_time', 'end_time', 'image']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['artist'].required=False #queryset = Artist.objects.all()
        self.fields['venue'].required=False #queryset = Venue.objects.all()
        self.fields['category'].required=False #queryset = Category.objects.all()

        self.fields['artist'].empty_label = "Select or type new below"
        self.fields['venue'].empty_label = "Select or type new below"
        self.fields['category'].empty_label = "Select or type new below"


    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('artist') and not cleaned_data.get('new_artist'):
            self.add_error('artist', "Select or type an artist")
        if not cleaned_data.get('venue') and not cleaned_data.get('new_venue'):
            self.add_error('venue', "Select or type a venue")
        if not cleaned_data.get('category') and not cleaned_data.get('new_category'):
            self.add_error('category', "Select or type a category")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Create new artist if needed
        new_artist = self.cleaned_data.get('new_artist')
        if new_artist:
            artist = Artist.objects.create(name=new_artist)
            instance.artist = artist

        new_venue = self.cleaned_data.get('new_venue')
        if new_venue:
            venue = Venue.objects.create(name=new_venue)
            instance.venue = venue 
            new_category = self.cleaned_data.get('new_category')
        if new_category:
            category = Category.objects.create(name=new_category)
            instance.category = category

        if commit:
            instance.save()
        return instance



class EventTicketForm(forms.ModelForm):
    class Meta:
        model = EventTicket
        fields = ['ticket_type', 'price', 'quantity']
        widgets = {
            'ticket_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
