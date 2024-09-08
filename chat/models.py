from django.db import models
import uuid
from api.models import User

# Create your models here.

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='conversations')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    body = models.TextField()
    sent_to = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.author.nickname} sent [{self.body}] to {self.sent_to.nickname}'