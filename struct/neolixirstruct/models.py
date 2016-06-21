from __future__ import unicode_literals
import uuid

import neolixir


class NeolixirDependencyRelation(neolixir.Relationship):
    """
    Represents `(m)<--prerequisite--(n)` relations (implies (m)--usedfor-->(n)).
    """
    # id, _start, _end  =  automatically created
    __rel_type__ = 'prerequisite'
    explain_prerequisite = neolixir.String()
    explain_usedfor      = neolixir.String()
    level                = neolixir.String()


class NeolixirBaseNode(neolixir.Node):
    """
    BaseNode that is extended by SubjectNode, TopicNode, and ConceptNode.
    """
    # `id`      Autoincrementing Integer propery handled by neolixir
    uuid        = neolixir.String(default=uuid.uuid4)
    path        = neolixir.String()
    scope       = neolixir.String(default='miniref')
    version     = neolixir.String(default='0.1')
    created_at  = neolixir.DateTime()
    modified_at = neolixir.DateTime()
    comment     = neolixir.String()
    
    prerequisites = neolixir.RelOut(NeolixirDependencyRelation)
    usedfors      = neolixir.RelIn(NeolixirDependencyRelation)
