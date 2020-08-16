from django.contrib import admin
from django.urls import path, include
from authorization import views

app_name='authorization'

urlpatterns = [    
    path('index/',views.index,name='index'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('register/',views.user_register,name='register'),
    #path('teacher-registration/',views.teacherRegistartion,name='teacher_register'),
    path('teacher-form/',views.teacher_form,name='teacher-form'),
    path('activity-page/',views.index,name='activity'),
    path('class_observation/',views.index,name='class_observation'),
    path('layout-static/',views.index,name='layout-static'),
    path('layout-sidenav-light/',views.index,name='layout-sidenav-light'),
    path('activity_page/',views.index,name='activity-page'),
    path('class-room-observation/',views.class_room_observation,name='class_room_observation'),
    path('charts/',views.index,name='charts'),
    path('tables/',views.index,name='tables'),
    path('401/',views.index,name='401'),
    path('404/',views.index,name='404'),
    path('500/',views.index,name='500'),
    
]

