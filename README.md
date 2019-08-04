# AdventureTracker API

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

We use [pipenv](https://github.com/pypa/pipenv) to manage virtual environments & dependencies, so installation is
simply done by typing `pipenv install` in cloned repository. 

Minimum system requirements:

- Python 3.6
- Pipenv
- PostgreSQL 10 + PostGIS
- NodeJS & Yarn (only for API blueprint docs)

## Libraries

- [Django](https://www.djangoproject.com/): Back-end framework
- [python-dotenv](https://github.com/theskumar/python-dotenv): Configuration using .env files
- [django-enumfield](https://github.com/5monkeys/django-enumfield): Enum support for Django ORM
- 

---
With ❤️ Hobbits (c) 2019