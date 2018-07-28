[![Python Support](https://img.shields.io/badge/python-3.4-blue.svg)]()
[![Codacy](https://api.codacy.com/project/badge/Grade/b5d7d584dfa14f9b82fded7a3f626631)](https://app.codacy.com/app/seLain/Arya?utm_source=github.com&utm_medium=referral&utm_content=seLain/Arya&utm_campaign=badger)
[![Code Health](https://landscape.io/github/seLain/Arya/master/landscape.svg?style=flat)](https://landscape.io/github/seLain/Arya/master)
[![Maintainability](https://api.codeclimate.com/v1/badges/ce9f30392b773895203c/maintainability)](https://codeclimate.com/github/seLain/Arya/maintainability)
[![Build](https://travis-ci.org/seLain/Arya.svg?branch=master)]()
[![Coverage Status](https://coveralls.io/repos/github/seLain/Arya/badge.svg)](https://coveralls.io/github/seLain/Arya)
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()

Development of an experimental kanban system

## Run

Under your virtual environment for Arya :

```
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver [IP:Port]
```

By default the server runs on http://localhost:8000

## Commands

By default, Ayra now supports following commands:

**create stage [stage_name]**

**delete stage [stage_name]**

**switch stage [stage_name] and stage [stage_name]**

**create task [task_name] in stage [stage_name]**

**delete task id=#[task_id]**

**move task id=#[task_id] to stage [stage_name]**

The commands explain themselves. It should be noticed that tasks are altered by ids not by names.

