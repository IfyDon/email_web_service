from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import APIKey
from .serializers import APIKeySerializer

class APIKeyViewSet(viewsets.ModelViewSet):
    """
    Manage API keys for the currently authenticated user.
    """
    serializer_class = APIKeySerializer
    permission_classes = [permissions.IsAuthenticated]   # Requires user login (session / token)

    def get_queryset(self):
        return APIKey.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def revoke(self, request, pk=None):
        """Deactivate (revoke) an API key."""
        api_key = self.get_object()
        api_key.is_active = False
        api_key.save(update_fields=['is_active'])
        return Response({'status': 'revoked'})

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Reactivate a previously revoked key."""
        api_key = self.get_object()
        api_key.is_active = True
        api_key.save(update_fields=['is_active'])
        return Response({'status': 'activated'})