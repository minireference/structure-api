from rest_framework import serializers

from .models import DjangoBaseNode, DjangoDependencyRelation


class DjangoBaseNodeSlugSerializer(serializers.ModelSerializer):
    """
    Just reports the `uuid` of target node as well as (scope:path).
    """
    id = serializers.UUIDField(source='uuid', required=True)    
    class Meta:
        model = DjangoBaseNode
        fields = ('id', 'path', 'scope')
        read_only_fields = ('id')

# Relationship serialization
class DjangoUsedforsSerializer(serializers.ModelSerializer):
    usedfor = DjangoBaseNodeSlugSerializer(required=True)
    class Meta:
        model = DjangoDependencyRelation
        fields = ('usedfor', 'explain_usedfor', 'level')

class DjangoPrerequisitesSerializer(serializers.ModelSerializer):
    prerequisite = DjangoBaseNodeSlugSerializer(required=True)
    class Meta:
        model = DjangoDependencyRelation
        fields = ('prerequisite', 'explain_prerequisite', 'level')


class DjangoBaseNodeSerializer(serializers.ModelSerializer):
    """
    Used to recusiverly serialize Nodes to JSON.
      - hops=0: only data of current node is returned (fk for others)
      - hops=1: return also data of nodes linked to
    """
    id = serializers.UUIDField(source='uuid', required=True)
    prerequsites = DjangoPrerequisitesSerializer(source='prerequisites_set', many=True, read_only=True)
    usedfors = DjangoUsedforsSerializer(source='usedfors_set', many=True, read_only=True)        
    
    class Meta:
        model = DjangoBaseNode
        fields = ('id',
                  'path',
                  'scope',
                  'version',
                  'created_at',
                  'modified_at',
                  'comment',
                  'prerequsites',
                  'usedfors',
        )
        read_only_fields = ('created_at', 'modified_at', 'prerequsites')


class CreateDjangoBaseNodeSerializer(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     node = DjangoBaseNode.objects.create_node(**validated_data)
    #     return node
    class Meta:
        model = DjangoBaseNode
        fields = ('path',
                  'scope',
                  'version',
                  'comment',
        )
        read_only_fields = ('id',  'created_at', 'modified_at')
        # write_only_fields = ('',)





# # custom field example
# class PolymorphicTaggedObjectRelatedField(serializers.RelatedField):
#     """
#     A custom field to use for the `tagged_object` generic relationship.
#     """
#     def to_representation(self, value):
#         """
#         Serialize tagged objects to a simple textual representation.
#         """
#         if isinstance(value, Bookmark):
#             return 'Bookmark: ' + value.url
#         elif isinstance(value, Note):
#             return 'Note: ' + value.text
#         raise Exception('Unexpected type of tagged object')
# if isinstance(value, Bookmark):
#     serializer = BookmarkSerializer(value)
# elif isinstance(value, Note):
#     serializer = NoteSerializer(value)
# else:
#     raise Exception('Unexpected type of tagged object')
# 
# return serializer.data