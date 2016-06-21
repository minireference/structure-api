from rest_framework import serializers

from .models import NeolixirBaseNode


class NeolixirBaseNodeSlugSerializer(serializers.Serializer):
    """
    Just reports the `uuid` of target node as well as (scope:path).
    """
    id = serializers.UUIDField(source='uuid', required=True)
    path = serializers.CharField(max_length=1000)
    scope = serializers.CharField(max_length=1000)

# Different serializer depending on direction being used for relationship
class NeolixirUsedforsRelationSerializer(serializers.Serializer):
    usedfor = NeolixirBaseNodeSlugSerializer(source='_start', required=True)
    explain_usedfor = serializers.CharField(max_length=1000)
    level = serializers.CharField(max_length=1000)

class NeolixirPrerequisitesRelationSerializer(serializers.Serializer):
    prerequisite = NeolixirBaseNodeSlugSerializer(source='_end', required=True)
    explain_prerequisite  = serializers.CharField(max_length=1000)
    level = serializers.CharField(max_length=1000)

class NeolixirBaseNodeSerializer(serializers.Serializer):
    """
    Serializer used for GET, PUT, and DELETE requests.
    """
    id          = serializers.UUIDField(source='uuid', required=True)
    path        = serializers.CharField(max_length=1000)
    scope       = serializers.CharField(max_length=1000)
    version     = serializers.CharField(max_length=1000)
    created_at  = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
    comment     = serializers.CharField(allow_blank=True)

    prerequisites = NeolixirPrerequisitesRelationSerializer(source='prerequisites.rels', many=True, read_only=True)
    usedfors = NeolixirUsedforsRelationSerializer(source='usedfors.rels', many=True, read_only=True)

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
    comment     = serializers.CharField(allow_blank=True, max_length=1000)

    def create(self, validated_data):
        node = NeolixirBaseNode(**validated_data)
        node.save()
        return node

