# Arya
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

