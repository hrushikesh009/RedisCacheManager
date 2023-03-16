import os
from pathlib import Path
import pandas as pd
import datetime
import redis
from django.core.management.base import BaseCommand

from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Create a Redis cache server
redis_client = redis.Redis(host='localhost', port=6379, db=0)

class Command(BaseCommand):
    help = "Populate Database"

    def handle(self, *args, **options):

        # Read the excel file and sort the data based on the sts column value
        filename_path = os.path.join(BASE_DIR,'Raw_Data.csv')

        data = pd.read_csv(filename_path).sort_values('sts')

        # Iterate over the sorted data
        for index, row in data.iterrows():
            
            # Extract the device ID and the useful information
            device_id = f"device:{row['device_fk_id']}"
            latitude = row['latitude']
            longitude = row['longitude']
            timestamp_str = row['time_stamp']

            timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ')         
            value ={
                "latitude" : latitude,
                "longitude" : longitude,
                "timestamp" : timestamp
            }

            
            
            #Check if the device ID exists in the Redis cache
            if redis_client.exists(device_id):
                existing_device_data = eval(redis_client.get(device_id))

        
                # Compare the timestamps of the current and existing device data

                if timestamp > existing_device_data['timestamp']:
                    redis_client.setex(device_id,settings.EXPIRE_TIME, str(value))
            else:
                # Create a new key-value pair in the cache
                redis_client.setex(device_id,settings.EXPIRE_TIME, str(value))

        redis_client.close()




            

