
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




Uncertainty reduction
---------------------
  - Can DRF use `neomodel` models?
  - Can DRF use `neolixir` models?


