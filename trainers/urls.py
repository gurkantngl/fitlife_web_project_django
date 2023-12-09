from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.trainerPanel, name="trainerPanel"),
    path('updateProfile/<str:trainer_id>/', views.updateProfile, name="updateProfile"),
    path('updateExpert/<str:trainer_id>/', views.updateExpert, name="updateExpert"),
    path('sendMessage/<str:trainer_username>/', views.sendMessage, name="sendMessage"),
    path('addNutritionProgram/<str:client_id>/', views.addNutritionProgram, name="addNutritionProgram"),
    path('saveNutritionProgram/<str:client_id>/', views.saveNutritionProgram, name="saveNutritionProgram"),
    path('viewNutritionProgram/<str:client_id>/', views.viewNutritionProgram, name="viewNutritionProgram"),
    path('addExerciseProgram/<str:client_id>/', views.addExerciseProgram, name="addExerciseProgram"),
    path('saveExerciseProgram/<str:client_id>/', views.saveExerciseProgram, name="saveExerciseProgram"),
    path('viewExerciseProgram/<str:client_id>/', views.viewExerciseProgram, name="viewExerciseProgram"),
    path('deleteExerciseProgram/<str:client_id>/', views.deleteExerciseProgram, name="deleteExerciseProgram"),
    path('deleteNutritionProgram/<str:client_id>/', views.deleteNutritionProgram, name="deleteNutritionProgram"),
]