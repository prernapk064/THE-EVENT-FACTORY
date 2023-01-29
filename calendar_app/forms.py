from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from . import models
from django import forms
from django.forms import ModelForm , DateInput

User = get_user_model()


class SigninForm(UserCreationForm):
    class Meta:
       model = User
       fields = ['username','email','password1','password2']

class EventForm(ModelForm):
  class Meta:
    model = models.Event
    widgets = {
      'start_at': DateInput(format='%Y-%m-%dT%H:%M', attrs={'type' : 'datetime-local'}),
      'end_at': DateInput(format='%Y-%m-%dT%H:%M', attrs={'type' : 'datetime-local'})
    }
    exclude = ['creator', 'created_at']

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    #super() in multiple inheritance
    self.fields['start_at'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_at'].input_formats = ('%Y-%m-%dT%H:%M',)

class ProfileForm(ModelForm):
    class Meta:
        model = models.Profile
        fields = ['profession', 'email', 'profile_pic', 'contact']
