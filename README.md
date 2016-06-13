#structure-api
[![Build Status](https://travis-ci.org/minireference/structure-api.svg?branch=master)](https://travis-ci.org/minireference/structure-api)

An API for the structure and dependencies between subjects, topics, and concepts.. Check out the project's [documentation](http://minireference.github.io/structure-api/).

# Prerequisites
- [virtualenv](https://virtualenv.pypa.io/en/latest/)
- [postgresql](http://www.postgresql.org/)
- [redis](http://redis.io/)
- [travis cli](http://blog.travis-ci.com/2013-01-14-new-client/)
- [heroku toolbelt](https://toolbelt.heroku.com/)

# Initialize the project
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

# Create Servers
By default the included fabfile will setup three environments:

- dev -- The bleeding edge of development
- qa -- For quality assurance testing
- prod -- For the live application

Create these servers on Heroku with:

```bash
fab init
```

# Automated Deployment
Deployment is handled via Travis. When builds pass Travis will automatically deploy that branch to Heroku. Enable this with:
```bash
travis encrypt $(heroku auth:token) --add deploy.api_key
```
