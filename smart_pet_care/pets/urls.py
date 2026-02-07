from django.urls import path
from . import views

urlpatterns = [
    # Public URLs
    path('', views.home, name='home'),
    path('pets/', views.pet_list, name='pet_list'),
    
    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # User Dashboard URLs
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('adopt/<int:pet_id>/', views.adopt_pet, name='adopt_pet'),
    path('adoption/cancel/<int:adoption_id>/', views.cancel_adoption, name='cancel_adoption'),
    
    # Reminder URLs
    path('reminders/', views.reminder_list, name='reminder_list'),
    path('reminder/add/', views.add_reminder, name='add_reminder'),
    path('reminder/edit/<int:reminder_id>/', views.edit_reminder, name='edit_reminder'),
    path('reminder/delete/<int:reminder_id>/', views.delete_reminder, name='delete_reminder'),
    
    # Chatbot URLs
    path('chatbot/', views.chatbot_view, name='chatbot'),
]