# Activities Backend

Backend app for recording tasks and activities performed in client companies, registering the people and vehicles assigned and the status of each one.

Built with Django 4 and Django Rest Framework, using Docker containers.

## Start Docker containers
```bash
make up
```

### Start shell of Django container
```bash
make shell
```

### Create a superuser
```bash
python manage.py createsuperuser
```

### Test app
```bash
python manage.py test --keepdb
```
