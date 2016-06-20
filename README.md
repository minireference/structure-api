STRUCTURE API
=============
An API for the structure and dependencies between subjects, topics, and concepts.

<!-- [![Build Status](https://travis-ci.org/minireference/structure-api.svg?branch=master)](https://travis-ci.org/minireference/structure-api) -->
<!-- Check out the project's [documentation](http://minireference.github.io/structure-api/). -->


TODOs
-----
  - Implement Relations in three backends 
  - Implement nested Serizlizers 
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
- [redis](http://redis.io/)
- [travis cli](http://blog.travis-ci.com/2013-01-14-new-client/)
- [heroku toolbelt](https://toolbelt.heroku.com/)

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
Create the database:

```bash
createdb struct
```
Initialize the git repository

```
git init
git remote add origin git@github.com:minireference/structure-api.git
```

Migrate the database and create a superuser:
```bash
python struct/manage.py migrate
python struct/manage.py createsuperuser
```

Run the development server: 
```bash
python struct/manage.py runserver
```

## Create Servers
By default the included fabfile will setup three environments:

- dev -- The bleeding edge of development
- qa -- For quality assurance testing
- prod -- For the live application

Create these servers on Heroku with:

```bash
fab init
```

## Automated Deployment
Deployment is handled via Travis. When builds pass Travis will automatically deploy that branch to Heroku. Enable this with:
```bash
travis encrypt $(heroku auth:token) --add deploy.api_key
```

