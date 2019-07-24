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
        trips=self.get_relevant_trips_per_routes_and_stops(stop_number, routes, day_info['day_long'], time, day_info["date"])
        directions = self.get_direction(day_info['day_long'], day_info["date"], routes, stop_number)
        machine_learning_inputs = self.serialize_machine_learning_input(
                                                            time,
                                                            day_info["day"],
                                                            day_info["month"],
                                                            day_info["date"],
                                                            stop_number,
                                                            weather,
                                                            routes,
                                                            trips)
        #return Response(machine_learning_inputs)

        results = self.get_arrival_times(machine_learning_inputs)
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

    def get_relevant_trips_per_routes_and_stops(self, stop_numbers, route_numbers, day, time, date):
        """
        Input: list of routes, list of stop numbers
        Filters trips that run for the given day, 30 mins before the time and upto
        one hour after the time given.
        Output: list of trips with srrival time, stop_sequence, short stop id and trip id
        """
        #checks if a string is given, converts to a list
        try:
            if stop_numbers.isdigit():
                stop_numbers=[stop_numbers]
        except AttributeError as e:
            pass
        #date in calendar must be changed
        date=(datetime.strptime(date,"%d-%m-%Y")).strftime('%Y%m%d')
        #get time 30 minutes before hand to allow for prediction model difference
        start_time=(datetime.strptime(self.get_time(),"%H:%M:%S")-timedelta(minutes=30)).strftime('%H:%M:%S')
        end_time=(datetime.strptime(self.get_time(),"%H:%M:%S")+timedelta(minutes=60)).strftime('%H:%M:%S')
        services=Calendar.objects.filter(**{day:1}, start_date__lte=date, end_date__gte=date)
        long_ids=Routes.objects.filter(route_short_name__in=route_numbers)
        trips=Trips.objects.filter(route_id__in=long_ids, service_id__in=services).values('trip_id')
        trips=StopTimes.objects.filter(trip_id__in=trips, departure_time__gte=start_time, departure_time__lte=end_time, stop__stopid_short__in=stop_numbers).order_by('departure_time')
        info={}
        for trip in trips:
            route_short=trip.trips_set.get().route.route_short_name
            if route_short not in info:
                info[route_short]=[trip.arrival_time, trip.stop_sequence, trip.stop.stopid_short, trip.trip_id],
            else:
                info[route_short]+=[trip.arrival_time, trip.stop_sequence, trip.stop.stopid_short, trip.trip_id],
        return info


    def get_direction(self, day, date, route_numbers, stop_number):
        """
        Input: bus stop number and route_number
        Filters endpoints that the bus goes to (one the given day) based on route and stop given
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

    def serialize_machine_learning_input(self,time, day, month, date, stop_number, weather, routes, trips):
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
                                                        trips)
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
                    results+={'stop': machine_learning_inputs['stop_number'], 'route': route, 'arrival_time': arrival_time.strftime("%H:%M:%S"), 'stop':machine_learning_inputs['trips'][route][num][2], 'trip_id':machine_learning_inputs['trips'][route][num][3]},

        return self.sort_results(results)

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
        #start_coords = self.get_coords("startpoint")
        start_coords = {"lat" : self.get_coords("startpointLat"),
                        "lon" : self.get_coords("startpointLon")}
        #end_coords = self.get_coords("destination")
        end_coords = {"lat" : self.get_coords("departureLat"),
                        "lon" : self.get_coords("departureLon")}
        dir_route = self.find_direct_routes(start_coords,
                                            end_coords,
                                           day_info['day_long'],
                                           day_info['date'],
                                           time)
        #default to maps
        """dir_route = self.find_direct_routes({'lat':53.3249987, 'lon':-6.26499894},
                                           {'lat':53.295312, 'lon': -6.134956},
                                           day_info['day_long'],
                                           day_info['date'],
                                           time)
        #direct possible
        dir_route = self.find_direct_routes({'lat':53.3249987, 'lon':-6.26499894},
                                               {'lat':53.342608,  'lon': -6.255987},
                                               day_info['day_long'],
                                               day_info['date'],
                                               time)"""

        if len(dir_route)==0:
            routes = self.get_route(time, start_coords,end_coords)
            route_segments = self.get_route_segments(routes, time)
            route_segments=self.validate(route_segments, time, day_info,weather)
            results=self.sort_routes(route_segments)
        else:
            dir_routes=self.validate(dir_route, time, day_info,weather)
            results=self.sort_routes(dir_routes)
            if len(results)==0:
                routes = self.get_route(time)
                route_segments = self.get_route_segments(routes, time)
                route_segments=self.validate(route_segments, time, day_info,weather)
                results=self.sort_routes(route_segments)
        return Response(results)

    def get_coords(self, point):
        """
        Input: http request
        Output: coords as dict
        """
        coords = self.request.GET.get(point)
        return literal_eval(coords)

    def get_route(self, time, start_coords, end_coords):

        """
        Input: origin coords as string, destination coords as string
        Output: route as json
        """
        key = os.getenv("GOOGLE")
        time='now' #EPOCH timestamp
        call = "https://maps.googleapis.com/maps/api/directions/json?origin="\
        +str(start_coords['lat'])+','+str(start_coords['lon'])+"&destination="+str(end_coords['lat'])+','+str(end_coords['lon'])+"&key="\
        + key + "&mode=transit&transit_mode=bus&alternatives=true&region=ie&departure_time="+str(time)

        response = requests.get(call)
        if response.status_code == 200:
            route = json.loads(response.text)
        elif response.status_code == 400:
            route = "not found"
        return route

    def get_route_segments(self, route, time):
        """
        Input: route as json
        Ouput: route segments as json
        """
        all_routes=[] 
   
        for r in range(0, len(route["routes"])):
            steps = route["routes"][r]["legs"][0]["steps"]
            segments = []
            count=0
            for step in steps:
                #print(step)
                #print()
                segment = {}
                segment["duration_sec"] = step["duration"]["value"]
                segment["instruction"] = step["html_instructions"]
                segment["start_lat"] = step["start_location"]["lat"]
                segment["start_lon"] = step["start_location"]["lng"]
                segment["end_lat"] = step["end_location"]["lat"]
                segment["end_lon"] = step["end_location"]["lng"]
                segment["polyline"] = step["polyline"]["points"]
                segment['distance'] = step["distance"]["value"]
                segment["travel_mode"] = step["travel_mode"]
                segment["markers"] += [{"start_lat": step["start_location"]["lat"],
            "start_lon": step["start_location"]["lng"],
            "end_lat": step["end_location"]["lat"],
            "end_lon": step["end_location"]["lng"]}]
                if segment["travel_mode"] == "TRANSIT":
                    segment["route"] = step["transit_details"]["line"]["short_name"]
                    segment["num_stops"] = step["transit_details"]["num_stops"]
                    segment["arrival_stop"] = step["transit_details"]["arrival_stop"]["name"]
                    segment["departure_stop"] = step["transit_details"]["departure_stop"]["name"]
                if count==0:
                    segment["start_time"]=time
                    if segment["travel_mode"] == "WALKING":
                        segment["end_time"]=(datetime.strptime(segment["start_time"],"%H:%M:%S")+timedelta(seconds=segment["duration_sec"])).strftime('%H:%M:%S')
                segments += [segment]
                count+=1
            all_routes+=segments,
        return all_routes

    def validate(self, route_segments, time, day_info, weather):
        """
        Input: a list of routes broken into segments
        Ouput: a list of dictionarys with valid routes based on our ML prediction model
        """
        valid_results=[]
        count=0
        #loop for each route option given by google maps
        for route in route_segments:
            start=time
            end=time
            #loop for each segment per route and check if the segment is valid.
            for i in range(0, len(route)):
                segment=route[i]
                #if segment is walking end time can be calculated by addition
                if segment["travel_mode"]=="WALKING":
                    valid_result=True
                    segment["end_time"]=(datetime.strptime(segment["start_time"],"%H:%M:%S")+timedelta(seconds=segment["duration_sec"])).strftime('%H:%M:%S')
                #if segment is transit, we must run our machine learning model to
                #ensure a bus will arrive after the previous stage of the journey
                #is complete
                if segment["travel_mode"]=="TRANSIT":
                    start_stop=self.get_station_number(segment["departure_stop"], segment["start_lat"], segment["start_lon"])
                    end_stop=self.get_station_number(segment["arrival_stop"], segment["end_lat"], segment["end_lon"])
                    if end_stop == None:
                        print('Cant identify stop')
                    #finds all relevant trips that serve the stop and route given by google maps
                    trips=self.get_relevant_trips_per_routes_and_stops([start_stop], [segment["route"]], day_info['day_long'], time, day_info["date"])

                    machine_learning_inputs = self.serialize_machine_learning_input(
                                                                        time,
                                                                        day_info["day"],
                                                                        day_info["month"],
                                                                        day_info["date"],
                                                                        start_stop,
                                                                        weather,
                                                                        segment["route"],
                                                                        trips)
                    #runs our machine learning on all relevant trips
                    results = self.get_arrival_times(machine_learning_inputs)
                    valid_result=False
                    #updates start, end and journey duration in segments.
                    for res in results:
                        #no walking as first stage.
                        if i==0:
                            if res['arrival_time']>= time:
                                index=results.index(res)
                                segment['later_bus_arrivals']=results[index:]
                                segment['start_time']=res['arrival_time']
                                if StopTimes.objects.filter(trip_id=res['trip_id'], stop__stopid_short=end_stop).count()==0:
                                    valid_result=False
                                    break
                                segment['end_time']=StopTimes.objects.filter(trip_id=res['trip_id'], stop__stopid_short=end_stop)[:1][0].arrival_time.strftime('%H:%M:%S')
                                segment['duration_sec']=(datetime.strptime(segment["end_time"],"%H:%M:%S")-datetime.strptime(segment["start_time"],"%H:%M:%S")).total_seconds()
                                if i !=len(route)-1:
                                    route[i+1]["start_time"]=segment['end_time']
                                valid_result=True
                                break
                        else:
                            #bus must leave after walking time
                            if res['arrival_time']>=route[i-1]['end_time']:
                                index=results.index(res)
                                segment['later_bus_arrivals']=results[index:]
                                segment['start_time']=res['arrival_time']
                                #testing to see if flushing query by print works
                                if StopTimes.objects.filter(trip_id=res['trip_id'], stop__stopid_short=end_stop).count()==0:
                                    valid_result=False
                                    break
                                segment['end_time']=StopTimes.objects.filter(trip_id=res['trip_id'], stop__stopid_short=end_stop)[:1][0].arrival_time.strftime('%H:%M:%S')
                                segment['duration_sec']=(datetime.strptime(segment["end_time"],"%H:%M:%S")-datetime.strptime(segment["start_time"],"%H:%M:%S")).total_seconds()
                                if i !=len(route)-1:
                                    route[i+1]["start_time"]=segment['end_time']
                                valid_result=True
                                break
                    if valid_result==True:
                        end=segment['end_time']
                    #after the segment has been checked, if no valid result has Been
                    #found break out of the route and dont add to results
                    if valid_result==False:
                        break
            count+=1
            duration=str((datetime.strptime(end,"%H:%M:%S")-datetime.strptime(start,"%H:%M:%S")).total_seconds())
            if valid_result==True and {'duration':duration, 'route':route} not in valid_results:
                valid_results+={'duration':duration, 'route':route},
        return valid_results

    def sort_routes(self, results):
        """
        Input: Routes results as json
        Output: Routes results sorted into a dictionary where route is key, then stops and times as values
        """
        return sorted(results, key=lambda k: k["duration"])

    def get_station_number(self, name, dest_lat, dest_lon):
        """
        Input: Station name and coordinates
        Output: Short stop id
        """
        num_of_stations_with_name=Stops.objects.filter(stop_name=name).count()
        if num_of_stations_with_name!=1:
            #Finds stations within 500m of the coordinates and returns 1
            for station in Stops.objects.raw('SELECT stop_id, stopID_short,'\
            +' ( 6371 * acos( cos( radians(%(dest_lat)s) ) * cos( radians( stop_lat ) ) *'\
            + ' cos( radians( stop_lon ) - radians(%(dest_lon)s) ) + sin( radians(%(dest_lat)s) )'\
            +' * sin( radians( stop_lat ) ) ) ) AS distance FROM website.stops HAVING distance < '\
            +'%(default_radius)s ORDER BY distance LIMIT 0 , 1;',{'dest_lat':str(dest_lat), 'dest_lon':str(dest_lon), 'default_radius':str(.5)}):
                return station.stopid_short
        else:
            return Stops.objects.get(stop_name=name).stopid_short

    def get_stations_nearby(self, dest_lat, dest_lon):
        """
        Input: Centre point coordinates
        Output: Dictionary of stops with stop id as key and distance in m from centre point as value
        """
        default_radius=1 #km
        station_list=[]
        #for results that are not null, the more stations we check the better
        #trade off-response time
        while default_radius<5 and len(station_list)<10:
            station_list=Stops.objects.raw('SELECT stop_id, stopID_short,'\
            +' ( 6371 * acos( cos( radians(%(dest_lat)s) ) * cos( radians( stop_lat ) ) *'\
            + ' cos( radians( stop_lon ) - radians(%(dest_lon)s) ) + sin( radians(%(dest_lat)s) )'\
            +' * sin( radians( stop_lat ) ) ) ) AS distance FROM website.stops HAVING distance < '\
            +'%(default_radius)s ORDER BY distance;',{'dest_lat':str(dest_lat), 'dest_lon':str(dest_lon), 'default_radius':str(default_radius)})
            default_radius+=1
        if (len(list(station_list))==0):
            return None
        #return(NearbyStations(station_list, many=True))
        station_dict={}
        for station in station_list:
            station_dict[station.stop_id]={'short': station.stopid_short, 'distance':round(station.distance*1000), 'walking_time':self.walking_time(station.distance)}
        return station_dict

    def walking_time(self, distance, speed=4):
        """
        Input: distance from stop, speed is by default 4km/hr
        Output: time(in seconds) needed to walk to the bus stops
        """
        return round((float(distance)/float(speed))*3600)

    def valid_route_check(self, time, leave_time, walking_time):
        """
        Input: Time as a datetime object, the leave_time of the bus and walking time needed to get to the station
        Can use to find if the user has enough time to walk to the bus
        Output: Boolean True/False
        """
        if (time + timedelta(hours=walking_time)).strftime('%H:%M')<leave_time-buffer:
            return True
        return False

    def make_walking_segment(self, start_lat, start_lon, end_lat, end_lon, end_name, walking_time, walking_distance, start_time=None):
        """
        input: Strings(starting coordinates, end coordinates, walking_time of segment, starting time of segments)
        output: walking segment as json
        """
        return {
            "duration_sec": walking_time,
            "instruction": "Walk to "+end_name,
            "start_lat": start_lat,
            "start_lon": start_lon,
            "end_lat": end_lat,
            "end_lon": end_lon,
            "distance": walking_distance,
            "travel_mode": "WALKING",
            "start_time": start_time,
        }

    def make_transit_segment(self, start_lat, start_lon, end_lat, end_lon, end_name, route, start_stop, end_stop, trip_headsign):
        return {
                "instruction": "Bus towards "+end_name,
                "trip_headsign": trip_headsign,
                "start_lat": start_lat,
                "start_lon": start_lon,
                "end_lat": end_lat,
                "end_lon": end_lon ,
                "travel_mode": "TRANSIT",
                "route": route ,
                "arrival_stop": end_stop,
                "departure_stop": start_stop
        }


    def find_direct_routes(self, start_coord, end_coord, day, date, time):
        """
        Input: start poition as dictionary with lat long as keys, end position as dictionary with lat long
               as keys.
        Our own routing which finds a direct route from one station to another.
        Output: 10 routes from start to stop order by stop_ids(for future walking calc)
        """
        #holds information 'start_stations', 'end_stations, 'date', 'start_time', 'end_time' for query
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
        for stop in end_stations.keys():
            end_stop_list += stop,
        inputs['end_stations']=tuple(end_stop_list)
        inputs['date']=(datetime.strptime(date,"%d-%m-%Y")).strftime('%Y%m%d')
        #get time 30 minutes before hand to allow for prediction model difference
        inputs['start_time']=(datetime.strptime(time,"%H:%M:%S")-timedelta(minutes=30)).strftime('%H:%M:%S')
        inputs['end_time']=(datetime.strptime(time,"%H:%M:%S")+timedelta(minutes=60)).strftime('%H:%M:%S')
        inputs['services']=[]
        for service in Calendar.objects.filter(**{day:1}, start_date__lte=inputs['date'], end_date__gte=inputs['date']):
            inputs['services']+=service.service_id,

        #Finds all trip info for direct routes from one of the given start stations and stop stations
        #within a given time on a specific day.
        #Attributes returned
        #'trip_id', 'arrival_time', 'departure_time', 'trip_headsign', 'route_short_name',
        #'start_stop_id', start_stop_id_long', start_stop_name, 'start_lat', 'start_lon', 'start_num',
        #''end_stop_id', 'end_lat', 'end_lon', 'end_num', end_stop_id_long, end_stop_name'

        trips=StopTimes.objects.raw("SELECT distinct t.trip_headsign, r.route_short_name, st1.trip_id,"\
        +" st1.departure_time, s1.stop_id as start_stop_id_long, s1.stopID_short as start_stop_id, s1.stop_name as start_stop_name,"\
        +"s1.stop_lat as start_lat, s1.stop_lon as start_lon, st1.stop_sequence as start_num, "\
        +"st2.arrival_time, s2.stopID_short as end_stop_id, s2.stop_id as end_stop_id_long, "\
        +"s2.stop_name as end_stop_name, s2.stop_lat as end_lat, s2.stop_lon as end_lon, "\
        +"st2.stop_sequence as end_num FROM website.stop_times as st1, website.stop_times as st2,"\
        +" website.trips as t, website.routes as r, website.stops as s1, "\
        + "website.stops as s2  where st1.stop_id in  %(start_stations)s"\
        +" and st2.stop_id in  %(end_stations)s and st1.stop_sequence<st2.stop_sequence and st1.departure_time>=%(start_time)s and "\
        +"st1.departure_time<=%(end_time)s and st2.departure_time>%(start_time)s"\
        +" and st1.trip_id=t.trip_id and t.service_id in %(services)s and st1.trip_id=st2.trip_id"\
        +"  and r.route_id=t.route_id and s1.stop_id=st1.stop_id"\
        +" and s2.stop_id=st2.stop_id order by s1.stopID_short limit 10;",inputs)
        #validate(self, route_segments, time, day_info, weather)
        #print(trips)
        results=[]
        for trip in trips:
            route=[]
            end_name='destination'
            route+=self.make_walking_segment(start_coord['lat'], start_coord['lon'], trip.start_lat, trip.start_lon, trip.start_stop_name, start_stations[trip.start_stop_id_long]['walking_time'], start_stations[trip.start_stop_id_long]['distance'], time),
            route+=self.make_transit_segment(trip.start_lat, trip.start_lon, trip.end_lat, trip.end_lon, trip.end_stop_name, trip.route_short_name, trip.start_stop_id, trip.end_stop_id, trip.trip_headsign),
            route+=self.make_walking_segment(trip.end_lat, trip.end_lon, end_coord["lat"], end_coord['lon'], end_name, end_stations[trip.end_stop_id_long]['walking_time'], end_stations[trip.end_stop_id_long]['distance']),
            results+=route,
        return results


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
