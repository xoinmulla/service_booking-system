from django.urls import path
from . import views

urlpatterns = [
        path('', views.home_view, name='home'),  # Add this line to handle the root URL

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    
    # User actions
    path('dashboard/user/', views.user_dashboard, name='user_dashboard'),
    path('book/<int:worker_id>/', views.book_worker, name='book_worker'),
    path('feedback/<int:booking_id>/', views.give_feedback, name='give_feedback'),
    
    # Worker actions
    path('dashboard/worker/', views.worker_dashboard, name='worker_dashboard'),
    path('create-profile/', views.create_worker_profile, name='create_worker_profile'),
    path('accept-booking/<int:booking_id>/', views.accept_booking, name='accept_booking'),
    path('view-feedback/', views.view_feedback, name='view_feedback'),

    # Admin actions
    path('register/dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-services/', views.manage_services, name='manage_services'),
    path('manage-locations/', views.manage_locations, name='manage_locations'),
    path('approve-users/', views.proceed_user_registration, name='proceed_user_registration'),
]
