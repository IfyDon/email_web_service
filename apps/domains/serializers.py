from rest_framework import serializers
from .models import SendingDomain
from services.domain_service import DomainService


class SendingDomainSerializer(serializers.ModelSerializer):
    verification_record = serializers.SerializerMethodField()
    dkim_record = serializers.SerializerMethodField()

    class Meta:
        model = SendingDomain
        fields = [
            'id', 'domain_name', 'verified', 'verification_token',
            'spf_record', 'dkim_selector', 'dkim_public_key',
            'verification_record', 'dkim_record',
            'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'verified', 'verification_token', 'dkim_public_key',
            'verification_record', 'dkim_record', 'created_at', 'updated_at',
        ]

    def get_verification_record(self, obj):
        return {
            'name': obj.get_verification_record_name(),
            'type': 'TXT',
            'value': obj.verification_token,
        }

    def get_dkim_record(self, obj):
        if not obj.dkim_public_key:
            return None
        # Construct a simplified DKIM TXT record value.
        # In production you would strip header/footer lines and concatenate.
        pub_key_stripped = (
            obj.dkim_public_key
            .replace('-----BEGIN PUBLIC KEY-----', '')
            .replace('-----END PUBLIC KEY-----', '')
            .replace('\n', '')
            .strip()
        )
        return {
            'name': obj.get_dkim_record_name(),
            'type': 'TXT',
            'value': f'v=DKIM1; k=rsa; p={pub_key_stripped}',
        }

    def create(self, validated_data):
        user = self.context['request'].user
        # Generate DKIM keys
        private_key, public_key = DomainService.generate_dkim_keys()
        validated_data['dkim_private_key'] = private_key
        validated_data['dkim_public_key'] = public_key
        # Optional default SPF record
        if not validated_data.get('spf_record'):
            validated_data['spf_record'] = 'v=spf1 include:spf.example.com ~all'
        domain = SendingDomain.objects.create(user=user, **validated_data)
        return domain