"""
fonction utilitire pour la gestion de la repution d'un utilisateur en fonction de sa contribution Sur ESIOverflow
(post, reponse) tout en tenant comptes des reaction des reaction d'autres utilisateurs faces a ses posts, reponse
"""
from .models import Profile, Post

def reputations(uid, postId=None, CommentId=None):
    reput = Profile.objects.get(id=uid) # en supposantv aue le uid de user ait dejq ete def comme id du profile
    #impact des posts
    if postId:
        v = post
        pass
    
    #impact des solution apportees
    if CommentId:
        pass