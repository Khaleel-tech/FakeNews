from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class NewsInputForm(forms.Form):
    headline = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Enter a short headline'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, 'placeholder': 'Paste the full news content here...'}))
