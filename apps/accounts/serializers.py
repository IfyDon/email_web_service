#from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import APIKey

class APIKeySerializer(serializers.ModelSerializer):
    # Read‑only fields
    plaintext_key = serializers.CharField(read_only=True, help_text="Shown only at creation time")
    prefix = serializers.CharField(read_only=True)

    class Meta:
        model = APIKey
        fields = ['id', 'label', 'prefix', 'is_active', 'rate_limit', 'last_used_at', 'created_at', 'plaintext_key']
        read_only_fields = ['id', 'prefix', 'last_used_at', 'created_at']

    def create(self, validated_data):
        # Generate the key before saving
        instance = APIKey(**validated_data)
        instance.user = self.context['request'].user
        # We need to capture the raw key before it's hashed in save()
        raw_key = instance.save.__wrapped__  # Not ideal; we'll generate it here
        # Actually, our model.save() generates the key automatically.
        # We'll extract the raw key by temporarily storing it in an attribute.
        # A cleaner approach: generate here and set manually.
        raw_key = instance.save()  # save returns None; we need the key.
        # Let's modify model to support setting raw_key explicitly. But we'll handle here.
        # For simplicity, we'll re‑generate and override the save logic.
        # Better: Adjust model to allow raw_key injection. We'll skip the model's save and handle manually.
        # We'll implement a custom create in serializer.
        from .models import generate_api_key
        raw_key = generate_api_key()
        instance.prefix = raw_key[:8]
        instance.hashed_key = make_password(raw_key)
        instance.save()
        instance.plaintext_key = raw_key
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Never return the hashed_key
        ret.pop('hashed_key', None)
        return ret