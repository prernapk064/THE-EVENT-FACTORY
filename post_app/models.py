from django.db import models
from django.contrib.auth.models import User
from calendar_app.models import Event
from django.shortcuts import reverse
from datetime import datetime
# Create your models here.

class Post(models.Model):
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    post = models.TextField(blank = False)
    post_at = models.DateTimeField(default = datetime.now)

    def __str__(self):
        return 'Create_Post'

    def get_absolute_url(self):
        return reverse('post_app:post', kwargs={'pk' : self.event.pk})

    class Meta:
        ordering = ["-post_at"]
