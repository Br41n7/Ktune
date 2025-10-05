from django import forms
from artist.models import User,ArtistProfile

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    is_host = forms.BooleanField(required=False, label="Register as Host")

    class Meta:
        model = User
        fields = ('username', 'email', 'is_host')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')

        if password and confirm and password != confirm:
            self.add_error('confirm_password', "Passwords do not match")

class SettingsForm(forms.Form):
    class Meta:
        model=User
        fields=['profile_image','username','email','notify_on_event']
