from django.db import models


# Create your models here.
class Waypoint(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)


class Area(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField()
    name = models.CharField(max_length=100)
