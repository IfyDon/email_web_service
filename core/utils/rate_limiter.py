from rest_framework.throttling import SimpleRateThrottle
from apps.accounts.models import APIKey

class APIKeyRateThrottle(SimpleRateThrottle):
    """
    Rate throttle based on the API key's 'rate_limit' field (requests per minute).
    Falls back to 100/min if no key is present.
    """
    scope = 'api_key'  # Not used directly; we override get_rate

    def get_cache_key(self, request, view):
        # Use the API key's ID as the unique key
        if hasattr(request, 'auth') and isinstance(request.auth, APIKey):
            api_key = request.auth
            self.rate = f"{api_key.rate_limit}/min"
            return self.cache_format % {
                'scope': 'api_key',
                'ident': api_key.pk
            }
        # Fallback to IP throttling if no API key (unlikely for protected views)
        return self.cache_format % {
            'scope': 'api_key',
            'ident': self.get_ident(request)
        }

    def get_rate(self):
        # rate is already set in get_cache_key
        return self.rate if hasattr(self, 'rate') else '100/min'