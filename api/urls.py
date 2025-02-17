from django.urls import include, path

urlpatterns = [
    # users
    path('users/', include('api.users.urls'))
]
