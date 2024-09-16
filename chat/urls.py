from django.urls import path
from chat.views import conversations, conversationsDetail, createConversation

urlpatterns = [
    path('chat/', conversations),
    path('chat/create/', createConversation),
    path('chat/<uuid:pk>/', conversationsDetail),
]
