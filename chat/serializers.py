from chat.models import Message, Conversation
from api.serializers import UserSerializer
from rest_framework import serializers

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        

class ConversationSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = '__all__'