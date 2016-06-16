from __future__ import unicode_literals
import uuid


from neomodel import (StructuredNode,
                      StringProperty,
                      IntegerProperty,
                      DateTimeProperty,
                      RelationshipTo,
                      RelationshipFrom)


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

    def __unicode__(self):
        return "NeoBaseNode " + self.scope + '::' + self.path + ' v' + self.version
    
    def __repr__(self):
        return 'NeoBaseNode ' + str(self._id)


    def save(self, *args, **kwargs):
        """
        Custom save method.
        """
        super(NeoBaseNode, self).save()




#     # traverse incoming IS_FROM relation, inflate to Person objects
#     #code = StringProperty(unique_index=True, required=True)
#     #inhabitant = RelationshipFrom('Person', 'IS_FROM')
# 
# 
# class Person(StructuredNode):
#     name = StringProperty(unique_index=True)
#     age = IntegerProperty(index=True, default=0)
# 
#     # traverse outgoing IS_FROM relations, inflate to Country objects
#     country = RelationshipTo(Country, 'IS_FROM')
