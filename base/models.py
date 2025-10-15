from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Topic (models.Model):
    name = models.CharField(max_length= 100)
    
    def __str__(self):
        return self.name
    

class Room (models.Model):
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.SET_NULL, null = True, blank = True)
    topic = models.ForeignKey(Topic, on_delete = models.SET_NULL, null = True ,blank = True)
    name = models.CharField(max_length= 100)
    description = models.TextField(null = True, blank = True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.name
    
class Message (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    room = models.ForeignKey(Room, on_delete = models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.body[0:50]
    

class UserAccount(AbstractUser):
    phone = models.CharField(max_length = 20, blank = True)
    address = models.CharField(max_length = 250, blank = True)
    postcode = models.CharField(blank = True)
    birthday = models.DateField(null = True, blank = True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.username}"
