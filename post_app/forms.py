from .models import Post
from django import forms
from django.forms import ModelForm


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['post']
