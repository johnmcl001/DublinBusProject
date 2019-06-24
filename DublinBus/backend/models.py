# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Routes(models.Model):
    """
    Model for gtfs routes.txt
    """
    route_id = models.CharField(primary_key=True, max_length=45)
    route_type = models.IntegerField(blank=True, null=True)
    agency_id = models.CharField(max_length=45, blank=True, null=True)
    route_short_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'routes'


class Stops(models.Model):
    """
    Model for gtfs stops.txt
    """
    index = models.BigIntegerField(blank=True, primary_key=True)
    stop_lat = models.FloatField(blank=True, null=True)
    zone_id = models.FloatField(blank=True, null=True)
    stop_lon = models.FloatField(blank=True, null=True)
    stop_id = models.TextField(blank=True, null=True)
    stop_name = models.TextField(blank=True, null=True)
    location_type = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stops'


class Test(models.Model):
    c1 = models.IntegerField(primary_key=True)
    c2 = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'test'
