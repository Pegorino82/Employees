# Employees

##  starting with docker

1. git clone https://github.com/Pegorino82/Employees.git
2. docker-compose build
3. docker-compose up

#### for create superuser or/and fill db with test data:
1. git clone https://github.com/Pegorino82/Employees.git
2. docker-compose build
3. docker-compose start
4. docker-compose exec server python manage.py fill_units
5. docker-compose exec server python manage.py fill_employees
6. docker-compose exec server python manage.py createsuperuser
7. docker-compose up


## if starting on local server add local_settings.py with 

    DEBUG = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'employees',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': 5432
        }
    }

and fill DATABASES according your postgres
## Then do:
1. `pip install -r requirements.txt`
2. `python manage.py makemigrations`
3. `python manage.py migrate`
4. `python manage.py fill_units [-a]` - to fill db with test units, flag -a to set amount, default 10
5. `python manage.py fill_employees [-a]` - to fill db with test employees, flag -a to set amount, default 300
6. `python manage.py runserver`

start page on 127.0.0.1:8000

to have ability to use django admin run `python manage.py createsuperuser`

