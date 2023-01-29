from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Event(models.Model):
    creator = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 100, unique = True , null = False)
    about = models.TextField()
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    created_at = models.DateTimeField(default = datetime.now)

    def __str__(self):
        return f'{self.title} conducted by {self.creator}'

    def get_absolute_url(self):
        return reverse('calendar_app:eventinfo', kwargs={"pk":self.pk})

    @property
    def event_url(self):
        return '{}'.format(reverse('calendar_app:eventinfo', kwargs={"pk":self.pk}))


class Profile(models.Model):
    user_name = models.ForeignKey(User, on_delete = models.CASCADE)
    profession = models.TextField(max_length = 300, blank = True, null = False)
    email = models.EmailField(blank = False)
    profile_pic = models.ImageField(upload_to = 'profile', null = True, default = 'default.jpg')
    contact = models.BigIntegerField(null = True, default = '0000000000')

    def __str__(self):
        return f'{"@"}' + f'{self.user_name.username}'

    def get_absolute_url(self):
        return reverse('profiledetail', kwargs={'pk' : self.pk})

class EventMembers(models.Model):
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    member = models.ForeignKey(User, on_delete = models.CASCADE)

    class Meta:
      unique_together = ['event', 'member']

    def __str__(self):
        return f'{self.member}'
