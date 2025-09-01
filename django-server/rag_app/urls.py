from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_view, name='search'),
    path('chat/', views.chat_view, name='chat'),
    path('search_documents/', views.search_documents, name='search_documents'),
    path('chat_stream/', views.chat_stream, name='chat_stream'),
    path('api/chat/', views.chat_api, name='chat_api'),  # New API endpoint
]
