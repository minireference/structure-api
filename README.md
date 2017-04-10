STRUCTURE API
=============
An API for the structure and dependencies between subjects, topics, and concepts.

<!-- [![Build Status](https://travis-ci.org/minireference/structure-api.svg?branch=master)](https://travis-ci.org/minireference/structure-api) -->
<!-- Check out the project's [documentation](http://minireference.github.io/structure-api/). -->



TODOs
-----
  - Implrmrny Subject, Topic, and Concept Nodes in both backends
  - Preprocess common core node data
  - Import common core edge data (from .csv)
  - Think about Polymorphism for nesting in serilizers and in wire format
  - Implement session middleware no will not have to call .save manually (except when need auto-id field to be generated)
    http://stackoverflow.com/questions/6606725/best-way-to-integrate-sqlalchemy-into-a-django-project
  - Export parts of graph to CmapTools format






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
pg_ctl -D /usr/local/var/postgres/ start
createdb struct
```


