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
    
    def __str__(self):
        return self.usr_id.email
    
    
# class UserQuestionHistory(models.Model):
#     profile = models.ForeignKey(UserQuizProfile, on_delete=models.CASCADE)
#     quiz_id = models.IntegerField()
#     success_count = models.IntegerField()
#     loss_count = models.IntegerField()
    
    
class Question(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D','D')])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question
    