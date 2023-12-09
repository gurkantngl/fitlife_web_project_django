from django.contrib import admin
from django.urls import path, include
from users import views


urlpatterns = [
    path('', views.userPanel, name="userPanel"),
    path('update/<str:user_id>/', views.update, name="update"),
    path('sendMessageUser/<str:user_id>/', views.sendMessageUser, name="sendMessageUser"),
    path('viewExerciseProgramUser/<str:client_id>/', views.viewExerciseProgramUser, name="viewExerciseProgramUser"),
    path('updateInfo/<str:client_id>/', views.updateInfo, name="updateInfo"),
    path('viewNutritionProgramUser/<str:client_id>/', views.viewNutritionProgramUser, name="viewNutritionProgramUser"),
    path('updateExerciseProgram/<str:client_id>/<int:gun_sayisi>/', views.updateExerciseProgram, name="updateExerciseProgram"),
]