from __future__ import unicode_literals
import uuid

import neolixir

class NeolixirBaseNode(neolixir.Node):
    """
    BaseNode that is extended by SubjectNode, TopicNode, and ConceptNode.
    """
    # `id`      Integer propery handled by neolixir
    uuid        = neolixir.String(default=uuid.uuid4)
    path        = neolixir.String()
    scope       = neolixir.String(default='miniref')
    version     = neolixir.String(default='0.1')
    created_at  = neolixir.DateTime()
    modified_at = neolixir.DateTime()
    comment     = neolixir.String()
