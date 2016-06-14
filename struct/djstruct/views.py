
from django.http import Http404

from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from .models import BaseNode
from .permissions import IsOwnerOrReadOnly
from .serializers import CreateBaseNodeSerializer, BaseNodeSerializer
from .customqueryset import CustomQuerySet


class BaseNodeViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    """
    Creates, updates, and retrives BaseNode objects.
    """
    queryset = CustomQuerySet(model=BaseNode)
    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self, *args, **kwargs):
        """
        Custom get_object method to retrieve one item
        """
        # print args                  # nope
        # print kwargs                # nope!
        # print self.get_queryset()   # nope!!
        # print lookup_url_kwarg      # nope!!!
        # print self.kwargs           # YES
        try:
            return self.get_queryset().get(pk=self.kwargs['pk'])
        except BaseNode.DoesNotExist:
            raise Http404

    def get_serializer(self, *args, **kwargs):
        """
        Selectable serializer for instance.  This can be used when returning
        generic Nodes---will need custom serializer depending on instance.
        """
        # print "In get_serializer"
        # print args
        # print kwargs        # contains instance --> when detail view
        # print self.args
        # print self.kwargs
        _serializer_class = BaseNodeSerializer
        return _serializer_class(*args, **kwargs)
        
    def create(self, request, *args, **kwargs):
        self.serializer_class = CreateBaseNodeSerializer
        self.permission_classes = (AllowAny,)
        return super(BaseNodeViewSet, self).create(request, *args, **kwargs)
