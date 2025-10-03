from django import forms
from .models import ArtistProfile

class ArtistProfileForm(forms.Form):
    class Meta:
        model=ArtistProfile
        fields=['stage_name','bio','genre','profile_picture','instagram','youtube','twitter']
