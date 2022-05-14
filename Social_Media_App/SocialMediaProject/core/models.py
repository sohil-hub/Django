from email.policy import default
from django.db import models
from django.contrib.auth import get_user_model

USER = get_user_model()

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(to=USER, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to = 'profile_images', default = 'default-user-img.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username