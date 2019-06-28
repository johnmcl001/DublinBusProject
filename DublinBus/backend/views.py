"""
Create views here
Don't need to worry about rendering
Mostly just create the logic for the machine learning
"""

from django.shortcuts import HttpResponse
from rest_framework import viewsets
from rest_framework import views
from rest_framework.response import Response
from django_downloadview import setup_view


from .serializers import *
from .models import *


class SearchByStop(views.APIView):
    """
    Search by stop feature
    """

    def get(self, request):
        """
        Input: HTTP request
        Output: Machine learning output as json
        Note: Main logic implemented here using the methods below
        """
        stop_number = self.get_params("stopnumber")
        time = self.get_params("time")
        day = self.get_params("day")
        weather = self.get_weather(time, day)
        routes = self.get_routes(stop_number)
        direction = self.get_direction(stop_number, routes)
        machine_learning_inputs = self.serialize_machine_learning_input(
            stop_number, weather, routes, direction,
        )
        output = self.get_arrival_times(machine_learning_inputs)
        results = self.serialize_machine_learning_output(output)
        return Response(stop_number)

    def get_params(self, target):
        """
        input: params from url
        output: desired param as string
        """
        param = self.request.get(target, None)
        return param

    def get_weather(self, time, date):
        """
        Input: time and date
        Output: weather conditions for prediction as json or dictionary
        """
        weather = "Weather API results for time and date"
        return weather

    def get_routes(self, stop_number):
        """
        Input: bus stop number
        Output: List of Routes that server that bus stop as list
        """
        routes = "select all routes from routes where stop = bus_stop_number"
        return routes

    def get_direction(self, route_number, stop_number):
        """
        Input: bus stop number and route_number
        Output: Direction of route as int
        Note: Only have to do this for 1 route since it's same for each
        """
        direction = "select direction from stops/routes where route = route_number and stop = stop_number"
        return direction

    def serialize_machine_learning_input(self, stop_number, weather, routes, direction):
        """
        Input: weather data as json/dict, routes as list, direction as int
        Output: machine learning inputs as json

        """
        machine_learning_inputs = "Serializer"
        return machine_learning_inputs

    def get_arrival_times(self, machine_learning_inputs):
        """
        Input: machine learning inputs as json
        Output: machine learning predictions as dictionary/json
        Note: output format depends on if we serialize here or somewhere else
        """
        predictions = []
        return predictions

    def serialize_machine_learning_output(self, machine_learning_results):
        """
        Input: Machine learning results
        Output: Machine learning results as json
        """
        results_as_json = "json"
        return results_as_json

class SearchByRoute(SearchByStop):
    """
    Search by route feature
    Inherits from search by stop
    """
    def get(self, request):
        return HttpResponse("<h1>SearchByRoute</h1>")

class SearchByDestination(SearchByStop):
    """
    Search by destination feature
    Inherits from search by stop
    """
    def get(self, request):
        return HttpResponse("<h1>SearchByDestination</h1>")

# Just lets us view the data base in a web ui
# Also useful for testing sometimes
# Get list with localhost:8000/api

# Will probably remove at the end


class StopsView(viewsets.ModelViewSet):
    """
    Shows stops table
    """
    queryset = Stops.objects.all()
    serializer_class = StopsSerializer

class RoutesView(viewsets.ModelViewSet):
    """
    Shows routes table
    """
    queryset = Routes.objects.all()
    serializer_class = RoutesSerializer


class StopTimesView(viewsets.ModelViewSet):
    """
    Shows stoptimes table
    """
    queryset = StopTimes.objects.all()
    serializer_class = StopTimesSerializer


class TripsView(viewsets.ModelViewSet):
    """
    shows trips table
    """
    queryset = Trips.objects.all()
    serializer_class = TripsSerializer
