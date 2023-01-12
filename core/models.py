from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

# model of the currently logged in user
User = get_user_model()

# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(
        upload_to="profile_images", default="default_user.jpg")
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user


class Member(models.Model):

    name = models.CharField(max_length=50, default='john')
    phone = models.IntegerField(default=22222222)
    creation_date = models.DateField(default=datetime.today)
    email = models.EmailField(default='john@g.com')
    key_issue = models.CharField(
        max_length=2000, default='Det her betyder noget for mig')
    birth_year = models.IntegerField(default=1994)
    zip_code = models.IntegerField(default=2100)
    engagement_score = models.IntegerField(default=100)

    def __str__(self):
        return self.name
