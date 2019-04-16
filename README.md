# Employees

if starting on local server add local_settings.py with 

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
Then do:
1. pip install -r requirements.txt
2. python manage.py makemigrations
3. python manage.py migrate
4. python manage.py fill_units [-a] - to fill db with test units, flag -a to set amount, default 10
5. python manage.py fill_employees [-a] - to fill db with test employees, flag -a to set amount, default 300
6. python manage.py runserver
start page on 127.0.0.1:8000

