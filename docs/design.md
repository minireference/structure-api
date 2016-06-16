
Technial design specification
=============================

A graph datastore like neo4j is well suited for representing connections
between scientific subjects, topics, and concepts.

The goal of the STRUCTURE project is to create a "structure API" that can
be used from other projects, through a REST interface.


Example use case
----------------

A concept map webapp, when rendering the page /mechanics/kinematics can make
a single call to:

    struct /api/v1/nodes/mechanics/kinematics

and receive a json 

    {'id':
     'path':
     'name':
     'contains':      [{ node...}, {node...}, ],
     'prerequisites': [{ node...}, {node...}, ],
     'usedfor':       [{ node...}, {node...}, ],
    }

which is all the information needed to draw a "local" concept map of Kinematics,
showing prerequisites as clickable links above,
detail of kinematics topic in center, and applications of kinematics below.

Multiple types of node queries:

  1. Get object (serizlize all references as UUIDs)
  2. Get object and links (serizlize refeences to full json, references-in-references as UUIDs)
  3. Same as above but traverse 2-hops in graph
  4. Full traversal:
     given node n, find ALL its prerequisites

We can use a `hops=0` as default, `hops=1`, `hops=2`, etc. `hops=DFS` for full




Uncertainty reduction
---------------------
  - How to represent polymorphism in API (spec for json)
    - attributes all nodes must have
    - attirbutes 
  - Relations and poly in `neomodel` models?
  - Relations and poly in `neolixir` models?




