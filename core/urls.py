# from .views import UserViewSet, ChatViewSet, MessageViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import *

# router = DefaultRouter()
# router.register(r'user', UserViewSet, basename='user')
# router.register(r'chat', ChatViewSet, basename='chat')
# router.register(r'message', MessageViewSet, basename='message')

# urlpatterns = router.urls
urlpatterns = [
    path('', chats_view, name='chats'),
    path('user/', list_users, name='users'),
    path('user/<str:username>', user_info, name='user'),
    path('chat/<int:pk>', chat_info, name='chat'),
    path('message/', send_message, name='message'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
]
