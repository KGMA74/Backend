from django.shortcuts import render
from django.conf import settings
from django.db.models import Q
from api.models import (
    User, Profile, PostCategory, Post, 
    Tag, Vote, VoteType, Education, Experience
)
from api.serializers import (
    UserSerializer, ProfileSerializer, 
    PostCategorySerializer, PostSerializer, PostCreateSerializer, 
    TagSerializer, VoteSerializer, VoteTypeSerializer, EducationSerializer, ExperienceSerializer
)
from rest_framework import generics, status
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
                samesite=settings.AUTH_COOKIE_SAMESITE,
                domain=settings.AUTH_COOKIE_DOMAIN
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE,
                domain=settings.AUTH_COOKIE_DOMAIN
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
            samesite=settings.AUTH_COOKIE_SAMESITE,
            domain=settings.AUTH_COOKIE_DOMAIN
        )
        
        #un cookie pour le refresh token
        response.set_cookie(
            'refresh',
            refresh_token,
            max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
            secure=settings.AUTH_COOKIE_SECURE,
            httponly=settings.AUTH_COOKIE_HTTP_ONLY,
            path=settings.AUTH_COOKIE_PATH,
            samesite=settings.AUTH_COOKIE_SAMESITE,
            domain=settings.AUTH_COOKIE_DOMAIN
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
            print("Access token:", access_token)
            
            #on met a jour le access token
            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                path=settings.AUTH_COOKIE_PATH,
                samesite=settings.AUTH_COOKIE_SAMESITE,
                domain=settings.AUTH_COOKIE_DOMAIN
            )
            
        return response
    

class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')
        
        if access_token:
            request.data['token'] = access_token
            
        return super().post(request, *args, **kwargs)
    

    
@api_view(['POST'])
def LogoutView(request):
    if request.method == 'POST':
        
        # Supprimer les token en mettant leur valeur des cookies a ''
        response = Response(status=status.HTTP_204_NO_CONTENT)
        
        response.set_cookie(
            'refresh',
            value='',
            max_age=0,
            secure=settings.AUTH_COOKIE_SECURE,
            httponly=settings.AUTH_COOKIE_HTTP_ONLY,
            path=settings.AUTH_COOKIE_PATH,
            samesite=settings.AUTH_COOKIE_SAMESITE,
            domain=settings.AUTH_COOKIE_DOMAIN 
        )
        
        response.set_cookie(
            'access',
            value='',
            max_age=0,
            secure=settings.AUTH_COOKIE_SECURE,
            httponly=settings.AUTH_COOKIE_HTTP_ONLY,
            path=settings.AUTH_COOKIE_PATH,
            samesite=settings.AUTH_COOKIE_SAMESITE,
            domain=settings.AUTH_COOKIE_DOMAIN
        )

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
    lookup_field = 'pk'

@api_view(['GET'])
def PostList_byUser(request, id):
    if request.method == 'GET':
        votes = Post.objects.filter(Q(author=id) & ~Q(category='Comment'))
        serializer = PostSerializer(votes, many=True)
        
        return Response(data=serializer.data,
                        status=status.HTTP_202_ACCEPTED
                    )
    return Response("", status=status.HTTP_400_BAD_REQUEST)

class createPost(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    

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
    
class VoteTypeRetrieve(generics.RetrieveAPIView):
    queryset = VoteType.objects.all()
    serializer_class = VoteTypeSerializer
    lookup_field = 'id'
    
class vote(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    
class updateVote(generics.UpdateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    lookup_field = 'id'
    
class unvote(generics.DestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    lookup_field = 'id'
    
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
def comments_by_post(request, postId):
    if request.method == 'GET':
        try:
            comments = Post.objects.get(pk=postId).comments.all()
            serializer = PostSerializer(comments, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"{e}", status=status.HTTP_404_NOT_FOUND)
    return Response("", status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
# -------------------les tags
class tagsList(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer



@api_view(['GET'])
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

@api_view(['GET'])
@permission_classes([AllowAny])
def search(request):
    query = request.GET.get('q', '')  # Récupère la requête depuis le frontend
    
    if query:
        # Rechercher dans les utilisateurs
        users = User.objects.filter(Q(nickname__icontains=query) | Q(email__icontains=query))
        user_serializer = UserSerializer(users, many=True)
        
                
        # Récupérer les profils associés aux utilisateurs
        profiles = Profile.objects.filter(user__in=users)
        profile_serializer = ProfileSerializer(profiles, many=True)

        # Rechercher dans les tags
        tags = Tag.objects.filter(name__icontains=query)
        tag_serializer = TagSerializer(tags, many=True)

        # Rechercher dans les posts
        posts = Post.objects.filter(Q(title__icontains=query) | Q(details__icontains=query))
        post_serializer = PostSerializer(posts, many=True)

        return Response({
            'profiles': profile_serializer.data,
            'tags': tag_serializer.data,
            'posts': post_serializer.data,
        })
    
    return Response({'error': 'No query provided'}, status=400)

# -------------------------profile
class updateProfile(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
class profilesList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    
class createProfile(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
class retrieveProfile(generics.RetrieveAPIView):
    lookup_field = 'user'
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
#----------------------education

@api_view(['GET'])
def userEducation(request, userId):
    if request.method == 'GET':
        try:
            educations = Profile.objects.get(pk=userId).educations.all()
        except:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EducationSerializer(educations, many=True)
        print('*************************', serializer.data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    return Response('', status=status.HTTP_400_BAD_REQUEST)

class EducationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    lookup_field = 'pk'
    
#---------------------- experience
@api_view(['GET'])
def userExperience(request, userId):
    if request.method == 'GET':
        try:
            experiences = Profile.objects.get(pk=userId).experiences.all()
        except:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ExperienceSerializer(experiences, many=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    return Response('', status=status.HTTP_400_BAD_REQUEST)


class ExperienceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    lookup_field = 'pk'
    
#----------------skills

@api_view(['GET'])
def userSkills(request, userId):
    if request.method == 'GET':
        try:
           
            skills = Profile.objects.get(pk=userId).skills.all()
            serializer = TagSerializer(skills, many=True)
            print('*************************', serializer.data)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            print('*************************', serializer.data)
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response('', status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def addSkills(request, userId):
    try:
        profile = Profile.objects.get(pk=userId)
    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    skill_ids = request.data.get('skills', [])
    skills = Tag.objects.filter(id__in=skill_ids)
    profile.skills.add(*skills)
    
    serializer = TagSerializer(skills, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def removeSkills(request, userId):
    try:
        profile = Profile.objects.get(pk=userId)
    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    skill_ids = request.data.get('skills', [])
    skills = Tag.objects.filter(id__in=skill_ids)
    profile.skills.remove(*skills)
    
    return Response({'status': 'Skills removed'}, status=status.HTTP_200_OK)
