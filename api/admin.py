from django.contrib import admin
from api.models import (
    User, Profile, PostCategory, 
    Post, Tag, Vote, VoteType
)

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'email']
    
class ProfileAdmin(admin.ModelAdmin):
    list_editable = ['verified']
    list_display = ['user', 'full_name', 'verified']
    
admin.site.register(User, UserAdmin)
admin.site.register([
    Profile, 
    PostCategory, 
    Post, 
    Tag, 
    Vote, 
    VoteType,
])