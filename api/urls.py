from django.urls import path
import djoser.email
from api.views import (
    UserList, PostList, VoteList, PostRetrieve,
    VoteList_byVoteType, VoteList_byPost, tags_by_post, comments_by_post, comments_by_post_number,userExperience, ExperienceDetail,
    userEducation, EducationDetail, addSkills, removeSkills, userSkills,
    vote_of_user_in_post, tagsList, categoriesList, createProfile, retrieveProfile, profilesList, updateProfile,
    VoteTypeRetrieve, UserRetrieve, 
    PostList_byUser, createPost, vote, unvote, updateVote, search,
    
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    LogoutView,
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
    path('post/<str:pk>/', PostRetrieve.as_view()),
    path('user-posts/<str:id>/', PostList_byUser),
    path('posts/<str:postId>/votes/<str:vote_type>/', VoteList_byPost), #a change
    path('posts/create/', createPost.as_view()),
    path('posts/<str:postId>/tags/', tags_by_post),
    path('posts/<str:postId>/comments_number/', comments_by_post_number),
    path('posts/<str:postId>/comments/', comments_by_post),
    path('posts/<str:postId>/user/<str:userId>/vote/', vote_of_user_in_post),
    
    path('votes/', VoteList.as_view()),
    path('votes/<str:vote_type>/', VoteList_byVoteType),
    path('vote/', vote.as_view()),
    path('unvote/<str:id>/', unvote.as_view()),
    path('update-vote/<str:id>/', updateVote.as_view()),
    
    
    path('vote-type/<str:id>/', VoteTypeRetrieve.as_view()),

    path('tags/', tagsList.as_view()), #recuperer la liste des tags
    path('categories/', categoriesList.as_view()), #recuperer la liste des categories
    
    path('profile/', createProfile.as_view()),
    path('update-profile/<str:user>/', updateProfile.as_view()),
    path('profiles/', profilesList.as_view()),
    path('profiles/<str:user>/', retrieveProfile.as_view()),
    
    path('experiences/<str:userId>/', userExperience, name='experience-list'),
    path('experience/<str:pk>/', ExperienceDetail.as_view(), name='experience-detail'),
    
    path('educations/<str:userId>/', userEducation, name='education-list'),
    path('education/<str:pk>/', EducationDetail.as_view(), name='education-detail'),
    
    path('profiles/<str:userId>/skills/', userSkills, name='skills'),
    path('profile/<str:userId>/add-skills/', addSkills, name='add-skills'),
    path('profile/<str:userId>/remove-skills/', removeSkills, name='remove-skills'), 
    
    path('search/', search),
]