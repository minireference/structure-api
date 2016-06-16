from rest_framework import serializers

from .models import NeolixirBaseNode


class BaseNodeSerializer(serializers.Serializer):
    """
    Serializer used for GET, PUT, and DELETE requests.
    """
    id          = serializers.UUIDField(source='uuid', required=True)
    path        = serializers.CharField(max_length=1000)
    scope       = serializers.CharField(max_length=1000)
    version     = serializers.CharField(max_length=1000)
    created_at  = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
    comment     = serializers.CharField(allow_blank=True, allow_null=True)

    def update(self, instance, validated_data):
        instance.path = validated_data.get('path', instance.path)
        instance.scope = validated_data.get('scope', instance.scope)
        instance.version = validated_data.get('version', instance.version)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance

class CreateBaseNodeSerializer(serializers.Serializer):
    path        = serializers.CharField(required=True,    max_length=1000)
    scope       = serializers.CharField(allow_blank=True, max_length=1000)
    version     = serializers.CharField(allow_blank=True, max_length=1000)
    comment     = serializers.CharField(allow_blank=True, allow_null=True, max_length=1000)

