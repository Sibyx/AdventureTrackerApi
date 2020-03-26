# AdventureTracker API

[![Run in Insomnia}](https://insomnia.rest/images/run.svg)](https://insomnia.rest/run/?label=AdventureTracker%20API&uri=https%3A%2F%2Fgithub.com%2FSibyx%2FAdventureTrackerApi%2Fblob%2Fmaster%2Fdocs%2Fadventure_tracker_insomnia.json)

AdventureTracker is an open-source application for creating nice & shiny travel notes using simple mobile application.
Diaries are set of travel records coordinates, description, point-type and photos.

This repository contains application interface which provide authentication & data synchronization across all front-end
applications (mobile or web application).

The main idea is to create a free open-source platform with open-api to allow automation and custom data handling.

API is implemented as simple [Django](https://www.djangoproject.com/) for Python 3 with
[PostgreSQL](https://www.postgresql.org/) database for storage with [PostGIS](https://postgis.net/) extension for
geo-spatial operations.

We use GitHub stack for project management (Issues, Wiki, Milestones etc.)

Project code style is according to [PEP8](https://www.python.org/dev/peps/pep-0008/) and version control is applied
as [git-flow](https://datasift.github.io/gitflow/IntroducingGitFlow.html).

API specification is written using [API Blueprint](https://apiblueprint.org/) and we use
[snowboard](https://github.com/bukalapak/snowboard) to create HTML output. You can find these files in `_docs`
directory in project root.

## Installation

We use [poetry](https://python-poetry.org/) to manage virtual environments & dependencies, so installation is
simply done by typing `poetry install` inside of virtual environment of cloned repository.

Minimum system requirements:

- Python 3.7+ (because of [ISO8601 issue](https://bugs.python.org/issue15873))
- Pipenv
- PostgreSQL 10 + PostGIS
- NodeJS & Yarn (only for API blueprint docs)

### Database seed

Initial database data are provided in `core/fixtures/initial.json` and you can load them by executing
`python manage.py loaddata core/fixtures/initial.json`. This file is changing over the time to provide new basic default
values (or field localization for example).

**Development**

We use [django serializer](https://docs.djangoproject.com/en/3.0/howto/initial-data/) to create `initial.json`, if you
want to update this file, execute `python manage.py dumpdata --indent 2 -o core/fixtures/initial.json core.RecordType`.

Please always update the existing seed (do not replace primary keys).

## Libraries

- [Django](https://www.djangoproject.com/): Back-end framework
- [python-dotenv](https://github.com/theskumar/python-dotenv): Configuration using .env files
- [django-enum-choices](https://github.com/HackSoftware/django-enum-choices): Enum support for Django ORM
- [django-api-forms](https://github.com/Sibyx/django_api_forms): Request validation

---
With ❤️ Hobbits (c) 2019
