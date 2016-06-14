from rest_framework import serializers

from .models import BaseNode


class BaseNodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseNode
        fields = ('id',
                  'path',
                  'scope',
                  'version',
                  'created_at',
                  'modified_at',
                  'comment',
        )
        read_only_fields = ('created_at', 'modified_at')


class CreateBaseNodeSerializer(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     node = BaseNode.objects.create_node(**validated_data)
    #     return node
    class Meta:
        model = BaseNode
        fields = ('id',
                  'path',
                  'scope',
                  'version',
                  'created_at',
                  'modified_at',
                  'comment',
        )
        read_only_fields = ('created_at', 'modified_at')
        # write_only_fields = ('',)
