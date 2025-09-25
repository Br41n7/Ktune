from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    quantity = forms.IntegerField(
        min_value=1,
        label="Number of Tickets",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'})
    )

    class Meta:
        model = Booking
        fields = ['quantity']
