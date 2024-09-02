"""
Ici sont defini les fonction utilitaires comme le calcul de la reputatiom d un utilisateur ....
"""
from .models import (
    Vote,
    Profile,
    Post
)


def Post_votes_nbr(post_id):
    """
    Retourne le nombre de votes positifs (upvotes) et négatifs (downvotes) pour un post donné.
    """
    votes = Vote.objects.filter(post=post_id)  # Filtre les votes associés au post spécifié
    upvotes = votes.filter(type='upvote').count()  # Compte le nombre de votes positifs (type=1)
    downvotes = votes.filter(type='downvote').count()  # Compte le nombre de votes négatifs (type=2)
    return upvotes, downvotes


def calculate_vote_impact(vote_type, Pweight=1, Nweight=2, delete=False):
    """
    Calcule l'impact d'un vote individuel.
    """
    reverse = -1 if delete else 1  # Ajuste la direction de l'impact en fonction de la suppression

    if vote_type == 'upvote': 
        return Pweight * reverse
    elif vote_type == 'downvote':  
        return - Nweight * reverse
    return 0

def apply_vote_impact(vote_id, delete=False):
    """
    Applique l'impact d'un vote individuel à la réputation de l'auteur du post.
    delete=True indique la suppression du vote d'id vote_id.
    """

    vote = Vote.objects.get(id=vote_id)
    post = vote.post
    profile = Profile.objects.get(user=post.author)

    # Calculer l'impact du vote
    impact = calculate_vote_impact(vote.vote_type, delete=delete)

    # Mettre à jour la réputation
    profile.reputation += impact
    profile.save()

    return profile.reputation


def total_comments(postId):
    """
    Retourne le nombre total de commentaires pour un post donné.
    """
    return Post.objects.get(id=postId).comments.count()


def count_total_comments(post_id):
    """
    Compte le nombre total de posts associés à un post principal, y compris tous les commentaires directs et indirects.
    
    :param post_id: ID du post principal
    :return: Nombre total de posts incluant le post principal et tous ses commentaires
    """
    try:
        post = Post.objects.get(id=post_id)
        count = 0  

        def count_comments(post):
            nonlocal count # utiliser le meme count defini anterieurement
            comments = Post.objects.filter(parent_post=post)
            count += comments.count()  # Ajouter le nombre de commentaires directs
            for comment in comments:
                count_comments(comment)  # Récursion pour compter les sous-commentaires

        count_comments(post)
        return count
    
    except Post.DoesNotExist:
        return -1
