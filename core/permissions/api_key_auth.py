from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from apps.accounts.models import APIKey
from django.utils import timezone

class APIKeyAuthentication(BaseAuthentication):
    """
    Authenticate requests using an API key in the Authorization header:
        Authorization: Bearer <key>
    """
    keyword = 'Bearer'

    def authenticate(self, request):
        auth = request.headers.get('Authorization')
        if not auth:
            return None

        try:
            keyword, raw_key = auth.split()
            if keyword.lower() != self.keyword.lower():
                return None
        except ValueError:
            raise exceptions.AuthenticationFailed('Invalid authorization header format.')

        # Validate key
        api_key = APIKey.get_key_by_plaintext(raw_key)
        if not api_key:
            raise exceptions.AuthenticationFailed('Invalid or expired API key.')

        if not api_key.is_active:
            raise exceptions.AuthenticationFailed('API key has been revoked.')

        # Update last_used_at (lightweight)
        api_key.touch()

        # The authenticated user is the owner of the key
        return (api_key.user, api_key)

    def authenticate_header(self, request):
        return 'Bearer realm="API"'