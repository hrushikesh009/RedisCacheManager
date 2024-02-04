# RedisCacheManager

## Introduction

RedisCacheManager is a Django application demonstrating the integration of Redis caching for efficient data retrieval. It focuses on providing device information, start and end locations, and location points based on time range.

## Requirements

- Python 3.0
- Ensure pip is installed (`pip --version`)
- Install virtual environment: `pip install virtualenv`

## Getting Started

To run this application, follow these steps:

### Step 0: Clone the Repository

```sh
git clone https://github.com/hrushikesh009/RedisCacheManager.git
```

### Step 1: Install Dependencies

```sh
pip install -r requirements.txt
```

### Step 2: Database Setup

Utilizing Postgres Database in this tutorial, modify the settings in `RedisCacheManager/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'Your Database Name',
        'HOST': 'localhost',
        'USER': 'Database Username',
        'PASSWORD': 'Database Password',
        'PORT': 'Database Port'
    }
}
```

Refer to [this link](https://stackpython.medium.com/how-to-start-django-project-with-a-database-postgresql-aaa1d74659d8) for PostgreSQL setup.

### Step 3: Database Creation

Use the following commands to connect to the PostgreSQL instance:

```sh
sudo -u postgres psql
```

Create a database for your project:

```sh
CREATE DATABASE <DATABASE NAME>;
```

Run the following commands to grant privileges:

```sh
CREATE USER <USER> WITH PASSWORD '<PASSWORD>';
ALTER ROLE<USER> SET client_encoding TO 'utf8';
ALTER ROLE <USER> SET default_transaction_isolation TO 'read committed';
ALTER ROLE <USER> SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE <DATABASE NAME> TO <USER>;
```

### Step 4: Set up Redis Client

In `RedisCacheManager/settings.py`, configure the Redis connection:

```python
redis_connection = {
    'host': '<HOST NAME>',
    'port': '<PORT>',
    'db': '<DATABASE>'
}
```

### Step 5: Run Migrations

```sh
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Populate Database

Run the following commands to populate the database with raw data:

```sh
python manage.py write_data_to_redis
python manage.py data_writer
```

### Step 7: Start the Local Server

```sh
python manage.py runserver
```

### Step 8: Explore Endpoints

- Provide Device Latest Information: `device_info/<str:device_id>/`
- Get Device Start and End Location: `device_start_end_location/<str:device_id>/`
- Retrieve Device Location Points based on Time Range: `device_location_points/<str:device_id>/`

These endpoints require `start_time` and `end_time` as query parameters to provide information.