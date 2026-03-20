from django.db import models


class SensorData(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    soil_moisture = models.FloatField()
    leaf_wetness = models.FloatField()
    light_intensity = models.FloatField()
    risk = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
