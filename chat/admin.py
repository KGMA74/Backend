from django.contrib import admin
from chat.models import Message, Conversation

admin.site.register([
    Message,
    Conversation,
])