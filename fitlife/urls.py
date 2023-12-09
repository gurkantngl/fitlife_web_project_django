from django.contrib import admin
from django.urls import path, include
from login import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('login/', include("login.urls")),
    path('user/', include("users.urls")),
    path('adminPanel/', include("adminPanel.urls")),
    path('trainer/', include("trainers.urls")),
]
