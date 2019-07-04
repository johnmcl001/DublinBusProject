"""
Convert query results to json files
"""

from rest_framework import serializers
from .models import *


class MachineLearningInputs(object):
    """
    Create inputs objects for serialization
    """
    def __init__(self, stop_number, weather, routes, direction):
        self.stop_number = stop_number
        self.weather = weather
        self.routes = routes
        self.direction = direction


class MachineLearningInputSerializer(serializers.Serializer):
    """
    Serialize input data for machine learning
    """
    stop_number = serializers.CharField(max_length=200)
    weather = serializers.DictField()
    routes = serializers.ListField(child=serializers.CharField(max_length=5))
    direction = serializers.IntegerField(min_value=0, max_value=1)


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

class RouteSerializer(serializers.ModelSerializer):
    """
    Convert route data from gtfs to json
    """
    class Meta:
        """
        Meta data for RouteSerializer, model and what to return
        """
        model = Routes
        fields = "__all__"

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
