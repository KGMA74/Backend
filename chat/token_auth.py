from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from rest_framework_simplejwt.tokens import AccessToken

from api.models import User


@database_sync_to_async
def get_user(access_token):
    try:
        token = AccessToken(access_token)
        user_id = token.payload['user_id']
        return User.objects.get(pk=user_id)
    except Exception as e:
        return None


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)
        
    async def __call__(self, scope, receive, send):
        # Récupérer les cookies de la requête
        headers = dict(scope['headers'])
        cookie_header = headers.get(b'cookie', b'').decode()

        access_token = None
        if cookie_header:
            cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookie_header.split('; ')}
            access_token = cookies.get('access_token', None)

        if access_token:
            # Si le token est trouvé, récupérer l'utilisateur
            scope['user'] = await get_user(access_token)
            
        return await super().__call__(scope, receive, send)