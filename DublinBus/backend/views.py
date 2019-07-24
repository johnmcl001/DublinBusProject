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

import pickle
from sklearn.linear_model import LinearRegression
import pandas as pd

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)


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
        trips=self.get_relevant_trips_per_route_and_stop(stop_number, routes, day_info['day_long'], time, day_info["date"])
        directions = self.get_direction(day_info['day_long'], day_info["date"], routes, stop_number)
        machine_learning_inputs = self.serialize_machine_learning_input(
                                                            time,
                                                            day_info["day"],
                                                            day_info["month"],
                                                            day_info["date"],
                                                            stop_number,
                                                            weather,
                                                            routes,
                                                            trips,
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
        now = datetime.now().strftime("%H:%M:%S")
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
            day = datetime.strptime(date, '%d-%m-%Y').weekday()
            month=int(datetime.strptime(date, '%d-%m-%Y').strftime('%m'))
            day_long=datetime.strptime(date, '%d-%m-%Y').strftime('%A').lower()
            return {"date": date, "day": day, 'month': month, 'day_long':day_long}

        date = self.request.GET.get("date", None)
        day = datetime.strptime(date, '%d-%m-%Y').weekday()
        day_long=datetime.strptime(date, '%d-%m-%Y').strftime('%A').lower()
        month=int(datetime.strptime(date, '%d-%m-%Y').strftime('%m'))
        return {"date": date, "day": day, 'month': month, 'day_long':day_long}

    def get_weather(self, time, date):
        """
        Input: time and date as strings
        Output: weather conditions for prediction as json or dictionary
        """
        weatherResult=Forecast.objects.filter(date=date)
        #print(weatherResult)
        for result in weatherResult:
            if result.end_time=="00:00":
                result.end_time="24:00"
                if result.start_time <= (datetime.strptime(self.get_time(),"%H:%M:%S")+timedelta(minutes=60)).strftime("%H:%M") < result.end_time:
                    forecast = {
                        "temperature": result.temperature,
                        "cloud": result.cloud_percent,
                        "rain": result.rain,
                        "description": result.description,
                    }
                    return forecast
            else:
                if datetime.strptime(result.start_time, "%H:%M") <= (datetime.strptime(self.get_time(),"%H:%M:%S")+timedelta(minutes=60)) < datetime.strptime(result.end_time, "%H:%M"):
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

    def get_relevant_trips_per_route_and_stop(self, stop, route_numbers, day, time, date):
        """
        #Input: short route id, time(optional)
        #Filters trips that run for the given day, 30 mins before the time and upto
        #one hour after the time given.
        #Output: list of trips objects
        """
        date=(datetime.strptime(date,"%d-%m-%Y")).strftime('%Y%m%d')
        #print(date)
        #get time 30 minutes before hand to allow for prediction model difference
        start_time=(datetime.strptime(self.get_time(),"%H:%M:%S")-timedelta(minutes=30)).strftime('%H:%M:%S')
        end_time=(datetime.strptime(self.get_time(),"%H:%M:%S")+timedelta(minutes=60)).strftime('%H:%M:%S')
        services=Calendar.objects.filter(**{day:1}, start_date__lte=date, end_date__gte=date)
        long_ids=Routes.objects.filter(route_short_name__in=route_numbers)
        trips=Trips.objects.filter(route_id__in=long_ids, service_id__in=services).values('trip_id')
        trips=StopTimes.objects.filter(trip_id__in=trips, departure_time__gte=start_time, departure_time__lte=end_time, stop__stopid_short=stop).order_by('departure_time')
        #print(trips)
        info={}
        for trip in trips:
            route_short=trip.trips_set.get().route.route_short_name
            if route_short not in info:
                info[route_short]=[trip.arrival_time, trip.stop_sequence],
            else:
                info[route_short]+=[trip.arrival_time, trip.stop_sequence],
        return info


    def get_direction(self, day, date, route_numbers, stop_number):
        """
        Input: bus stop number and route_number
        Output: Direction of route as int and headsign label
        """
        stop_number=Stops.objects.get(stopid_short=stop_number)
        allTrips=StopTimes.objects.filter(stop=stop_number)
        services=Calendar.objects.filter(**{day:1}, start_date__lte=date, end_date__gte=date)
        directions = {}
        for route in route_numbers:
            allRoutes=Trips.objects.filter(route__route_short_name=route, trip__in=allTrips, service_id__in=services).values('direction_id', 'trip_headsign').distinct()
            if len(allRoutes) > 0:
                directions[route] = allRoutes[0]
        return directions

    def serialize_machine_learning_input(self,time, day, month, date, stop_number, weather, routes, trips, direction):
        """
        Input: weather data as json/dict, routes as list, direction as int
        Output: machine learning inputs as json

        """
        machine_learning_inputs = MachineLearningInputs(time,
                                                        day,
                                                        month,
                                                        date,
                                                        stop_number,
                                                        weather,
                                                        routes,
                                                        trips,
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
        date=datetime.strptime(machine_learning_inputs['date'],'%d-%m-%Y')
        time=datetime.strptime(machine_learning_inputs['time'], '%H:%M:%S').time()
        results=[]
        #machine_learning_inputs['trips'][route][1]=stop sequence
        #machine_learning_inputs['trips'][route][0]=Planned arrival time
        predictions_dict={}
        for route in machine_learning_inputs['trips'].keys():
            predictions_dict[route]={}
            stop_num=[]
            df=pd.DataFrame(columns=['temperature_NORM','PROGRNUMBER_NORM','month','day'])
            for num in range(0, len(machine_learning_inputs['trips'][route])):
                if machine_learning_inputs['trips'][route][num][1] not in stop_num:
                    stop_num+=machine_learning_inputs['trips'][route][num][1],
                    filename = os.path.join(dirname, '46A.pkl')
                    model = pickle.load(open(filename,'rb'))
                    df=df.append({
                        "temperature_NORM":machine_learning_inputs['weather']['temperature'],
                        "PROGRNUMBER_NORM":num,
                        "month": machine_learning_inputs['month'],
                        "day": machine_learning_inputs['day']
                        }, ignore_index=True)
            predictions_list=model.predict(df)
            for i in range(0, len(stop_num)):
                predictions_dict[route][stop_num[i]]=predictions_list[i]

        for route in machine_learning_inputs['trips'].keys():
            for num in range(0, len(machine_learning_inputs['trips'][route])):
                arrival_time=(datetime.combine(date, machine_learning_inputs['trips'][route][num][0])+timedelta(seconds=predictions_dict[route][machine_learning_inputs['trips'][route][num][1]])).time()
                if self.valid_trip_check(date, time, arrival_time):
                    #mins_away=(datetime.combine(date, arrival_time)- datetime.combine(date, time))
                    #print(mins_away)
                    results+={'stop': machine_learning_inputs['stop_number'], 'route': route, 'arrival_time': arrival_time.strftime("%H:%M:%S")},

        return results

    def valid_trip_check(self, date, person_leaving_time, bus_arrival_time, walking_time=0, buffer=0):
        if (datetime.combine(date, person_leaving_time) + timedelta(hours=walking_time)).time()< (datetime.combine(date, bus_arrival_time)- timedelta(minutes=buffer)).time():
            return True
        return False


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
        start_coords = {"lat" : self.get_coords("startpointLat"),
                        "lon" : self.get_coords("startpointLon")}
        end_coords = {"lat" : self.get_coords("departureLat"),
                        "lon" : self.get_coords("departureLon")}
        route = self.get_route(start_coords, end_coords)
        route_segments = self.get_route_segments(route)
        return Response(route_segments)
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

    def get_route(self, start_coords, end_coords):
        """
        Input: origin coords as string, destination coords as string
        Output: route as json
        """
        key = os.getenv("GOOGLE")
        start = str(start_coords["lat"]) + "," + str(start_coords["lon"])
        end = str(end_coords["lat"]) + "," + str(end_coords["lon"])
        call = "https://maps.googleapis.com/maps/api/directions/json?origin=" +start + "&destination=" + end + "&key=" + key + "&mode=transit&transit_mode=bus&alternatives=true&region=IE"
        response = requests.get(call)

        if response.status_code == 200:
            route = json.loads(response.text)
        elif response.status_code == 400:
            route = "not found"
        return route

    def get_route_segments(self, route):
        """
        Input: route as json
        Ouput: route segments as json
        """
        steps = route["routes"][0]["legs"][0]["steps"]
        route_breakdown = {"instructions": [], "markers": [], "polylines": [], "busInfo": {}, "travel_mode": []}
        for step in steps:
            route_breakdown["instructions"] += [{"time": step["duration"]["value"]//60, "instruction": step["html_instructions"]}]
            route_breakdown["markers"] += [{"start_lat": step["start_location"]["lat"],
            "start_lon": step["start_location"]["lng"],
            "end_lat": step["end_location"]["lat"],
            "end_lon": step["end_location"]["lng"]}]
            route_breakdown["polylines"] += [step["polyline"]["points"]]
            route_breakdown["travel_mode"] += [step["travel_mode"]]
            if step["travel_mode"] == "TRANSIT":
                route_breakdown["busInfo"]["route"] = step["transit_details"]["line"]["short_name"]
                route_breakdown["busInfo"]["num_stops"] = step["transit_details"]["num_stops"]
                route_breakdown["busInfo"]["arrival_stop"] = step["transit_details"]["arrival_stop"]["name"]
                route_breakdown["busInfo"]["departure_stop"] = step["transit_details"]["departure_stop"]["name"]
        return route_breakdown


    def get_arrival_time(self, ):
        """
        Input
        Output
        """
        pass

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
        return(NearbyStations(station_list, many=True))
        #station_dict={}
        #for station in station_list:
        #    station_dict[station.stop_id]=station.distance
        #return station_dict

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


class StopsAutocomplete(views.APIView):

    def get(self, request):
        """
        Input: User HTTP request
        Output: List of stops for a specific route, direction, day
        """
        params = self.get_params()
        day = datetime.today().strftime('%A').lower()
        stops = self.get_stops(params, day)
        return Response(stops)

    def get_params(self):
        """
        Input: None
        Output: Route, direction, day as dict
        """
        params = {}
        params["route"] = self.request.GET.get("route", None)
        params["direction"] = self.request.GET.get("direction", None)
        return params


    def get_stops(self, params, day):
        """
        Input: sql query as string
        Output: stops for route given direction and day as list
        """
        query ="select distinct s.stopID_short, s.stop_name, s.stop_id from stops s, stop_times st, trips t, routes r, calendar c where s.stop_id = st.stop_id and st.trip_id = t.trip_id and t.route_id = r.route_id and t.service_id = c.service_id and r.route_short_name = %s and st.stop_headsign = %s"

        stops = list(Stops.objects.raw(query, [params["route"], params["direction"]]))

        stop_list = []
        for stop in stops:
            stop_list += [str(stop.stopid_short) + ", " + str(stop.stop_name)]


        return stop_list


class RouteView(generics.ListCreateAPIView):
    """
    Shows routes table
    """
    queryset = Routes.objects.all()
    serializer_class = RouteSerializer
