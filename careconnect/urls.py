from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    # 1. The Built-in Manager Admin Panel
    path('manager-hq/', admin.site.urls),

    # 2. Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 3. App Portals
    path('', views.dashboard, name='dashboard'),
    path('family/', views.family_portal, name='family_portal'),
    path('staff/', views.staff_portal, name='staff_portal'),
    path('dispatch/', views.admin_portal, name='admin_portal'),
    path('api/flutter/requests/', views.api_flutter_requests,name='api_flutter_requests'),
]