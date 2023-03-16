# Intro

This is a simple bot that says yo-mama jokes borrowing heavilly from https://github.com/abhay1/django-facebook-messenger-bot-tutorial and the accompanying tutorial.

# Requirements

- Python 3.0
- Make sure you have pip (pip --version)
- pip install virtualenv to install virtual environment
- Telegram messenger (you can also use the web version at web.telegram.org)

### Sample Video

https://drive.google.com/drive/folders/1o0xK000ZToAbwljM81HhWx5-JplOcNft?usp=sharing


## What to do

To get this running, you need the following. First install dependencies

### Step 0 : Clone the Repository

`git clone https://github.com/hrushikesh009/TelegramBot.git`


### Step 1 : Install dependencies

`pip install -r requirements.txt`

### Step 2 : Database Setup

In this tutorial, I utilized the MySQL Database as I already had MySQL client setup. You are free to choose the Database based on your own priority.

You have to install the Mysql client and set up a simple database with user and password privileges

`DATABASES = {

    'default': {
    
        'ENGINE': 'django.db.backends.mysql',
        
        'NAME': 'Your Database Name',
        
        'HOST': 'localhost', # usually its localhost but if you have a cloud host specific it over here
        
        'USER': 'Database Username',
        
        'PASSWORD': Database Passwordd,
        
        'PORT': 'Database Port'
        
    }
}`

Below link helps in setting up django with a simple postgres Database
https://stackpython.medium.com/how-to-start-django-project-with-a-database-postgresql-aaa1d74659d8

### Step 3 : Run migrations

`python manage.py makemigrations`

`python manage.py migrate`

This will setup all the necessary tables.

### Step 4 : Start the local server

And start the server with 

`python manage.py runserver`

### Step 5 : Download and use ngrok

You need an HTTPS url for most webhooks for bots to work. For purely development purposes you can use ngrok. It gives a web-accessible HTTPS url that tunnels through to your localhost.
Download ngrok (https://ngrok.com/)  , got to a new tab on your terminal and start it with 

`ngrok http 8000`

At this point, you will have to add the URLs to ALLOWED_HOSTS in `Telegram_Bot.settings`.

### Step 6 : Talk to the BotFather and get and set your bot token

Start telegram, and search for the Botfather. Talk to the Botfather on Telegram and give the command `/newbot` to create a bot and follow the instructions to get a token.

Copy the token and paste in `FunBot/views.py`

### Step 7 : Set your webhook by sending a post request to the Telegram API

If you are on a system where you can run a curl command, run the following command in your terminal (Remember to replace ngrok_url and bot_token)

`curl -F “url=<ngrok_url>/chat/c817304a3d163ebd58b44dd446eba29572300724098cdbca1a/“ https://api.telegram.org/bot<bot_token>/setWebhook`

Alternatively, you can use some service like Postman or hurl.it just remember to do the following:

- Request type is "POST"
- url to post to https://api.telegram.org/bot<bot_token>/setWebhook
- as parameters add this (name, value) pair: (url, <ngrok_url>/chat/c817304a3d163ebd58b44dd446eba29572300724098cdbca1a/)

You should get a response that states that "webhook has been set"

### Step 8 : Talk to the bot

You should now be able to talk to the bot and get responses from it

### Step 9: Capture the ClickStream

Once the Users start interacting with the bot the data will be captured in the database.

If you visit `url = <ngrok_url>/chat/home/` 

You would be able to view all the users using your bot and their interactions with the bot.



