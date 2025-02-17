from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class AppUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.email
    
    
class UserQuizProfile(models.Model):
    usr_id = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    games_amount = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    games_lost = models.IntegerField(default=0)
    
    