"""
Create views here
Don't need to worry about rendering
Mostly just create the logic for the machine learning
"""

from django.shortcuts import HttpResponse
from rest_framework import viewsets
from rest_framework import views
from rest_framework.response import Response
import pymysql
from datetime import datetime, timedelta
import json



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
        # direction = self.get_direction(stop_number, routes) # Done by Niamh
        machine_learning_inputs = serialize_machine_learning_input(stop_number,
                                                                   weather,
                                                                   routes,
                                                                   direction)
        # results = self.get_arrival_times(machine_learning_inputs)
        results_sorted = self.sort_results(results)
        # results_json = jsonify_results(results)
        # return Response(results_json)

    def get_params(self, target):
        """
        input: params from url
        output: desired param as string
        """
        param = self.request.GET.get(target, None)
        return param

    def get_weather(self, time, date):
        """
        Input: time and date
        Output: weather conditions for prediction as json or dictionary
        """
        def hour_rounder(t):
            """
            Rounds to nearest hour by adding a timedelta hour if minute >= 30
            Input: DateTime
            Output: DateTime Rounded
            """
            return (t.replace(second=0, minute=0, hour=t.hour)
                       +timedelta(hours=t.minute//30))

        datetime = datetime.strptime(date+" "+time, '%d-%m-%Y %H:%M')
        datetime=(hour_rounder(datetime))
        date=datetime.strftime("%d-%m-%Y")
        time=datetime.strftime("%H:%M")

        sql = "SELECT * FROM website.forecast where date='%s' and time='%s'" %(date, time)
        db = pymysql.connect(host="csi420-01-vm9.ucd.ie", port=3306 , user="niamh", passwd="comp47360jnnd", db="website")
        cursor = db.cursor()
        cursor.execute(sql)
        weather = cursor.fetchall()
        cursor.close()

        return weather

    def get_routes(self, stop_number):
        """
        Input: bus stop number as a string
        Output: List of Routes that server that bus stop as list
        """
        with open('frontEndBusInfo.json') as json_file:
                    busStopInfo = json.load(json_file)
        busStopInfo = busStopInfo[stop_number]['routes'][0]
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

# Just lets us view the data base in a web ui
# Also useful for testing sometimes
# Get list with localhost:8000/api

# Will probably remove at the end


class StopsView(viewsets.ModelViewSet):
    """
    Shows stops table
    """

      # Define which serializer to use
    serializer_class = StopSerializer
    queryset = Stops.objects.all()


class RoutesView(viewsets.ModelViewSet):
    """
    Shows routes table
    """
    queryset = Routes.objects.all()
    serializer_class = RouteSerializer


class StopTimesView(viewsets.ModelViewSet):
    """
    Shows stoptimes table
    """
    queryset = StopTimes.objects.all()
    serializer_class = StopTimeSerializer


class TripsView(viewsets.ModelViewSet):
    """
    shows trips table
    """
    queryset = Trips.objects.all()
    serializer_class = TripSerializer
