from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import SendingDomain
from .serializers import SendingDomainSerializer
from services.domain_service import DomainService


class DomainViewSet(viewsets.ModelViewSet):
    serializer_class = SendingDomainSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SendingDomain.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """Trigger DNS verification for the domain."""
        domain = self.get_object()
        if domain.verified:
            return Response(
                {'detail': 'Domain already verified.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if DomainService.verify_domain(domain):
            domain.verified = True
            domain.save(update_fields=['verified'])
            return Response({'verified': True})
        else:
            return Response(
                {
                    'verified': False,
                    'detail': 'Verification TXT record not found or does not match.'
                },
                status=status.HTTP_200_OK  # Not an error, allows retry
            )