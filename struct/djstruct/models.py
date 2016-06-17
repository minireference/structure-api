from __future__ import unicode_literals

import uuid
from django.db import models


# source https://github.com/django/django/blob/master/django/db/models/base.py
class DjangoBaseNode(models.Model):
    # id  auto-created by Django  (primary_key=True)
    uuid        = models.UUIDField(default=uuid.uuid4, editable=False)
    path        = models.CharField(blank=False, max_length=1000)
    scope       = models.CharField(default='miniref', max_length=1000)
    version     = models.CharField(default='0.1', max_length=1000, verbose_name='schema version')
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='last modified')
    comment     = models.TextField(blank=True, null=True, verbose_name='comments')

    class Meta:
        unique_together = ('scope', 'path')

    # Containment (folder-like) structure
    ############################################################################
    # contents = models.ManyToManyField("self", symmetrical=False,
    #                                   through='DjangoContainmentRelation',
    #                                   through_fields=('parent', 'child')
    #                                   related_name='parents')

    # Dependency structure
    ############################################################################
    prerequsites = models.ManyToManyField("self", symmetrical=False,
                                          through='DjangoDependencyRelation',
                                          through_fields=('usedfor', 'prerequisite'),
                                          related_name='usedfors')
    # Generic relatedness
    ############################################################################
    # TODO:   <--relatedto--> symmetric relationship
    
    def __unicode__(self):
        return "<DjangoBaseNode " + self.scope + ':' + self.path + '>'
    
    def __repr__(self):
        return self.__unicode__()

    def save(self, *args, **kwargs):
        """
        Custom save method.
        """
        # print "In custom save method >>>>>>>>>>>>>>>>>>>>"
        super(DjangoBaseNode, self).save()




# RELATIONSHIPS
# using https://docs.djangoproject.com/en/1.9/topics/db/models/#intermediary-manytomany

class DjangoDependencyRelation(models.Model):
    """
    Represents `(m)<--dependson--(n)` relations and implies `(m)--usedfor-->(n)`.
    """
    # id  auto-created
    prerequisite   = models.ForeignKey(DjangoBaseNode, null=True, related_name='prerequisites_rels', on_delete=models.SET_NULL)
    usedfor        = models.ForeignKey(DjangoBaseNode, null=True, related_name='usedfors_rels', on_delete=models.SET_NULL)
    explain_prerequisite  = models.CharField(max_length=1000, verbose_name='Explain why prerequsite is needed')
    explain_usedfor       = models.CharField(max_length=1000, verbose_name='Explain the application')
    level    = models.CharField(default='HS', max_length=1000, verbose_name='Educational level')

    def __unicode__(self):
        return '<Rel ' + self.prerequisite.path + '--usedfor-->' + self.usedfor.path + '>'
    
    def __repr__(self):
        return self.__unicode__()



# class DjangoBaseRelation(models.Model):
#     """
#     Metadata fields common to all relations.
#     """
#     scope       = models.CharField(default='miniref', max_length=1000, verbose_name='scope')
#     version     = models.CharField(default='0.1', max_length=1000, verbose_name='schema version')
#     created_at  = models.DateTimeField(auto_now_add=True, verbose_name='created at')
#     modified_at = models.DateTimeField(auto_now=True, verbose_name='last modified')
#     comment     = models.TextField(blank=True, null=True, verbose_name='comment')

# class DjangoContainmentRelation(models.Model):
#     """
#     Represents `p--contains--> c` relations and implies a c--ispartof-->p rel'n.
#     """
#     # id auto-created
#     parent   = models.ForeignKey(DjangoBaseNode, on_delete=models.SET_NULL)
#     child    = models.ForeignKey(DjangoBaseNode, on_delete=models.SET_NULL)
#     explain  = models.CharField(max_length=1000, verbose_name='Explanation')
#     level    = models.CharField(default='HS', max_length=1000, verbose_name='educational level')

    