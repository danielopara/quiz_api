from django.contrib import admin

from .models import AppUser, Question, UserQuizProfile

# Register your models here.
admin.site.register(AppUser)
admin.site.register(UserQuizProfile)
admin.site.register(Question)
