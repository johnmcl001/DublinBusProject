"""
Convert query results to json files
"""

from rest_framework import serializers
from .models import *


class MachineLearningInputs(object):
    """
    Create inputs objects for serialization
    """
    def __init__(self, time, day, month, date,stop_number, weather, routes, trips):
        self.time = time
        self.day = day
        self.date = date
        self.month = month
        self.stop_number = stop_number
        self.weather = weather
        self.routes = routes
        self.trips = trips


class MachineLearningInputSerializer(serializers.Serializer):
    """
    Serialize input data for machine learning
    """
    time = serializers.TimeField()
    day = serializers.CharField(max_length=10)
    month = serializers.CharField(max_length=2)
    date= serializers.DateField()
    stop_number = serializers.CharField(max_length=200)
    weather = serializers.DictField()
    routes = serializers.ListField(child=serializers.CharField(max_length=5))
    trips = serializers.DictField()


class StopSerializer(serializers.ModelSerializer):
    """
    Convert stop data from gtfs to json
    """
    class Meta:
        """
        Meta data for StopSerializer, model and what to return
        """
        model = Stops
        # Return more specific fields when we know what we want
        fields = "__all__"

class TouristSerializer(serializers.ModelSerializer):
    """
    Convert route data from gtfs to json
    """
    class Meta:
        """
        Meta data for RouteSerializer, model and what to return
        """
        model = Touristattractions
        fields = ["name", "description", "address", "image"]

class StopTimeSerializer(serializers.ModelSerializer):
    """
    Convert route data from gtfs to json
    """
    class Meta:
        """
        Meta data for RouteSerializer, model and what to return
        """
        model = StopTimes
        fields = "__all__"

class TripSerializer(serializers.ModelSerializer):
    """
    Convert route data from gtfs to json
    """
    class Meta:
        """
        Meta data for RouteSerializer, model and what to return
        """
        model = Trips
        fields = "__all__"
