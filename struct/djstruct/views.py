
from pprint import pprint

from django.http import Http404
from rest_framework import views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import BaseNode
from .permissions import IsOwnerOrReadOnly
from .serializers import CreateBaseNodeSerializer, BaseNodeSerializer


class BaseNodeDetailView(views.APIView):
    """
    Retrieve or update individual `BaseNode`s. 
    """
    permission_classes = (IsOwnerOrReadOnly,)
    
    
    def get(self, request, uuid, format=None):
        """
        Retrieve BaseNode details.
        ---
        serializer: BaseNodeSerializer
        """
        node = BaseNode.objects.get(uuid=uuid)
        serializer = BaseNodeSerializer(node)
        return Response(serializer.data)

    def put(self, request, uuid, format=None):
        """
        Update BaseNode details.
        ---
        serializer: BaseNodeSerializer
        """
        node = BaseNode.objects.get(uuid=uuid)
        self.check_object_permissions(request, node)
        serializer = BaseNodeSerializer(node, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseNodeListView(views.APIView):
    """
    Retrieve list of all `BaseNode` (that match criteria).
    ---
    serializer: BaseNodeSerializer    
    """
    permission_classes = (IsOwnerOrReadOnly,)
    
    def get(self, request, format=None):
        pre_nodes = BaseNode.objects.all()
        nodes = list(pre_nodes)
        serializer = BaseNodeSerializer(nodes, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """
        Create new BaseNode.
        ---
        serializer: CreateBaseNodeSerializer
        """
        create_serializer = CreateBaseNodeSerializer(data=request.data)
        if create_serializer.is_valid():
            node = create_serializer.save()
            serializer = BaseNodeSerializer(node)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

