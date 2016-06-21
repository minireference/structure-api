from __future__ import unicode_literals
import uuid

from neomodel import (StructuredNode,
                      StructuredRel,
                      StringProperty,
                      IntegerProperty,
                      DateTimeProperty,
                      RelationshipTo,
                      RelationshipFrom)



class NeoDependencyRelation(StructuredRel):
    """
    Represents `(m)<--dependson--(n)` relations and implies `(m)--usedfor-->(n)`.
    """
    # id  auto-created
    explain_prerequisite = StringProperty()
    explain_usedfor      = StringProperty()
    level                = StringProperty()

    def __unicode__(self):
        return '<NeoDependencyRelation ' + self._id + '>'
        # self.prerequisite.path + '--usedfor-->' + self.usedfor.path + 
    
    def __repr__(self):
        return self.__unicode__()



class NeoBaseNode(StructuredNode):
    """
    BaseNode that is extended by SubjectNode, TopicNode, and ConceptNode
    """ 
    # _id (int) is asssigned automatically, but lets keep the UUID primary key design
    uuid        = StringProperty(unique_index=True, default=uuid.uuid4)
    path        = StringProperty(unique_index=True, required=True)
    scope       = StringProperty(default='miniref')
    version     = StringProperty(default='0.1')
    created_at  = DateTimeProperty()
    modified_at = DateTimeProperty()
    comment     = StringProperty()
    
    prerequisites = RelationshipTo('neomodelstruct.NeoBaseNode',   'prerequisite', model=NeoDependencyRelation)
    usedfors      = RelationshipFrom('neomodelstruct.NeoBaseNode', 'prerequisite', model=NeoDependencyRelation)
    # ABANDON SHIP  ===  Tue 21 Jun 2016 14:48:55 EDT
    # The inference of sting to class for relatinships is not working:
    # https://github.com/robinedwards/neomodel/blob/master/neomodel/relationship_manager.py#L179
    # I also tried 'NeoBaseNode'  and 'neomodelstruct.models.NeoBaseNode' but no cigar

    def __unicode__(self):
        return "<NeoBaseNode " + self.scope + ':' + self.path + ">"
    
    def __repr__(self):
        return self.__unicode__()

    def save(self, *args, **kwargs):
        """
        Custom save methodself.
        """
        super(NeoBaseNode, self).save()

