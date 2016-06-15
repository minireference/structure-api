from __future__ import unicode_literals

import uuid
from django.db import models

from .customqueryset import CustomQuerySet


class BaseNodeManager(models.Manager):
    def get_queryset(self):
        # print "in BaseNodeManager get_queryset"
        return CustomQuerySet(self.model)


class BaseNode(models.Model):
    id          = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    path        = models.CharField(blank=False, max_length=1000, verbose_name='path')
    scope       = models.CharField(default='miniref', max_length=1000, verbose_name='scope')
    version     = models.CharField(default='0.1', max_length=1000, verbose_name='schema version')
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='last modified')
    comment     = models.TextField(blank=True, default='', verbose_name='comment')

    objects = BaseNodeManager()         ## used from API end
    _objects_impl = models.Manager()    ## use to access DB

    def __unicode__(self):
        return "BaseNode:" + self.scope + '::' + self.path + 'v' + self.version
    
    def __repr__(self):
        return 'BaseNode:' + str(self.id)

    def save(self, *args, **kwargs):
        """
        Custom save method.
        """
        print "In custom save method >>>>>>>>>>>>>>>>>>>>"
        super(BaseNode, self).save()
