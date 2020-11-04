from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class MessagePostForm(forms.Form):
    content = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={
                                                                            'class': 'form-control',
                                                                            'rows': 1,
                                                                            'id': 'textarea-input'}))

