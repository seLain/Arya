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