from django import forms
from .models import Event

class EventSearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=False,
        label="Search Events",
        widget=forms.TextInput(attrs={'placeholder': 'Search by name, artist, or venue'})
    )

class EventForm(forms.ModelForm):
    class Meta:
        model=Event
        fields=['name','artist','venue','category','start_time','end_time','description','image']

    
