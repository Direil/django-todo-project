from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('login/',  auth_views.LoginView.as_view(template_name='profile/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='list'), name='logout'),
    path('register/', views.register_user, name='register'),
]
