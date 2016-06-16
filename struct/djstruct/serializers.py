from rest_framework import serializers

from .models import DjangoBaseNode


class DjangoBaseNodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DjangoBaseNode
        fields = ('id',
                  'path',
                  'scope',
                  'version',
                  'created_at',
                  'modified_at',
                  'comment',
        )
        read_only_fields = ('created_at', 'modified_at')


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
