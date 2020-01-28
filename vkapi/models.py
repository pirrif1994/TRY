from django.conf import settings
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    vk_id = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField()
    access_token = models.TextField()
