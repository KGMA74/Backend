from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

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

# Custom user manager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from api.manager import UserManager



class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    nickname = models.CharField(max_length=50, unique=True)
    #la definition du chalmp password n'est pas necessair car fait par defaut
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname'] #USERNAME_FIELDet password sont requs pardefaut

    def __str__(self):
        return self.email
    
    def has_module_perms(self, obj=None):
        return True
    
    def has_perm(self, perm, obj=None):
        return True

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.nickname


class PostCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    owner = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    category = models.ForeignKey(PostCategory, related_name='posts', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='posts')
    
    title = models.CharField(max_length=255)
    details = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE) #
    owner = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE) #
    
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.content[:50]
       
class VoteType(models.Model):
    vote_type = models.CharField(max_length=50) #upvote | downvote |

    def __str__(self):
        return self.vote_type

class Vote(models.Model):
    owner = models.ForeignKey(User, related_name='votes', on_delete=models.CASCADE) #
    post = models.ForeignKey(Post, related_name='votes', on_delete=models.CASCADE) #
    type = models.ForeignKey(VoteType, related_name='votes', on_delete=models.CASCADE) #

    class Meta:
        #ajout d'une contraine unique car un user ne pouvant faire qu'un suele vote./
        constraints = [
            models.UniqueConstraint(fields=['owner', 'post'], name='unique_user_post_vote')
        ]

    def __str__(self):
        return f"{self.owner} voted {self.type.vote_type} on {self.post.title}"
    
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='send', on_delete=models.DO_NOTHING) #
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.DO_NOTHING) #
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)