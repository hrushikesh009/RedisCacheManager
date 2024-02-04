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
    permission_classes = (AllowAny,)

    def get(self, request, device_id):
        try:
            device_id_key = f"device:{device_id}"
            cache_details = 'Cache Miss'

            redis_client = self.get_redis_client()

            if redis_client.exists(device_id_key):
                cache_details = 'Cache Hit'
                device_data = eval(redis_client.get(device_id_key))
            else:
                cache_details = 'Cache Miss'
                device_data = self.get_device_data_from_db(device_id)
                if device_data:
                    self.update_redis_cache(device_id_key, device_data)

            return Response({
                'device_id': device_id,
                'device_data': device_data,
                'message': 'Data Successfully retrieved!',
                'Cache Details': cache_details
            })

        except Exception as e:
            return self.handle_error(device_id, e)

    def get_redis_client(self):
        try:
            return redis.Redis(host=settings.REDIS_CONNECTION['host'], 
                               port=settings.REDIS_CONNECTION['port'], 
                               db=settings.REDIS_CONNECTION['db'])
        except redis.exceptions.ConnectionError:
            raise Exception('Unable to connect to Redis!')

    def get_device_data_from_db(self, device_id):
        device_data = DeviceLocationData.objects.filter(device_id=device_id).order_by('-timestamp').first()
        return {
            "latitude": device_data.latitude,
            "longitude": device_data.longitude,
            "timestamp": device_data.timestamp
        } if device_data else None

    def update_redis_cache(self, device_id_key, device_data):
        redis_client = self.get_redis_client()
        redis_client.setex(device_id_key, settings.EXPIRE_TIME, str(device_data))

    def handle_error(self, device_id, exception):
        print(exception)  # Log the information
        return Response({'device_id': device_id, 'message': "Error Occurred!"}, status=500)


class DeviceLocationView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, device_id):
        try:
            device_id_key = f"device:{device_id}"

            redis_client = self.get_redis_client()

            if redis_client.exists(device_id_key):
                cache_details = 'Cache Hit'
                device_data = eval(redis_client.get(device_id_key))
                end_location = {
                    "latitude": device_data['latitude'],
                    "longitude": device_data['longitude']
                } if device_data else None
            else:
                cache_details = 'Cache Miss'
                device_data = self.get_device_data_from_db(device_id)
                if device_data:
                    end_location = {
                        "latitude": device_data.latitude,
                        "longitude": device_data.longitude
                    }
                    self.update_redis_cache(device_id_key, device_data)

            start_location = self.get_start_location(device_id)

            return Response({
                'device_id': device_id,
                'start_location': start_location,
                'end_location': end_location,
                'message': 'Data Successfully retrieved!',
                'Cache Details': cache_details
            })

        except Exception as e:
            return self.handle_error(device_id, e)

    def get_start_location(self, device_id):
        device_data = DeviceLocationData.objects.filter(device_id=device_id).order_by('timestamp').first()
        return {
            "latitude": device_data.latitude,
            "longitude": device_data.longitude
        } if device_data else None


class DeviceLocationPointsView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, device_id):
        try:
            start_time_str = request.query_params.get('start_time')
            end_time_str = request.query_params.get('end_time')

            if not start_time_str or not end_time_str:
                return Response({'device_id': device_id, 'message': "Start and End time parameters required!"}, status=200)

            start_time, end_time = self.get_start_and_end_time(start_time_str, end_time_str)

            if start_time >= end_time:
                return Response({'device_id': device_id, 'message': "Start Time cannot be greater than or equal to End Time"}, status=200)

            location_points = self.get_location_points(device_id, start_time, end_time)

            if not location_points:
                return Response({
                    'device_id': device_id,
                    'message': 'Data Not Found',
                }, status=200)

            return Response({
                'device_id': device_id,
                'location_points': location_points,
                'message': 'Data Successfully retrieved!'
            })

        except Exception as e:
            return self.handle_error
