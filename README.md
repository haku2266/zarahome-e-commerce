# Zarahome E-Commerce
In this project, I was using **HTMX** as an AJAX alternative
As a database, I used **PostgreSQL**, and its search parameters
Docker Compose has been added

In order to run the project, use the following commands:

1. 
```shell
docker-compose up
```

2. 
```shell
docker-compose exec web python manage.py migrate
```

3.
```shell
docker-compose exec web python manage.py createsuperuser
```
