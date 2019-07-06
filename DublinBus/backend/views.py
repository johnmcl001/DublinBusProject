"""
Create views here
Don't need to worry about rendering
Mostly just create the logic for the machine learning
"""

from django.shortcuts import HttpResponse
from rest_framework import viewsets
from rest_framework import views
from rest_framework.response import Response
import json
import os
from rest_framework import generics

#import pymysql
from datetime import datetime, timedelta


dirname = os.path.dirname(__file__)

from .serializers import *
from .models import *

#from .permissions import ApiPermissions

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
        date = self.get_params("date")
        weather = self.get_weather(time, date)
        bus_stop_info = self.get_bus_stop_info(stop_number)
        routes = bus_stop_info["routes"][0]
        directions = self.get_direction(routes, stop_number)
        return Response(directions)
        machine_learning_inputs = self.serialize_machine_learning_input(
                                                                stop_number,
                                                                weather,
                                                                routes,
                                                                directions)
        return Response(machine_learning_inputs)
        results = self.get_arrival_times(machine_learning_inputs)
        results = self.sort_results(results)
        return Response(results)

    def get_params(self, target):
        """
        input: params from url
        output: desired param as string
        """
        param = self.request.GET.get(target, None)
        return param

    def get_weather(self, time, date):
        """
        Input: time and date as strings
        Output: weather conditions for prediction as json or dictionary
        """
        weatherResult=Forecast.objects.get(date=date, start_time__lte=time, end_time__gt=time)
        forecast = {
            "temperature": weatherResult.temperature,
            "cloud": weatherResult.cloud_percent,
            "rain": weatherResult.rain,
            "description": weatherResult.description,
        }
        return forecast

    def get_bus_stop_info(self, stop_number):
        """
        Input: bus stop number as a string
        Output: List of Routes that server that bus stop as list
        """
        filename = os.path.join(dirname, "frontEndBusInfo.json")
        with open(filename) as json_file:
                    busStopInfo = json.load(json_file)
        busStopInfo = busStopInfo[stop_number]
        return busStopInfo

    def get_direction(self, route_numbers, stop_number):
        """
        Input: bus stop number and route_number
        Output: Direction of route as int and headsign label
        """
        stop_number=Stops.objects.get(stopid_short=stop_number)
        allTrips=StopTimes.objects.filter(stop=stop_number)
        directions = {}
        for route in route_numbers:
            allRoutes=Trips.objects.filter(route__route_short_name=route, trip__in=allTrips).values('direction_id', 'trip_headsign').distinct()
            # This query sometimes returns empty, even in mysql
            # Need to investigate further
            if len(allRoutes) > 0:
                directions[route] = allRoutes[0]
        return directions

    def serialize_machine_learning_input(self, stop_number, weather, routes, directions):
        """
        Input: weather data as json/dict, routes as list, direction as int
        Output: machine learning inputs as json

        """
        machine_learning_inputs = MachineLearningInputs(stop_number,
                                                        weather,
                                                        routes,
                                                        directions)
        machine_learning_inputs = MachineLearningInputSerializer(
            machine_learning_inputs)
        return machine_learning_inputs.data


    def get_arrival_times(self, machine_learning_inputs):
        """
        Input: machine learning inputs as json
        Output: machine learning predictions as dictionary/json
        Note: output format depends on if we serialize here or somewhere else
        """
        results =    [
           {
              "stop": "2007",
              "route":"46a",
              "arrival_time":"4"
           },
           {
              "stop": "2007",
              "route":"39a",
              "arrival_time":"2"
           },
           {
              "stop": "2007",
              "route":"145",
              "arrival_time":"1"
           },
           {
              "stop": "2007",
              "route":"46a",
              "arrival_time":"8"
           },
           {
              "stop": "2007",
              "route":"155",
              "arrival_time":"6"
           },
        ]
        return results



    def sort_results(self, results):
        """
        Input: Machine learning results as json
        Output: Machine learning results sorted by departure time as json
        """
        results_sorted = sorted(results, key=lambda k: k["arrival_time"])
        return results_sorted

class SearchByRoute(SearchByStop):
        """
        Input: HTTP request
        Output: Machine learning output as json
        Note: Main logic implemented here using the methods below
        """
        def get(self, request):
            start = self.get_params("start")
            route = self.get_params("route")
            time = self.get_params("time")
            date = self.get_params("date")

            weather = self.get_weather(time, date)
            stops = self.get_stops(start)
            stops = self.sort_stops_by_distance(stops)
            direction = self.get_direction([route], stops)
            machine_learning_inputs = self.serialize_machine_learning_input(
                                                                    stops,
                                                                    weather,
                                                                    route,
                                                                    direction)
            results = self.get_arrival_times(machine_learning_inputs)
            results = self.sort_results(results)
            return Response(results)

        def get_stops(self, start):
            """
            Input: starting point as string
            Output: stops near starting point and walking distance as dict
            """
            return "stops"

        def sort_stops_by_distance(self, stops):
            """
            Input: stops and distances as dictionary
            Output: stops sorted by increasing distance
            """
            return "stops sorted"


class SearchByDestination(SearchByStop):
    """
    Search by destination feature
    Inherits from search by stop
    """

    def get(self, request):
        return HttpResponse("<h1>SearchByDestination</h1>")

class RouteView(generics.ListCreateAPIView):
    """
    Shows routes table
    """
    queryset = Routes.objects.all()
    serializer_class = RouteSerializer
