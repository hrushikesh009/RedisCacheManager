
import datetime

import pytz
import redis
from django.conf import settings
from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DeviceLocationData

India_tz = pytz.timezone("Asia/Kolkata")

class DeviceInfoView(APIView):
    """
    Extract Device Information
    """
    permission_classes = (AllowAny,)

    
    def get(self, request, device_id):
        try:
            device_id_key = f"device:{device_id}"
            cache_details = 'Cache Miss'
            try:
                redis_client = redis.Redis(host=f"{settings.REDIS_CONNECTION['host']}", port=f"{settings.REDIS_CONNECTION['port']}", db=f"{settings.REDIS_CONNECTION['db']}")
                redis_client.ping()
            except redis.exceptions.ConnectionError:
                return Response({
                    'message': 'Unable to connect to Redis!'
                })
            
            if redis_client.exists(device_id_key):
                """Cache Hit"""
                cache_details = 'Cache Hit'
                device_data = eval(redis_client.get(device_id_key))

            else:
                """Cache Miss"""
                cache_details = 'Cache Miss'
                device_data = DeviceLocationData.objects.filter(device_id = device_id).order_by('-timestamp').first()
                if device_data:

                    device_data ={
                        "latitude" : device_data.latitude,
                        "longitude" : device_data.longitude,
                        "timestamp" : device_data.timestamp
                    }
                    redis_client.setex(device_id_key,settings.EXPIRE_TIME, str(device_data))
    
                else:
                    return Response({
                        'device_id': device_id,
                        'message': 'Data Not Found'
                    },status=200)
                
            return Response({
                        'device_id': device_id,
                        'device_data': device_data,
                        'messgae': 'Data Successfully retrived!',
                        'Cache Details': cache_details
                        })
                
        except Exception as e:
            print(e)
            """Prefer Logging the Information"""
            return Response({'device_id': device_id, 'message': "Error Occured!"},status=500)
        

class DeviceLocationView(APIView):
    """
    Extract Device Start and End Location
    """
    permission_classes = (AllowAny,)

    
    def get(self, request, device_id):
        try:
            device_id_key = f"device:{device_id}"

            try:
                redis_client = redis.Redis(host=f"{settings.REDIS_CONNECTION['host']}", port=f"{settings.REDIS_CONNECTION['port']}", db=f"{settings.REDIS_CONNECTION['db']}")
                redis_client.ping()
            except redis.exceptions.ConnectionError:
                return Response({
                    'message': 'Unable to connect to Redis!'
                })

            
            if redis_client.exists(device_id_key):
                cache_details = 'Cache Hit'
                """Cache Hit"""
                #Get the latest data for the given device id as end_location
                device_data = eval(redis_client.get(device_id_key))
                if device_data:
                    end_location = {
                            "latitude": device_data['latitude'],
                            "longitude": device_data['longitude']
                            }
                
            else:
                """Cache Miss"""
                cache_details = 'Cache Miss'
                #If the data is expired or not present in the database retrive it from the database
                device_data = DeviceLocationData.objects.filter(device_id = device_id).order_by('-timestamp').first()
                if device_data:
                    end_location = {
                            "latitude": device_data.latitude,
                            "longitude": device_data.longitude
                            }

                    #Add the latest data against the device ID if expired!
                    device_data ={
                            "latitude" : device_data.latitude,
                            "longitude" : device_data.longitude,
                            "timestamp" : device_data.timestamp
                        }
                    redis_client.setex(device_id_key,settings.EXPIRE_TIME, str(device_data))
            
            #Retrive the start location of the device ID
            device_data = DeviceLocationData.objects.filter(device_id = device_id).order_by('timestamp').first()
            if device_data:
                start_location = {
                    "latitude": device_data.latitude,
                    "longitude": device_data.longitude
                        }
                
            if not device_data:
                return Response({
                            'device_id': device_id,
                            'message': 'Data Not Found',
                        },status=200)
            
            return Response({
                        'device_id': device_id,
                        'start_location': start_location,
                        'end_location': end_location,
                        'messgae': 'Data Successfully retrived!',
                        'Cache Details': cache_details,
                        })
                     
        except Exception as e:
            print(e)
            """Prefer Logging the Information"""
            return Response({'device_id': device_id, 'message': "Error Occured!"},status=500)
        

class DeviceLocationPointsView(APIView):
    """
    Extract Device Location Points
    """
    permission_classes = (AllowAny,)

    
    def get(self, request, device_id):
        try:
            start_time_str = request.query_params.get('start_time')
            end_time_str = request.query_params.get('end_time')
                                            
            if not start_time_str or not end_time_str:
                return Response({'device_id': device_id, 'message': "Start and End time parameters required!"},status=200)
            
            try:
                start_time = datetime.datetime.strptime(start_time_str.strip(), '%Y-%m-%dT%H:%M:%SZ')
                end_time = datetime.datetime.strptime(end_time_str.strip(), '%Y-%m-%dT%H:%M:%SZ')
            except Exception as e:
                return Response({
                        'device_id': device_id,
                        'messgae': "Unable to Extract Data! Please check the data format ex.'%Y-%m-%dT%H:%M:%SZ' "
                        })
            
            if start_time > end_time:
                return Response({'device_id': device_id, 'message': "Start Time cannot be greater than or equal to End Time"},status=200)

    

            location_points = DeviceLocationData.objects.values('latitude', 
                                                                'longitude', 
                                                                'timestamp')\
                            .filter((Q(timestamp__gte = start_time) & Q(timestamp__lte = end_time)),
                                    device_id=device_id)\
                            .order_by('-timestamp')

            if not location_points:
                return Response({
                            'device_id': device_id,
                            'message': 'Data Not Found',
                        },status=200)

            return Response({
                        'device_id': device_id,
                        'location_points': location_points,
                        'messgae': 'Data Successfully retrived!'
                        })

            
        except Exception as e:
            print(e)
            """Prefer Logging the Information"""
            return Response({'device_id': device_id, 'message': "Error Occured!"},status=500)


