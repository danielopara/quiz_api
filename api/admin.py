from django.contrib import admin

from .models import AppUser, UserQuizProfile

# Register your models here.
admin.site.register(AppUser)
admin.site.register(UserQuizProfile)
