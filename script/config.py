import os

import pytz
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

#fetching the db_key
db_pass = os.getenv("DB_PASS")

tz = pytz.timezone('Asia/Kolkata')

DB_SETTINGS = {'host': 'localhost',
               'user': 'root',
               'password': db_pass,
               'db_name': 'carnot',
               'port': 3306
               }



DB_ENGINE = create_engine(f"mysql://{DB_SETTINGS['user']}:{DB_SETTINGS['password']}@{DB_SETTINGS['host']}:{DB_SETTINGS['port']}/{DB_SETTINGS['db_name']}")
print(DB_ENGINE)
# db_engine = create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(user, pass, host, port, db))



