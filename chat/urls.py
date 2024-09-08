from django.urls import path
from chat.views import conversations

urlpatterns = [
    path('chat/', conversations),
]
