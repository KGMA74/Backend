from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# ----------------------Todo
#:::::::::Ok
# create model User 
# create model Post :::::::::Ok
# create model Comment :::::::::Ok
# create model Vote :::::::::Ok
# create model Vote_type :::::::::Ok
# create model PostCategory :::::::::Ok
# create model Tag :::::::::Ok
# create relation comment_user :::::::::Ok
# create relation comment_post :::::::::Ok
# create relation post_user :::::::::Ok
# create relation user_vote :::::::::Ok
# create relation post_vote :::::::::Ok
# create relation post_tag 
# create relation post_post_category :::::::::Ok
# create relation vote_vote_type :::::::::Ok
# creationd de la relation followers_following
# ##



# Custom user manager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from api.manager import UserManager



class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    nickname = models.CharField(max_length=50, unique=True)
    #la definition du champ password n'est pas necessaire car faite par defaut par django
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname'] #USERNAME_FIELD et password sont requs pardefaut

    def __str__(self):
        return self.email
    
    def has_module_perms(self, obj=None):
        return True
    
    def has_perm(self, perm, obj=None):
        return True
'''
class Profile(models.Model):
    # utiliser le id de user comme clef primaire [to do]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    #ajout recent
    #follow = models.ManyToManyField(self, on_delete=models.CASCADE, related_name='followers_followings')#
    confirmed = models.BooleanField(default=False)
    reputation = models.FloatField(default=0) 

    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.nickname
'''

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    
    following = models.ManyToManyField('self', symmetrical=False, related_name='follower', blank=True) # symetrical a false car A suit B n implique pas B suit A
    confirmed = models.BooleanField(default=False)
    reputation = models.IntegerField(default=0)

    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user}'

class Tag(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    
    def count_posts(self):
        return self.posts.count()

class PostCategory(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    parent_post = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='comments') # si non null => cest un commentaire
    category = models.ForeignKey(PostCategory, related_name='posts', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    
    title = models.CharField(max_length=255, blank=True, null=True)
    details = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title or ''
    
    def is_comment(self):
        return self.parent_post is not None

       
class VoteType(models.Model):
    vote_type = models.CharField(max_length=50, primary_key=True) #upvote | downvote |

    def __str__(self):
        return self.vote_type

class Vote(models.Model):
    author = models.ForeignKey(User, related_name='vote_author', on_delete=models.CASCADE) #
    post = models.ForeignKey(Post, related_name='vote_post', on_delete=models.CASCADE) #
    type = models.ForeignKey(VoteType, related_name='votes_type', on_delete=models.CASCADE) #

    class Meta:
        #ajout d'une contraine unique car un user ne pouvant faire qu'un seul vote./
        constraints = [
            models.UniqueConstraint(fields=['author', 'post'], name='unique_user_post_vote')
        ]

    def __str__(self):
        return f"{self.author} voted {self.type.vote_type} on {self.post.title}"
    

class Image(models.Model):
    author = models.ForeignKey(User, related_name='image', on_delete=models.CASCADE) #
    post = models.ForeignKey(Post, related_name='votes', on_delete=models.CASCADE) #
        
    url = models.ImageField(upload_to='Images/', blank=True, null=True)
    


#pour la creation d un profile auto associe un new user
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
