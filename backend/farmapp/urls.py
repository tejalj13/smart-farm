from django.urls import path
from . import views

urlpatterns = [
    path('api/sensor-data/', views.get_sensor_data),
    path('', views.dashboard),
    path('api/data/', views.receive_data),
]
