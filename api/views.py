from django.shortcuts import render
from django.conf import settings
from api.models import (
    User, Profile, PostCategory, Post, 
    Tag, Vote, VoteType, Comment,  Message
)
from api.serializers import (
    UserSerializer, ProfileSerializer, 
    PostCategorySerializer, PostSerializer, 
    TagSerializer, VoteSerializer, VoteTypeSerializer,
    CommentSerializer, MessageSerializer
)
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


# Create your views here.
#customisation de la class TokenObtainPairView pour que les tokens passes par les cookies et non les headers donc plus securise
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            
            
        #un cookie pour le access token
        response.set_cookie(
            'access',
            access_token,
            max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
            secure=settings.AUTH_COOKIE_SECURE,
            httponly=settings.AUTH_COOKIE_HTTP_ONLY,
            path=settings.AUTH_COOKIE_PATH,
            samesite=settings.AUTH_COOKIE_SAMESITE
        )
        
        #un cookie pour le refresh token
        response.set_cookie(
            'refresh',
            refresh_token,
            max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
            secure=settings.AUTH_COOKIE_SECURE,
            httponly=settings.AUTH_COOKIE_HTTP_ONLY,
            path=settings.AUTH_COOKIE_PATH,
            samesite=settings.AUTH_COOKIE_SAMESITE
        )
            
        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs) :
        refresh_token = request.COOKIES.get('refresh')
        
        if refresh_token:
            #si le token refresh dans le la list des cookies
            request.data['refresh'] = refresh_token
            
        response =  super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data.get('access')
            
            #on met a jour le access token
            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                path=settings.AUTH_COOKIE_PATH,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            
        return response
    

class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')
        
        if access_token:
            request.data['token'] = access_token
            
        return super().post(request, *args, **kwargs)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def LogoutView(request):
    if request.method == 'POST':
        response = Response(status=status.HTTP_204_NO_CONTENT)
        
        #on supprime les cookies access et refresh
        response.delete_cookie('access')
        response.delete_cookie('refresh') 
        
        return response
     
    return Response("", status=status.HTTP_405_METHOD_NOT_ALLOWED)    
    
#user management
#[!] -----------------------------plus necessaire
'''
class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
'''

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserRetrieve(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    
#[!] ----------------------------plusnecessaire
    
#class Post
class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    
class PostRetrieve(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'

@api_view(['GET'])
def PostList_byUser(request, id):
    if request.method == 'GET':
        votes = Post.objects.filter(owner=id)
        serializer = PostSerializer(votes, many=True)
        
        return Response(data=serializer.data,
                        status=status.HTTP_202_ACCEPTED
                    )
    return Response("", status=status.HTTP_400_BAD_REQUEST)

class createPost(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

#----------------------------------------vote
@api_view(['GET'])
@permission_classes([AllowAny])
def VoteList_byPost(request, postId, vote_type="-1"):
    # -1 mean all_type for us both upvote
    if request.method == 'GET':
        votes = Vote.objects.filter(post=postId)
        upvotes = votes.filter(type=1).count()
        downvotes = votes.filter(type=2).count()
        
        if vote_type != "-1":
            votes = votes.filter(type=vote_type)
        
        return Response(data={'upvotes': upvotes, 'downvotes': downvotes},
                        status=status.HTTP_202_ACCEPTED
                    )
    return Response("", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def VoteList_byVoteType(request, vote_type):
    if request.method == 'GET':
        votes = Vote.objects.filter(type=vote_type)
        serializer = VoteSerializer(votes, many=True)
        
        return Response(data=serializer.data,
                        status=status.HTTP_202_ACCEPTED
                    )
    return Response("", status=status.HTTP_400_BAD_REQUEST)
    
class VoteList(generics.ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [AllowAny]
    
class VoteTypeRetrieve(generics.RetrieveAPIView):
    queryset = VoteType.objects.all()
    serializer_class = VoteTypeSerializer
    lookup_field = 'id'
    permission_classes = [AllowAny]
    
class vote(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [AllowAny]
    
class updateVote(generics.UpdateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    lookup_field = 'id'
    permission_classes = [AllowAny]
    
class unvote(generics.DestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    lookup_field = 'id'
    permission_classes = [AllowAny]
    
#-----------------*--les commentaires
@api_view(['GET'])
@permission_classes([AllowAny])
def comments_by_post(request, postId):
    if request.method == 'GET':
        try:
            comments = Comment.objects.filter(post=postId)
            serializer = CommentSerializer(comments, many=True)
        except Exception as e:
            return Response("{e}", status=status.HTTP_404_NOT_FOUND)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    return Response("", status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
# -------------------les tags
@api_view(['GET'])
@permission_classes([AllowAny])
def tags_by_post(request, postId):
    if request.method == 'GET':
        try:
            tags = Post.objects.get(id=postId).tags.all()
            serialier = TagSerializer(tags, many=True)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_404_NOT_FOUND)
        return Response(data=serialier.data, status=status.HTTP_200_OK)
    
    return Response("", status=status.HTTP_405_METHOD_NOT_ALLOWED)