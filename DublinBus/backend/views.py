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
from .HereManager import HereManager
from datetime import datetime, timedelta, date
from ast import literal_eval

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
        #return Response(machine_learning_inputs)
        results = self.get_arrival_times(machine_learning_inputs)
        results = self.sort_results(results)
        return Response(results)

    def get_time(self):
        """
        input: None
        output: either time specified in url or time now as string
        """
        now = datetime.now().strftime("%H:%M")
        if self.request.GET.get("time", now) == "null":
            return now
        return self.request.GET.get("time", now)

    def get_day_and_date(self):
        """
        input: None
        output: return day and date in dict
        """
        date = datetime.today().strftime('%d-%m-%Y')
        if self.request.GET.get("date") == "null" or self.request.GET.get("date") is None:
            day = datetime.strptime(date, '%d-%m-%Y').strftime('%a')
            return {"date": date, "day": day}

        date = self.request.GET.get("date", None)
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
        time = self.get_time()
        day_info = self.get_day_and_date()
        weather = self.get_weather(time, day_info["date"])
        start_coords = self.get_coords("startpoint")
        end_coords = self.get_coords("destination")
        dir_route = self.find_direct_route(start_coords,
                                           end_coords,
                                           day_info,
                                           time)
        return Response(dir_route)

    def get_coords(self, point):
        """
        Input: http request
        Output: coords as dict
        """
        coords = self.request.GET.get(point)
        return literal_eval(coords)

    def get_arrival_time(self, ):
        """
        Input
        Output
        """

    def get_stations_nearby(self, dest_lat, dest_lon):
        """
        Input: Centre point coordinates
        Output: List of stop objects with attributes id and distance from centre point
        """
        default_radius=1 #km
        station_list=[]
        #for results that are not null, the more stations we check the better
        #trade off-response time
        while default_radius<5 and len(station_list)<5:
            station_list=Stops.objects.raw('SELECT stop_id, stopID_short,'\
            +' ( 6371 * acos( cos( radians(%(dest_lat)s) ) * cos( radians( stop_lat ) ) *'\
            + ' cos( radians( stop_lon ) - radians(%(dest_lon)s) ) + sin( radians(%(dest_lat)s) )'\
            +' * sin( radians( stop_lat ) ) ) ) AS distance FROM website.stops HAVING distance < '\
            +'%(default_radius)s ORDER BY distance LIMIT 0 , 10;',{'dest_lat':str(dest_lat), 'dest_lon':str(dest_lon), 'default_radius':str(default_radius)})
            default_radius+=1
        if (len(list(station_list))==0):
            return None
        station_dict={}
        for station in station_list:
            station_dict[station.stop_id]=station.distance
        return station_dict

    def walking_time(self, distance, speed=4):
        """
        Input: distance from stop, speed is by default 4km/hr
        Output: time(in hours) needed to walk to the bus stops
        """
        return float(distance)/float(speed)

    def valid_route_check(self, leave_time, walking_time):
        if (datetime.now() + timedelta(hours=walking_time)).strftime('%H:%M')<leave_time-buffer:
            return True
        return False

        """def get_relevant_routes_for_stop(stop, day, time):
        """
        #Input: bus stop, day and time
        #Output: routes that serve that bus stop that leave around the time given
        """
        day=datetime.now().strftime("%A").lower()
        #get time 30 minutes before hand to allow for prediction model difference
        start_time=(datetime.strptime(self.get_time(),"%H:%M")-timedelta(minutes=30)).strftime('%H:%M:%S')
        end_time=(datetime.strptime(self.get_time(),"%H:%M")+timedelta(minutes=60)).strftime('%H:%M:%S')
        services=Calendar.objects.filter(**{day:1})
        trips=StopTimes.objects.filter(departure_time__gte=start_time, departure_time__lte=end_time, stop__stopid_short=stop).values('trip_id')
        long_ids=Trips.objects.filter(service_id__in=services, trip_id__in=trips).values('route_id').distinct()
        routes=Routes.objects.filter(route_id__in=long_ids).values('route_short_name')
        return routes
        """

        """def get_relevant_trips_per_route_and_stop(route, stop, day, time):
        """
        #Input: short route id, time(optional)
        #Filters trips that run for the given day, 30 mins before the time and upto
        #one hour after the time given.
        #Output: list of trips objects
        """
        day=datetime.now().strftime("%A").lower()
        #get time 30 minutes before hand to allow for prediction model difference
        start_time=(datetime.strptime(self.get_time(),"%H:%M")-timedelta(minutes=30)).strftime('%H:%M:%S')
        end_time=(datetime.strptime(self.get_time(),"%H:%M")+timedelta(minutes=60)).strftime('%H:%M:%S')
        services=Calendar.objects.filter(**{day:1})
        long_ids=Routes.objects.filter(route_short_name=route)
        trips=Trips.objects.filter(route_id__in=long_ids, service_id__in=services).values('trip_id')
        trips=StopTimes.objects.filter(trip_id__in=trips, departure_time__gte=start_time, departure_time__lte=end_time, stop__stopid_short=stop)
        return trips
        """

    def find_direct_route(self, start_coord, end_coord, day, time):
        """
        Input: start poition as lat long, end position as lat long
               day of the week(optional, today if null), time(optional, now if null)
        Output: 10 routes from start to stop order by stop_ids(for future walking calc)
        """
        inputs={}
        start_stations=self.get_stations_nearby(start_coord["lat"],
                                                start_coord["lon"])
        end_stations=self.get_stations_nearby(end_coord["lat"],
                                              end_coord["lon"])
        if start_stations==None or end_stations==None:
            return "There are no direct routes within a 5km walk"
        #convert list to tuples with stop ids for query
        start_stop_list = []
        for stop in start_stations.keys():
            start_stop_list += stop,
        inputs['start_stations']=tuple(start_stop_list)
        end_stop_list = []
        for stop in start_stations.keys():
            end_stop_list += stop,
        inputs['end_stations']=tuple(end_stop_list)

        day=datetime.now().strftime("%A").lower()
        inputs[day]=1
        inputs['date']=datetime.now().strftime('%Y%m%d')
        #get time 30 minutes before hand to allow for prediction model difference
        inputs['start_time']=(datetime.strptime(self.get_time(),"%H:%M")-timedelta(minutes=30)).strftime('%H:%M:%S')
        inputs['end_time']=(datetime.strptime(self.get_time(),"%H:%M")+timedelta(minutes=60)).strftime('%H:%M:%S')

        #checks that trip will leave within the time frame given, the two stops are in the same trip,
        #the service runs on the correct day and the destination stop comes after the start stop
        #

        trips=StopTimes.objects.raw("SELECT distinct t.trip_headsign, t.route_id, st1.trip_id, st1.departure_time, st1.stop_id as start_stop_id, "\
        +"st1.stop_sequence as start_num, st1.shape_dist_traveled as start_dist,st2.arrival_time, st2.stop_id as end_stop_id, st2.stop_sequence as end_num ,"\
        +" st2.shape_dist_traveled as end_dist FROM website.stop_times as st1, website.stop_times as st2, website.trips "\
        +"as t, website.calendar as c where st1.stop_id in %(start_stations)s and st2.stop_id in %(end_stations)s"\
        +" and st1.stop_sequence<st2.stop_sequence and st1.departure_time>=%(start_time)s and st1.departure_time<=%(end_time)s and st2.departure_time>%(start_time)s"\
        +" and st1.trip_id=t.trip_id and t.service_id=c.service_id and c.friday=1 and st1.trip_id=st2.trip_id"\
        +" and c.start_date<=%(date)s and c.end_date>=%(date)s order by st1.stop_id limit 20;",inputs)

        routes=[]
        for trip in trips:
            #run machine learning model to get start_time
            #trip.departure_time=start_time
            start_walk_time=self.walking_time(start_stations[trip.start_stop_id])
            return (datetime.strptime(time, '%H:%M') + timedelta(minutes = start_walk_time*60)).strftime("%H:%M")
            leavetime = self.get_arrival_time()

            if self.valid_route_check(leavetime, start_walk_time):
                #run machine learning to predict arrival time
                #trip.arrival_time=arrival_time
                end_walk_time=self.walking_time(end_stations[trip.end_stop_id])
                routes+=[start_walk_time,trip,end_walk_time]

        #each object contains the walking distance to stop, its headsign, route_id, trip_id, departure_time, start stop_id, start stop_sequence,
        #start shape_dist_traveled, dest arrival_time, dest stop_id, dest stop_sequence, dest shape_dist_traveled and walking dist to destination
        return routes

    def get(self, request):
        return Response([
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
        ])

class RouteView(generics.ListCreateAPIView):
    """
    Shows routes table
    """
    queryset = Routes.objects.all()
    serializer_class = RouteSerializer
