from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.adminPanel, name="adminPanel"),
    path('users/', views.users, name="users"),
    path('trainers/', views.trainers, name="trainers"),
    path('userActivePassive/<str:user_email>/', views.userActivePassive, name="userActivePassive"),
    path('trainerActivePassive/<str:trainer_email>/', views.trainerActivePassive, name="trainerActivePassive"),
    path('userUpdate/<str:user_id>/', views.userUpdate, name="userUpdate"),
    path('trainerUpdate/<str:trainer_id>/', views.trainerUpdate, name="trainerUpdate"),
]