from asyncio import events
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
        fields = ('quantity',)
        # fields = ('ticket', 'quantity')



    # def init(self,*args,**kwargs):
    #     event=kwargs.pop('events',None)
    #     super().init(*args,**kwargs)
    #     if events:
    #         self.fields['ticket'].queryset=events.tickets.
