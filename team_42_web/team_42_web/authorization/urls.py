from django.contrib import admin
from django.urls import path, include
from authorization import views

app_name='authorization'

urlpatterns = [    
    path('index/',views.index,name='index'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('register/',views.user_register,name='register'),
    path('teacher-registration/',views.teacherRegistartion,name='teacher_register'),
]

