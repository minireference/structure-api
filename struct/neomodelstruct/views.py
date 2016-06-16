
from pprint import pprint

from django.http import Http404
from rest_framework import views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import NeoBaseNode
from .serializers import CreateBaseNodeSerializer, BaseNodeSerializer


class NeoBaseNodeDetailView(views.APIView):
    """
    Retrieve or update individual `NeoBaseNode`s. 
    """
    def get(self, request, uuid, format=None):
        """
        Retrieve NeoBaseNode details.
        ---
        serializer: BaseNodeSerializer
        """
        node = NeoBaseNode.nodes.get(uuid=uuid)
        serializer = BaseNodeSerializer(node)
        return Response(serializer.data)

    def put(self, request, uuid, format=None):
        """
        Update NeoBaseNode details.
        ---
        serializer: BaseNodeSerializer
        """
        node = NeoBaseNode.nodes.get(uuid=uuid)
        serializer = BaseNodeSerializer(node, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NeoBaseNodeListView(views.APIView):
    """
    Retrieve list of all `NeoBaseNode`s (that match criteria).
    ---
    serializer: BaseNodeSerializer    
    """    
    def get(self, request, format=None):
        nodes = list(NeoBaseNode.nodes)
        serializer = BaseNodeSerializer(nodes, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """
        Create new NeoBaseNode.
        ---
        serializer: CreateBaseNodeSerializer
        """
        create_serializer = CreateBaseNodeSerializer(data=request.data)
        if create_serializer.is_valid():
            data = create_serializer.data
            # pprint(data)
            node = NeoBaseNode(**data)
            node.save()
            node.refresh()
            # pprint(node)
            serializer = BaseNodeSerializer(node)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

