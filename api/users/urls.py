from django.urls import path

from .views import UserView

urlpatterns = [
    path('register', UserView.register),
    
    path('login', UserView.login),
    
    path('user_profile', UserView.get_user_profile)
]
