""" Profile - BaseUserModel """
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import IntegerField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(blank=True, null=True)
    header_img = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=120, blank=True, null=True)
    rank = models.CharField(max_length=120, blank=True, null=True)
    level = IntegerField(blank=True, null=True)
    missions = IntegerField(blank=True, null=True)

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return self.user.get_full_name()