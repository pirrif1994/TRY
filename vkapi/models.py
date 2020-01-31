from django.conf import settings
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    vk_id = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField()
    access_token = models.TextField()
    id = models.TextField(primary_key=True)

    def __str__(self):
        string = self.first_name+" "+self.last_name
        return string