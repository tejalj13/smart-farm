from django.urls import path
from .views import receive_data, dashboard

urlpatterns = [
    path('api/sensor-data/', receive_data),
    path('', dashboard),
]
