
Technical design specification
==============================

Graph data structures are well suited for representing connections between scientific
subjects, topics, and concepts. The goal of the STRUCTURE API is to create a
metadata service to be used as part of other educational software projects for:
  - Tagging by referring to the `path` (sting) of a particular subject, topic,
    concept, or educational standard, e.g., `tag='math/calculus/derivative'`
  - Graph browsing interfaces for tagged content collections
  - Representation for learner knowledge model by reference to paths, e.g.
    `learner.knowlge={'math/calculus/derivative':(0.9,0.1), ...}`, where the
    tuple `(0.9,0.1)` describes a learner who is 90% likely to be able to answer
    derivative questions questions, and our uncertainty of this estimate is ~10%.


Example browsing interface
--------------------------
The STRUCTURE API can be used to build a concept map browser application (Summer 2018)
that when rendering the page `/mechanics/kinematics` makes an API call to:

    /api/v1/nodes/miniref/mechanics/kinematics

and receives `json` data of the form: 

    {'id':
     'path':
     'name':
     'prerequisites': [{ node...}, {node...}, ],
     'contains':      [{ node...}, {node...}, ],
     'usedfor':       [{ node...}, {node...}, ],
    }

This is all the information needed to draw the concept map view zoomed in on the
topic Kinematics that shows the detail of kinematics topic in a big central div,
prerequisites as clickable links above, and applications of kinematics below.
See [about.md](./about.md) for an ASCII-drawn example browsing interface of this
concept.


Graph queries
-------------
We can foresee multiple types of graph queries for node data:
  1. Get object (serialize all references as UUIDs)
  2. Get object and links (serialize references to full json, references-in-references as UUIDs)
  3. Same as above but traverse 2-hops in graph
  4. Full traversal: `given node n, find ALL its prerequisites`

We can use a `hops=0` as default, `hops=1`, `hops=2`, etc. `hops=DFS` for full

TODO: think about use cases and performance implications (does GraphQL solve all this?).





Uncertainty reduction
---------------------
  - How to represent polymorphism in API (spec for json)
    - attributes all nodes must have?
    - `__class__` attribute exposed to fronted to know what type of node it is rendering



Conventions
-----------
Each element of the graph system (edges, vertices and their subclasses) must have
a `uuid` property (exposed as `id` to the frontend).

However, during the initial development process (May/June 2018) we'll maintain
the default auto-incrementing numeric ids for easier interactive debugging in
the Postgres DB shell. These "training wheels" will be removed in the final version
and all FK will be switched to use only `uuid`d.

