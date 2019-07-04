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
        day = self.get_params("day")
        weather = self.get_weather(time, day)
        routes = self.get_routes(stop_number)
        direction = self.get_direction(stop_number, routes)
        machine_learning_inputs = serialize_machine_learning_input(stop_number,
                                                                   weather,
                                                                   routes,
                                                                   direction)
        # results = self.get_arrival_times(machine_learning_inputs)
        results_sorted = self.sort_results(results)
        # results_json = jsonify_results(results)

        return Response([
   {
      "route":"145",
      "arrival_time":"1"
   },
   {
      "route":"39a",
      "arrival_time":"2"
   },
   {
      "route":"46a",
      "arrival_time":"4"
   },
   {
      "route":"155",
      "arrival_time":"6"
   },
   {
      "route":"46a",
      "arrival_time":"8"
   }
])

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
        weatherResult=Forecast.objects.get(date=date, start_time__lte=time, end_time__lt=time )
        return weatherResult

    def get_routes(self, stop_number):
        """
        Input: bus stop number as a string
        Output: List of Routes that server that bus stop as list
        """
        filename = os.path.join(dirname, "frontEndBusInfo.json")
        with open(filename) as json_file:
                    busStopInfo = json.load(json_file)
        busStopInfo = busStopInfo[stop_number]['routes'][0]
        return busStopInfo

    def get_direction(self, route_number, stop_number):
        """
        Input: bus stop number and route_number
        Output: Direction of route as int and headsign label
        """
        stop_number=Stops.objects.get(stopid_short=stop_number)
        allTrips=StopTimes.objects.filter(stop=stop_number.stop_id)
        allRoutes=Trips.objects.filter(route__route_short_name='7d', trip__in=allTrips).values('direction_id', 'trip_headsign').distinct()
        return allRoutes[0]

    def serialize_machine_learning_input(self, stop_number, weather, routes, direction):
        """
        Input: weather data as json/dict, routes as list, direction as int
        Output: machine learning inputs as json

        """
        machine_learning_inputs = MachineLearningInputs(stop_number,
                                                        weather,
                                                        routes,
                                                        direction)
        machine_learning_inputs = MachineLearningInputSerializer(
            machine_learning_inputs)
        return machine_learning_inputs.data


    def get_arrival_times(self, machine_learning_inputs):
        """
        Input: machine learning inputs as json
        Output: machine learning predictions as dictionary/json
        Note: output format depends on if we serialize here or somewhere else
        """
        results = []
        return results



    def sort_results(self, results):
        """
        Input: Machine learning results as json
        Output: Machine learning results sorted by departure time as json
        """
        results_sorted = sorted(results, key=lambda k: k["arrival_time"])
        return results_sorted

    def jsonify_results(self, results):
        """
        Input: Serialized machine learning results
        Output: Machine Learning results as json
        Note: Not sure if we can just do this in the previous function
        """
        results_jsonified = ResultsJsonifier(results)
        return results_jsonified.data


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

class RouteView(generics.ListCreateAPIView):
    """
    Shows routes table
    """
    queryset = Routes.objects.all()
    serializer_class = RouteSerializer
