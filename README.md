STRUCTURE API
=============
An API for the structure and dependencies between subjects, topics, and concepts.

<!-- [![Build Status](https://travis-ci.org/minireference/structure-api.svg?branch=master)](https://travis-ci.org/minireference/structure-api) -->
<!-- Check out the project's [documentation](http://minireference.github.io/structure-api/). -->


Design TL;DR
------------
  - Graph data structure with specialized tooling for repesenting educaitonal content domain
  - Decision: stick to Django ORM (no neo4j for now)


Project milestones
------------------
  - Milestone 1: import state from `data/**.yaml` [2017]
  - Milestone 2: export state (DRF YAML serializer or custom?)
  - Milestone 3: ETL for internal representaion to feel and metacademy
  - Milestone 4: basic graph display UI (stretch goals, seatch and faceted filtering)
  - Milestone 5: graph editing frontend
  - Milestone 6: example applications that make use of sturcture-api (concept map browser, learning pathway recommendations, 



TODOs
-----
  - Finalize BaseNode
  - Implement Subject, Topic, and Concept Nodes in both backends
  - Preprocess common core node data
  - Import common core edge data (from .csv)
  - Think about Polymorphism for nesting in serilizers and in wire format
  - Implement session middleware no will not have to call .save manually (except when need auto-id field to be generated)
    http://stackoverflow.com/questions/6606725/best-way-to-integrate-sqlalchemy-into-a-django-project
  - Export parts of graph to CmapTools format
  - Export to feel format
  - Export to metacademy format
  - Dockerize for prod (docker-compose and docker-host)






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


Export data using command:



