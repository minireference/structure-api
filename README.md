STRUCTURE API
=============
An API for the structure and dependencies between subjects, topics, and concepts.



  TODOs
  -----
    - Finalize BaseNode, and add BaseEdge
    - Cleanup settings/requirements
    - Think about Polymorphism for nesting in serializers and in wire format
    - Implement session middleware no will not have to call .save manually (except when need auto-id field to be generated)
      http://stackoverflow.com/questions/6606725/best-way-to-integrate-sqlalchemy-into-a-django-project
    - Dockerize for prod (docker-compose and docker-host)
    - figure out a way to speedup query for http://127.0.0.1:8000/api/v1/nodes/
      takes too long and we have 700 nodes and 500 rel'ns.
    - Handle `alias` properties
    - Store `source_file`(str) and `file_order` (float) along with data items in
      order to reproduce YAML identically after roundtrip


Design TL;DR
------------
  - Graph data structure with specialized tooling for representing educational content domain
  - Decision: stick to Django ORM (no neo4j for now)


New roadmap:
 - update backend models with a complete graph model (without miniref or CC specifics)
 - make sure tree tructures fit nicely in graphs
   Treebeard or MPTT nodes -- as an option 
 - Graph viz: reproduce [concept-coaster](https://github.com/pixyj/feel) and metacademy frontends
 - Alignment interface prototype:
   - two pane based on search
 - Search backend (depends on search R&D project for files)



Project milestones
------------------

  - Milestone 1: proof of concept [Ivan]
    - Tasks:
      - Import state from `data/**.yaml` [2017]
      - Refactor graph models into abstract `BaseNode` and `BaseEdge` and implement
        education related models:
          - `Node` with `kind in [subject, topic, concept, ...]`
          - `DependencyEdge`
          - `RelatedEdge`
          - `ContainsEdge`
      - Export state using
        [DRF YAML serializer](http://jpadilla.github.io/django-rest-framework-yaml/)
    - Technical challenges:
      - Is round-trip possible (choose sort, control YAML formatting)
      - How to deal with missing FKs during import (import queue?)

  - Milestone 2: ETL for internal representation to other platforms
    - Goal 1: Obtain a graph viz without too much custom work
    - Goal 2: Learn about feel and metacademy data models to inform what will be needed
    - Tasks:
      - Export structure-api data to feel fixtues format, import in feel instance
      - Export data to metacademy fixtures format
      - Export parts of graph to [CmapTools format](http://cmap.ihmc.us/xml/CXL.html) ?

  - Milestone 3: basic graph display UI
    - React
    - Technology research:
      - GraphQL to talk to backend?
    - Stretch goals:
      - search and faceted

  - Milestone 4: graph editing
    - Goal: create a graph editing interface for non-technical teachers to create
      educational graphs (concept maps) for students
    - Technology research:
      - GraphQL
      - [jsPlumb](https://jsplumbtoolkit.com/demos/toolkit/database-visualizer/index.html)? 

  - Milestone 6: example applications that make use of sturcture-api
    - [subject/topic browser](https://github.com/minireference/structure-api/blob/master/docs/about.md#browsing)
    - [learning pathway recommendations](https://github.com/minireference/structure-api/blob/master/docs/about.md#content-recommendation)








# Installation

## Prerequisites
- [virtualenv](https://virtualenv.pypa.io/en/latest/)
- [postgresql](http://www.postgresql.org/)



## Initialize the project
Create and activate a virtualenv:

```bash
virtualenv env
source env/bin/activate
```


Install dependencies:

```bash
pip install -r requirements/local.txt
```

Start Postgres and create the database:

```bash
mkdir postgres_data
initdb /Users/ivan/Projects/Minireference/STRUCTURE/structure-api/postgres_data
pg_ctl -D /Users/ivan/Projects/Minireference/STRUCTURE/structure-api/postgres_data start
createdb struct

# to stop
# pg_ctl -D /Users/ivan/Projects/Minireference/STRUCTURE/structure-api/postgres_data stop
```


Importing and exporting graph data
----------------------------------
Currently (May 5) we have the following data fixtures;

```
data/
├── README.md
├── ccssm                                       # Common Core State Standard for Math
│   ├── 1.yml
│   ├── 2.yml
│   ├── 3.yml
│   ├── 4.yml
│   ├── 5.yml
│   ├── 6.yml
│   ├── 7.yml
│   ├── 8.yml
│   ├── HSA.yml
│   ├── HSF.yml
│   ├── HSG.yml
│   ├── HSN.yml
│   ├── HSS.yml
│   ├── K.yml
│   ├── context.yml
│   ├── domain.yml
│   ├── practice.yml
│   └── standard.yml
└── miniref                                     # [WIP] data entry for Minireferece Co. concept maps
    ├── context.yml
    ├── math.yml
    └── physics.yml
```


Load data using command:

    ./struct/manage.py loadfromyamldata data/miniref/
    ./struct/manage.py loadfromyamldata data/ccssm/


Export data using command:

    Not implemented yet

