from django.urls import path
from chat.views import conversations, conversationsDetail

urlpatterns = [
    path('chat/', conversations),
    path('chat/<uuid:pk>/', conversationsDetail),
]
