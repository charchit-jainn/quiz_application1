from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("register/", views.register, name="register"),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('result/<int:quiz_id>/', views.result, name='result'),
    path("leaderboard/<int:quiz_id>/", views.leaderboard, name="leaderboard"),
]
