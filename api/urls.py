from django.urls import path
import djoser.email
from api.views import (UserList, PostList, VoteList, VoteList_byVoteType, VoteList_byPost,
    VoteTypeRetrieve, UserRetrieve, 
    PostList_byUser, createPost, vote, unvote,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    LogoutView
    )

urlpatterns = [
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    path('logout/', LogoutView),
    
    
    #path('users/', UserList.as_view()), #a modifier
    #path('users/register/', UserRegister.as_view()),
    #path('users/<str:id>/', UserRetrieve.as_view()),
    #path('users/<str:id>/posts/', PostList_byUser),
    #path('users/<str:id>/posts/create/', createPost.as_view()),

    
    path('posts/', PostList.as_view()),
    path('posts/<str:post>/votes/', VoteList_byPost),
    path('posts/create/', createPost.as_view()),
    
    path('votes/', VoteList.as_view()),
    path('votes/<str:vote_type>/', VoteList_byVoteType),
    path('vote/', vote.as_view()),
    path('unvote/<str:id>/', unvote.as_view()),
    
    
    path('vote-type/<str:id>/', VoteTypeRetrieve.as_view())
]
