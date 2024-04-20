# Zarahome E-Commerce

### `Django` project for learning purposes

#### -|- List of technologies utilized:

-   `HTMX` as a util to create dynamic components
-   `PostgreSQL` as a SQL database
-   `Docker & Docker-compose` for containerization
-   and more

#### -|- How to run the project:

_Clone the application to your local device_

```bash
git clone git@github.com:haku2266/zarahome-e-commerce.git
```

_Get into the app directory_

```bash
cd zarahome-e-commerce/
```

_Run docker-compose file_

``` bash
docker-compose up --build
```

_Apply migrations_
```bash
docker-compose exec web python manage.py migrate
```

_Create admin_
```bash
docker-compose exec web python manage.py createsuperuser
```

_Access the app through the next link_
1. For users:
**http://0.0.0.0:8000/**

3. For admin
**http://0.0.0.0:8000/admin/**

