from rest_framework import serializers
from api.models import User, Profile, PostCategory, Post, Tag, Vote, VoteType, Comment
#from django.contrib.auth.password_validation import validate_password

"""
[!] plus necessaire car on va utiliser les jwt tokens pour la gestions des login/logout etant plus securisé

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['nickname', 'email', 'password', 'password2']
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Password fields does not match'}
            )
        return attrs
        
    def create(self, validated_data):
        user = User.objects.create(
            nickname =validated_data['nickname'],
            email = validated_data['email']
        )
        user.set_password(validated_data['password']) #cela permet d'hasher le code avant d'enregistrer
        user.save()
        return user
"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
    
class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = '__all__'
    
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
    
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

class VoteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteType
        fields = '__all__'