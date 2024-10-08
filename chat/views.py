from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from chat.models import Message, Conversation
from chat.serializers import MessageSerializer, ConversationSerializer, createConversationSerializer


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



@api_view(['POST'])
def createConversation(request):
    if request.method == 'POST':
        serializer = createConversationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['DELETE'])
def deleteConversation(request, pk):
    if request.method == 'DELETE':
        conversation = request.user.conversations.get(pk=pk)
        conversation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)