from django.db import models
from calendar_app.models import *
from django.contrib.auth.models import User
from django.shortcuts import reverse
# Create your models here.


class Group(models.Model):
    creator = models.ForeignKey(User, on_delete = models.CASCADE)
    group_name = models.CharField(max_length = 100, blank = False)
    slug = models.SlugField(unique = False , null = True)
    about = models.TextField(blank = False, default = "Vision")

    def save(self, *args, **kwargs):
        self.slug = self.group_name
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("group:groupdetail", kwargs={"pk" : self.pk})

    def __str__(self):
        return self.group_name



class GroupMembers(models.Model):
    group = models.ForeignKey(Group, on_delete = models.CASCADE)
    member_name = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.member_name.username
