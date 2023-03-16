from django.urls import path
from .views import DeviceInfoView,DeviceLocationView,DeviceLocationPointsView
urlpatterns = [
    path('device_info/<str:device_id>/', DeviceInfoView.as_view(), name='device-info'),
    path('device_start_end_location/<str:device_id>/', DeviceLocationView.as_view(), name='device-start-end-location'),
    path('device_location_points/<str:device_id>/', DeviceLocationPointsView.as_view(), name='device-location-points'),


]