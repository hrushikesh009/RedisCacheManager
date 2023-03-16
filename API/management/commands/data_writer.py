
import os
from pathlib import Path

import pandas as pd

from django.core.management.base import BaseCommand
import datetime

from API.models import DeviceLocationData

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Command(BaseCommand):
    help = "Populate Database"

    def handle(self, *args, **options):
        
        """Input your file path"""
        filename_path = os.path.join(BASE_DIR,'Raw_Data.csv')

        file = pd.read_csv(filename_path).sort_values('sts')

        count = 0
        for index,row in file.iterrows():
            try:
                device_id = row['device_fk_id']
                latitude = row['latitude']
                longitude = row['longitude']
                timestamp_str = row['time_stamp']

                timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ')  

                object = DeviceLocationData(
                                device_id=device_id, 
                                latitude=latitude, 
                                longitude=longitude,
                                timestamp = timestamp
                            )
                object.save()
                count +=1
            except Exception as e:
                print(e)
                print("Unable to Save data")
                """Preferabel logg or save the certain file"""

        print(f'{count} value was written to the database')
        
        
    
        
        
                    
