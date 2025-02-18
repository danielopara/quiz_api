from django.urls import path

from .views import QuestionView

urlpatterns = [
    path('create_question', QuestionView.create_question)
]
