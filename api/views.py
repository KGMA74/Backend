from django.shortcuts import render
from django.conf import settings
from django.db.models import Q
from api.models import (
    User, Profile, PostCategory, Post, 
    Tag, Vote, VoteType, Message
)
from api.serializers import (
    UserSerializer, ProfileSerializer, 
    PostCategorySerializer, PostSerializer, 
    TagSerializer, VoteSerializer, VoteTypeSerializer,
    MessageSerializer
)
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from djoser.social.views import ProviderAuthView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .utils import (
    Post_votes_nbr,
    count_total_comments
)

from django.contrib.auth import login 

# Create your views here..
class CustomProviderAuthView(ProviderAuthView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 201:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response
#customisation de la class TokenObtainPairView pour que les tokens passes par les cookies et non les headers donc plus securise
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        print(response)
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
@permission_classes([AllowAny])
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
    
class PostList(generics.ListAPIView):
    """
    Vue pour lister tous les posts principaux (excluant les commentaires).
    """
    queryset = Post.objects.filter(~Q(category='Comment'))  # Exclure les commentaires
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    
class PostRetrieve(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'

@api_view(['GET'])
def PostList_byUser(request, id):
    if request.method == 'GET':
        votes = Post.objects.filter(author=id)
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
def VoteList_byPost(request, postId, vote_type="all"):
    # all for  both upvote and downvote
    if request.method == 'GET':
        
        upvotes, downvotes =  Post_votes_nbr(postId)

        #useless
        if vote_type != "all":
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
    
#le vote d'un utilisareur dans un post
@api_view(['GET'])
@permission_classes([AllowAny])
def vote_of_user_in_post(request, postId, userId):
    if request.method == 'GET':
        try:
            vote = Vote.objects.get(author=userId, post=postId)
            serializer = VoteSerializer(vote, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_404_NOT_FOUND)
    return Response("", status=status.HTTP_405_METHOD_NOT_ALLOWED)

#nombre de commentaire d un post (qui son egalement des post de categories commentaire)
@api_view(['GET'])
@permission_classes([AllowAny])
def comments_by_post_number(request, postId):
    #nombre de commentaire dun post
    if request.method == 'GET':
        try:
            return Response(data={'totalComments': count_total_comments(post_id=postId)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_404_NOT_FOUND)
    return Response("", status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
#-----------------*--les commentaires
@api_view(['GET'])
@permission_classes([AllowAny])
def comments_by_post(request, postId):
    if request.method == 'GET':
        try:
            comments = Post.objects.filter(parent_post_id=postId)
            serializer = PostSerializer(comments, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_404_NOT_FOUND)
    return Response("", status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
# -------------------les tags
class tagsList(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]



@api_view(['GET'])
@permission_classes([AllowAny])
def tags_by_post(request, postId):
    #recuperer les tags dun post des donnes
    if request.method == 'GET':
        try:
            tags = Post.objects.get(id=postId).tags.all()
            serialier = TagSerializer(tags, many=True)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_404_NOT_FOUND)
        return Response(data=serialier.data, status=status.HTTP_200_OK)
    
    return Response("", status=status.HTTP_405_METHOD_NOT_ALLOWED)

#categories de post
class categoriesList(generics.ListAPIView):
    queryset = PostCategory.objects.all()
    serializer_class = PostCategorySerializer
    permission_classes = [AllowAny]

@api_view(['GET'])
class SearchUserView(APIView):
    def get(self, request):
        search_term = request.query_params.get('search')
        matches = User.objects.filter(
            Q(nickname_icontains=search_term) |
            Q(email_icontains=search_term)
        ).distinct()