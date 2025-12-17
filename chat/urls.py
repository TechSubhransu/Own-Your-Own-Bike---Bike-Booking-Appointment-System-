from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('admin-chat/', views.admin_chat_view, name='admin_chat'),
]
