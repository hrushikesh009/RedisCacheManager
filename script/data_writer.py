import datetime
import os
from pathlib import Path

import config
import pandas as pd
import pytz
from sqlalchemy import create_engine

tz = pytz.timezone('Asia/Kolkata')
engine = create_engine(config.DB_ENGINE) 

BASE_DIR = Path(__file__).resolve().parent.parent


def readexcel(excel_name):
    s_start = datetime.datetime.now(tz=tz)
    print("***********Reading Excel**************")

    filename_path = os.path.join(BASE_DIR,excel_name)

    file = pd.read_csv(filename_path).sort_values('sts')
    end = datetime.datetime.now(tz=tz)
    
    print("*******Excel read time***************"), end - s_start
    return file

def write_to_database(file):

    for index,row in file.iterrows():

        device_id = row['device_fk_id']
        latitude = row['latitude']
        longitude = row['longitude']
        timestamp_str = row['time_stamp']

        timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ')

        
        with engine.connect() as conn:
            conn.execute(f""" INSERT INTO device_location_data (device_id, latitude, longitude,timestamp) VALUES ('{device_id}', '{latitude}', '{longitude}',' {timestamp}');""")

    engine.dispose()

if __name__ == '__main__':
    file=readexcel('Raw_Data.csv')
    write_to_database(file)
    print("\n*******************************updation Done*******************************")



















# import redis
# import pandas as pd

# # Create a Redis cache server
# r = redis.Redis(host='localhost', port=6379, db=0)

# # Read the excel file and sort the data based on the sts column value
# data = pd.read_excel('Raw_Data.csv', index_col='sts',engine="openpyxl")
# data.sort_index(inplace=True)

# # Iterate over the sorted data
# for index, row in data.iterrows():
#     # Extract the device ID and the latest data based on the sts column value
#     device_id = row['device_fk_id']
#     latest_data = row.to_dict()
    
#     # Store the latest data (as per time stamp) of device against each device ID in Redis cache
#     r.hmset(device_id, latest_data)

# import pandas as pd
# import redis

# # Create a Redis client object
# redis_client = redis.Redis(host='localhost', port=6379, db=0)

# # Read the Excel file and sort the data by the sts column
# data = pd.read_csv('Raw_Data.csv').sort_values('sts')

# # Iterate over the rows of the sorted data
# for i, row in data.iterrows():
#     # Extract the device ID and device data from the row
#     device_id = row['device_fk_id']
#     device_data = row.to_dict()

#     # Check if the device ID exists in the Redis cache
#     if redis_client.exists(device_id):
#         # Retrieve the existing device data from the cache
#         existing_device_data = eval(redis_client.get(device_id))

#         # Compare the timestamps of the current and existing device data
#         if device_data['sts'] > existing_device_data['sts']:
#             # Update the value in the cache
#             redis_client.set(device_id, str(device_data))
#     else:
#         # Create a new key-value pair in the cache
#         redis_client.set(device_id, str(device_data))

# # Close the Redis connection
# redis_client.close()