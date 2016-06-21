from pprint import pprint

from django.http import Http404
from rest_framework import views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import NeolixirBaseNode
from .serializers import CreateBaseNodeSerializer, NeolixirBaseNodeSerializer


class NeolixirBaseNodeDetailView(views.APIView):
    """
    Retrieve or update individual `NeolixirBaseNode`s. 
    """
    def get(self, request, uuid, format=None):
        """
        Retrieve NeolixirBaseNode details.
        ---
        serializer: NeolixirBaseNodeSerializer
        """
        node = NeolixirBaseNode.get_by(uuid=str(uuid))
        serializer = NeolixirBaseNodeSerializer(node)
        return Response(serializer.data)

    def put(self, request, uuid, format=None):
        """
        Update NeolixirBaseNode details.
        ---
        serializer: NeolixirBaseNodeSerializer
        """
        node = NeolixirBaseNode.get_by(uuid=str(uuid))
        serializer = NeolixirBaseNodeSerializer(node, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NeolixirBaseNodeListView(views.APIView):
    """
    Retrieve list of all `NeolixirBaseNode`s (that match criteria).
    ---
    serializer: NeolixirBaseNodeSerializer    
    """    
    def get(self, request, format=None):
        nodes = NeolixirBaseNode.query.all()
        serializer = NeolixirBaseNodeSerializer(nodes, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """
        Create new NeolixirBaseNode.
        ---
        serializer: CreateBaseNodeSerializer
        """
        create_serializer = CreateBaseNodeSerializer(data=request.data)
        if create_serializer.is_valid():
            node = create_serializer.save()
            # print "Creating NeolixirBaseNode "
            # print node
            serializer = NeolixirBaseNodeSerializer(node)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

