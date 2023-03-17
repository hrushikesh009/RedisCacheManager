# Intro

This is a simple Redis Cache based Django demonstration that will help you get started with basic of the Redis and Django Application!

# Requirements

- Python 3.0
- Make sure you have pip (pip --version)
- pip install virtualenv to install virtual environment


## What to do

To get this running, you need the following. First install dependencies

### Step 0 : Clone the Repository

`git clone https://github.com/hrushikesh009/RedisCacheManager.git`


### Step 1 : Install dependencies

`pip install -r requirements.txt`

### Step 2 : Database Setup

In this tutorial, I utilized the Postgres Database as I already had Postgres client setup. You are free to choose the Database based on your own priority.

You have to install the postgres client and set up a simple database with user and password privileges

`DATABASES = {

    'default': {
    
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        
        'NAME': 'Your Database Name',
        
        'HOST': 'localhost', # usually its localhost but if you have a cloud host specific it over here
        
        'USER': 'Database Username',
        
        'PASSWORD': Database Passwordd,
        
        'PORT': 'Database Port'
        
    }
}`

Below link helps in setting up django with a simple postgres Database
https://stackpython.medium.com/how-to-start-django-project-with-a-database-postgresql-aaa1d74659d8

### Step 3: Database Creation

Use the Below command to connect to the postgres instance

`sudo -u postgres psql`

First, create a database for your project:

`CREATE DATABASE <DATABASE NAME>;`

Run Below Commands to grant PRIVILEGES

`CREATE USER <USER> WITH PASSWORD '<PASSWORD>';`

`ALTER ROLE<USER> SET client_encoding TO 'utf8';`
`ALTER ROLE <USER> SET default_transaction_isolation TO 'read committed';`
`ALTER ROLE <USER> SET timezone TO 'UTC';`
 
`GRANT ALL PRIVILEGES ON DATABASE <DATABASE NAME> TO <USER>;`

### Step 4: Set up Redis Client

Under the settings.py placed in RedisCacheManager
`redis_connection = {
    'host':<HOST NAME>,
    'port': <PORT>,
    'db': <DATABASE>
}`

### Step 5 : Run migrations

`python manage.py makemigrations`

`python manage.py migrate`

This will setup all the necessary tables.

### Step 6: Populate Database

Below commands will populated database with raw data to work with Redis Examples!

`python manage.py write_data_to_redis`

`python manage.py data_writer`

### Step 7 : Start the local server

And start the server with 

`python manage.py runserver`

### Step 8: Play with the Endpoints

Provide Device Latest Information
`'device_info/<str:device_id>/'` 

Provides Start and End Location of the Device
`device_start_end_location/<str:device_id>/`

Provides Data Location Points based on Time range
`device_location_points/<str:device_id>/`

Above endpoints require
- start_time
- end_time

as query paramter to provide information





