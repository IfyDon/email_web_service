import secrets
from django.conf import settings
from django.db import models


def generate_verification_token():
    return 'ev_' + secrets.token_urlsafe(24)


class SendingDomain(models.Model):
    """
    Represents a custom sending domain owned by a user.
    Stores verification information and DKIM keys.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='domains'
    )
    domain_name = models.CharField(max_length=255)
    verified = models.BooleanField(default=False)
    verification_token = models.CharField(
        max_length=64,
        default=generate_verification_token,
        editable=False,
        help_text="TXT record value to prove ownership"
    )
    spf_record = models.TextField(
        blank=True,
        help_text="Complete SPF TXT record (e.g., 'v=spf1 include:spf.example.com ~all')"
    )
    dkim_selector = models.CharField(
        max_length=64,
        default='default',
        help_text="DKIM selector prefix (e.g., 'google')"
    )
    dkim_private_key = models.TextField(
        blank=True,
        help_text="DKIM private key in PEM format (store encrypted in production)"
    )
    dkim_public_key = models.TextField(
        blank=True,
        help_text="DKIM public key in PEM format"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'domain_name']

    def __str__(self):
        return self.domain_name

    def get_verification_record_name(self) -> str:
        """DNS name where the ownership TXT record must be placed."""
        return f"_email-service.{self.domain_name}"

    def get_dkim_record_name(self) -> str:
        """DNS name for the DKIM TXT record."""
        return f"{self.dkim_selector}._domainkey.{self.domain_name}"