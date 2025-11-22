from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path('manager-hq/', admin.site.urls),
    
    # Auth (Web)
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),

    # Web Portals
    path('', views.dashboard, name='dashboard'),
    path('family/', views.family_portal, name='family_portal'),
    path('staff/', views.staff_portal, name='staff_portal'),
    path('dispatch/', views.admin_portal, name='admin_portal'),

    # Mobile API
    path('api/login/', views.api_login),
    path('api/family/', views.api_family_requests),
    path('api/staff/', views.api_staff_requests),
    # Legacy support for older Flutter test
    path('api/flutter/requests/', views.api_staff_requests),
]