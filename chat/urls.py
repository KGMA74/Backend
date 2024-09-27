from django.urls import path
from chat.views import conversations, conversationsDetail, createConversation, deleteConversation

urlpatterns = [
    path('chat/', conversations),
    path('chat/create/', createConversation),
    path('chat/<uuid:pk>/', conversationsDetail),
     path('chat/<uuid:pk>/delete/', deleteConversation),
]
