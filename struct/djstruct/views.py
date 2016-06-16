
from pprint import pprint

from django.http import Http404
from rest_framework import views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import DjangoBaseNode
from .permissions import IsOwnerOrReadOnly
from .serializers import CreateDjangoBaseNodeSerializer, DjangoBaseNodeSerializer


class DjangoBaseNodeDetailView(views.APIView):
    """
    Retrieve or update individual `DjangoBaseNode`s. 
    """
    permission_classes = (IsOwnerOrReadOnly,)
    
    
    def get(self, request, uuid, format=None):
        """
        Retrieve DjangoBaseNode details.
        ---
        serializer: DjangoBaseNodeSerializer
        """
        node = DjangoBaseNode.objects.get(pk=uuid)
        serializer = DjangoBaseNodeSerializer(node)
        return Response(serializer.data)

    def put(self, request, uuid, format=None):
        """
        Update DjangoBaseNode details.
        ---
        serializer: DjangoBaseNodeSerializer
        """
        node = DjangoBaseNode.objects.get(pk=uuid)
        self.check_object_permissions(request, node)
        serializer = DjangoBaseNodeSerializer(node, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DjangoBaseNodeListView(views.APIView):
    """
    Retrieve list of all `DjangoBaseNode` (that match criteria).
    ---
    serializer: DjangoBaseNodeSerializer    
    """
    permission_classes = (IsOwnerOrReadOnly,)
    
    def get(self, request, format=None):
        pre_nodes = DjangoBaseNode.objects.all()
        nodes = list(pre_nodes)
        serializer = DjangoBaseNodeSerializer(nodes, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """
        Create new DjangoBaseNode.
        ---
        serializer: CreateDjangoBaseNodeSerializer
        """
        create_serializer = CreateDjangoBaseNodeSerializer(data=request.data)
        if create_serializer.is_valid():
            node = DjangoBaseNode(**create_serializer.data)
            node.save()
            serializer = DjangoBaseNodeSerializer(node)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

