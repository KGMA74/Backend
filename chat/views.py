from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from chat.models import Message, Conversation
from chat.serializers import MessageSerializer, ConversationSerializer

@api_view(['GET'])
def conversations(request):
    if request.method == 'GET':
        conversations = request.user.conversations.all()
        serializer = ConversationSerializer(conversations, many=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def conversationsDetail(request, pk):
    if request.method == 'GET':
        conversation = request.user.conversations.get(pk=pk)
        serializer = ConversationSerializer(conversation, many=False)
        
        messages = MessageSerializer(conversation.messages.all(), many=True)
        
        return Response(data={
            'conversation': serializer.data,
            'messages': messages.data
            }, status=status.HTTP_200_OK)
        
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)