from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', views.loginPanelAdmin, name="loginAdmin"),
    path('trainer/', views.loginPanelTrainer, name="loginTrainer"),
    path('user/forgetpassword/', views.forgetpassword, name="forgetpassword"),
    path('user/confirmcode/', views.confirmcode, name="confirmcode"),
    path('user/change-password/', views.changepassword, name="changepassword"),
    path('user/register/', views.registerpanel, name="registerpanel"),
    path('user/', views.loginPanelUser, name="loginUser"),
]
