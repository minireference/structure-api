from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from .models import BaseNode
from .permissions import IsOwnerOrReadOnly
from .serializers import CreateBaseNodeSerializer, BaseNodeSerializer

class BaseNodeViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    """
    Creates, updates, and retrives BaseNode objects.
    """
    queryset = BaseNode.objects.all()
    serializer_class = BaseNodeSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def create(self, request, *args, **kwargs):
        self.serializer_class = CreateBaseNodeSerializer
        self.permission_classes = (AllowAny,)
        return super(BaseNodeViewSet, self).create(request, *args, **kwargs)
