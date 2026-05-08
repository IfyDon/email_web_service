from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.utils import timezone
import secrets


def generate_api_key():
    """Generate a plaintext API key (stored hashed)."""
    return 'ewk_' + secrets.token_urlsafe(32)


class APIKey(models.Model):
    """
    Represents an API key for programmatic access.
    The key is hashed using Django's password hashers – never stored in plaintext.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='api_keys'
    )
    label = models.CharField(max_length=128, help_text="A name to identify this key")
    prefix = models.CharField(max_length=8, editable=False)        # first 8 chars of plaintext
    hashed_key = models.CharField(max_length=256, editable=False)
    is_active = models.BooleanField(default=True)
    rate_limit = models.IntegerField(
        default=100,
        help_text="Max requests per minute for this key"
    )
    last_used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.label} ({self.prefix}…)"

    def save(self, *args, **kwargs):
        # If it's a new key, generate one and hash it
        if not self.pk:
            raw_key = generate_api_key()
            self.prefix = raw_key[:8]
            self.hashed_key = make_password(raw_key)
        super().save(*args, **kwargs)

    def verify_key(self, raw_key: str) -> bool:
        """Check if the provided raw key matches the stored hash."""
        return check_password(raw_key, self.hashed_key)

    @classmethod
    def get_key_by_plaintext(cls, raw_key: str):
        """Find the APIKey object for a given plaintext key (if valid)."""
        # We only store the prefix; we need to iterate over possible matches
        prefix = raw_key[:8]
        candidates = cls.objects.filter(prefix=prefix, is_active=True)
        for key_obj in candidates:
            if key_obj.verify_key(raw_key):
                return key_obj
        return None

    def touch(self):
        """Update last_used_at without triggering signals or full save cycle."""
        APIKey.objects.filter(pk=self.pk).update(last_used_at=timezone.now())