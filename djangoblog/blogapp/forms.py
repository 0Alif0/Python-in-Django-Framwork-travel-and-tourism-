from django import forms
from .models import article, author, category, comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class createForm(forms.ModelForm):
    class Meta:
        model = article
        fields = [
            'title',
            'body',
            'image',
            'category'
        ]


class registerUser(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2'
        ]


class createAuthor(forms.ModelForm):
    class Meta:
        model = author
        fields = [
            'profile_picture',
            'details'
        ]


class categoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields = [
            'name'
        ]

class commentForm(forms.ModelForm):
    class Meta:
        model = comment
        fields = [
            'name',
            'email',
            'post_comment'
        ]
