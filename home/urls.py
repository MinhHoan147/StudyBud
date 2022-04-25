from . import views
from django.urls import path



app_name = 'home'
urlpatterns = [
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('register/',views.user_register,name='register'),

    path('',views.home, name='home'),
    path('room/<str:pk>/',views.room, name='room'),
    path('create_room/', views.create_room, name='create-room'),
    path('update_room/<str:pk>/', views.update_room, name='update-room'),
    path('delete_room/<str:pk>/', views.delete_room, name='delete-room'),

    path('delete_message/<str:pk>/', views.delete_message, name='delete-message'),
    path('update_message/<str:pk>/', views.update_message, name='update-message'),

    path('user_profile/<str:pk>/', views.user_profile, name='user-profile'),
    path('update-user/', views.update_user, name='update-user'),

    path('topics/', views.topic_page, name='topics'),
    path('activities/', views.activity_page, name='activities'),

]