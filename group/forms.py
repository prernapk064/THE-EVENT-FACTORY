from django import forms
from .models import *


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_name', 'about']

class GroupMember(forms.ModelForm):
    class Meta:
        model = GroupMembers
        fields = '__all__'
