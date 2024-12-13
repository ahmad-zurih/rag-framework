from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('chat/', views.chat_page, name='chat'),
    path('chat/stream/', views.chat_stream, name='chat_stream'),
]
