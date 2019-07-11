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
import requests
import os
from rest_framework import generics
from geopy.geocoders import Nominatim
from .HereManager import HereManager

#import pymysql
from datetime import datetime, timedelta, date


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

        stop_number = self.request.GET.get("stopnumber")
        time = self.get_time()
        day_info = self.get_day_and_date()
        weather = self.get_weather(time, day_info["date"])
        bus_stop_info = self.get_bus_stop_info(stop_number)
        routes = self.get_routes(bus_stop_info)
        directions = self.get_direction(routes, stop_number)
        machine_learning_inputs = self.serialize_machine_learning_input(
                                                            time,
                                                            day_info["day"],
                                                            day_info["date"],
                                                            stop_number,
                                                            weather,
                                                            routes,
                                                            directions)
        results = self.get_arrival_times(machine_learning_inputs)
        results = self.sort_results(results)
        return Response(results)

    def get_time(self):
        """
        input: None
        output: either time specified in url or time now as string
        """
        now = datetime.now().strftime("%H:%M")
        return self.request.GET.get("time", now)

    def get_day_and_date(self):
        """
        input: None
        output: return day and date in dict
        """
        date = self.request.GET.get("date",
                                    datetime.today().strftime('%d-%m-%Y'))
        day = datetime.strptime(date, '%d-%m-%Y').strftime('%a')
        return {"date": date, "day": day}

    def get_weather(self, time, date):
        """
        Input: time and date as strings
        Output: weather conditions for prediction as json or dictionary
        """
        weatherResult=Forecast.objects.filter(date=date)
        for result in weatherResult:
            if datetime.strptime(result.start_time, "%H:%M") <= datetime.strptime(time, "%H:%M") < datetime.strptime(result.end_time, "%H:%M"):
                forecast = {
                    "temperature": result.temperature,
                    "cloud": result.cloud_percent,
                    "rain": result.rain,
                    "description": result.description,
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

    def get_routes(self, bus_stop_info):
        """
        Input: Http request, bus_stop_info
        Ouput: route(s) as list
        """
        if self.request.GET.get("route") != None:
            routes = [self.request.GET.get("route")]
        else:
            routes = bus_stop_info["routes"][0]
        return routes

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

    def serialize_machine_learning_input(self, time, day, date, stop_number, weather, routes, directions):
        """
        Input: weather data as json/dict, routes as list, direction as int
        Output: machine learning inputs as json

        """
        machine_learning_inputs = MachineLearningInputs(time,
                                                        day,
                                                        date,
                                                        stop_number,
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
