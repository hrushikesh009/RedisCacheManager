from django.db import models

class DeviceLocationData(models.Model):
    device_id = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField()

    class Meta:
        db_table = 'device_location_data'
