from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.user_logout, name='user_logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('password_change/', views.password_change, name='password_change'),
]