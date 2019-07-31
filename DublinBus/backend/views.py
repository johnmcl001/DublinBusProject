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
import redis
from itertools import permutations
from .queries import *
from django.db.models import Q, F

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
        services=get_services(day_info['day_long'], day_info['date'])
        trips=get_relevant_stop_times_per_routes_and_stops(stop_number, routes, services, time)
        trips=self.format_trips_into_dict_with_routes_as_key(trips)
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
        results = self.format_results(results)
        return Response(results)

    def format_results(self, results):
        """
        Input: results as json
        Output: formatted results as json
        """
        formatted_results = {"directions": []}
        count=0
        for i in range(0, len(results)):
            if count==10:
                break
            formatted_results["directions"] += [
                {
                    "instruction": results[i]["route"],
                    "time": results[i]["arrival_time"]
                }
            ]
            count+=1
        return formatted_results

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
        for result in weatherResult:
            if result.end_time=="00:00":
                result.end_time="24:00"
                if result.start_time <= (datetime.strptime(time,"%H:%M:%S")+timedelta(minutes=60)).strftime("%H:%M") < result.end_time:
                    forecast = {
                        "temperature": result.temperature,
                        "cloud": result.cloud_percent,
                        "rain": result.rain,
                        "description": result.description,
                    }
                    return forecast
            else:
                if datetime.strptime(result.start_time, "%H:%M") <= (datetime.strptime(time,"%H:%M:%S")+timedelta(minutes=60)) < datetime.strptime(result.end_time, "%H:%M"):
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
            try:
                #Sometimes stop numbers aren't being ran by DB due to maintainence etc.
                #If they are not, frontEndBusInfo will not hold their info.
                busStopInfo = busStopInfo[stop_number]
            except:
                busStopInfo=None
            return busStopInfo

    def get_routes(self, bus_stop_info):
        """
        Input: Http request, bus_stop_info
        Ouput: route(s) as list
        """
        if self.request.GET.get("route") != "null" and self.request.GET.get("route") is not None:
            routes = [self.request.GET.get("route")]
        else:
            routes = bus_stop_info["routes"][0]
        return routes

    def format_trips_into_dict_with_routes_as_key(self, trips):
        """
        Input: Trips Objects in a queryset
        Use to seperate trips into routes to create dataframes for our ML
        Output: Dictionary with route as key and trip objects as a list.
        """
        info={}
        for trip in trips:
            route_short=trip.route_short_name
            if route_short not in info:
                info[route_short]=[trip]
            else:
                info[route_short]+=trip,
        return info

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

        predictions_dict={}
        for route in machine_learning_inputs['trips'].keys():
            predictions_dict[route]={}
            stop_num=[]
            df=pd.DataFrame(columns=['temperature_NORM','PROGRNUMBER_NORM','month','day'])
            for num in range(0, len(machine_learning_inputs['trips'][route])):
                if machine_learning_inputs['trips'][route][num].stop_sequence not in stop_num:
                    stop_num+=machine_learning_inputs['trips'][route][num].stop_sequence,
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
                arrival_time=(datetime.combine(date, machine_learning_inputs['trips'][route][num].arrival_time)+timedelta(seconds=predictions_dict[route][machine_learning_inputs['trips'][route][num].stop_sequence])).time()
                if arrival_time>=time:
                    results+={'stop': machine_learning_inputs['stop_number'], 'route': route, 'arrival_time': arrival_time.strftime("%H:%M:%S"), 'stop':machine_learning_inputs['trips'][route][num].stop, 'trip_id':machine_learning_inputs['trips'][route][num].trip_id},

        return self.sort_results(results)


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
    First tries to find a direct route between the beginning and end stations
    If no direct journeys ar available, it looks for a direct crossover.
    Finally calls API for multi-leg journeys
    """

    def get(self, request):

        time = self.get_time()
        day_info = self.get_day_and_date()
        weather = self.get_weather(time, day_info["date"])
        start_coords = {"lat": self.get_coords("startpointLat"),
                        "lon": self.get_coords("startpointLon")}
        end_coords = {"lat": self.get_coords("departureLat"),
                        "lon": self.get_coords("departureLon")}
        start_stations=get_stations_nearby(start_coords["lat"],
                                                start_coords["lon"])
        end_stations=get_stations_nearby(end_coords["lat"],
                                              end_coords["lon"])
        services=get_services(day_info['day_long'], day_info['date'])
        start_routes=self.get_routes_for_list_of_stops(start_stations['list_stop_short'])
        end_routes=self.get_routes_for_list_of_stops(end_stations['list_stop_short'])
        dir_route = self.find_direct_routes(start_stations,end_stations,
                                            start_routes, end_routes,
                                           services,
                                           time)

        if len(dir_route)!=0:
            dir_route=self.format_direct_route(dir_route, start_coords, end_coords, start_stations, end_stations, time)
            dir_routes=self.validate(dir_route, time, day_info,weather)
            if len(dir_routes)!=0:
                print('direct route')
                results=self.sort_routes(dir_routes)
                results = self.format_response(results)
                return Response(results)
        crossovers=self.bus_crossover(start_stations, start_routes, end_stations, end_routes, services, time)
        if len(crossovers)!=0:
            print('crossover route')
            crossovers=self.format_bus_crossover(crossovers, start_coords, end_coords, start_stations, end_stations, time)
            crossovers=self.validate(crossovers, time, day_info,weather)
            if len(crossovers)!=0:
                results=self.sort_routes(crossovers)
                results = self.format_response(results)
                return Response(results)
        print('api')
        routes = self.get_route(time, day_info['date'], start_coords, end_coords)
        full_journeys = self.get_full_journeys(routes, time)
        full_journeys=self.validate(full_journeys, time, day_info,weather)
        results=self.sort_routes(full_journeys)
        results = self.format_response(results)
        return Response(results)

    def get_coords(self, point):
        """
        Input: http request
        Output: coords as dict
        """
        coords = self.request.GET.get(point)
        return literal_eval(coords)

    def get_route(self, time, date, start_coords, end_coords, mode='transit'):

        """
        Input: origin coords as string, destination coords as string
        Output: route as json
        """
        date=datetime.strptime(date,'%d-%m-%Y')
        time=datetime.strptime(time, '%H:%M:%S').time()
        time=int(datetime.combine(date, time).timestamp())
        key = os.getenv("GOOGLE")
        if mode=='transit':
            call = "https://maps.googleapis.com/maps/api/directions/json?origin="\
            +str(start_coords['lat'])+','+str(start_coords['lon'])+"&destination="+str(end_coords['lat'])+','+str(end_coords['lon'])+"&key="\
            + key + "&mode=transit&transit_mode=bus&alternatives=true&region=ie&departure_time="+str(time)
        else:
            call = "https://maps.googleapis.com/maps/api/directions/json?origin="\
            +str(start_coords['lat'])+','+str(start_coords['lon'])+"&destination="+str(end_coords['lat'])+','+str(end_coords['lon'])+"&key="\
            + key + "&mode="+mode

        response = requests.get(call)
        if response.status_code == 200:
            route = json.loads(response.text)
        elif response.status_code == 400:
            route = "not found"
        return route

    def get_full_journeys(self, route, time):
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
                segment["markers"] = [step["start_location"]["lat"],
            step["start_location"]["lng"],
            step["end_location"]["lat"],
            step["end_location"]["lng"]]
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

    def validate(self, full_journeys, time, day_info, weather):
        """
        Input: a list of routes broken into segments
        Ouput: a list of dictionarys with valid routes based on our ML prediction model
        """
        valid_results=[]
        #loop for each journey option given by google maps
        for journey in full_journeys:
            start=time
            end=time
            #loop for each leg per journey and check if the leg is valid.
            for i in range(0, len(journey)):
                leg=journey[i]
                #if leg is walking end time can be calculated by addition
                if leg["travel_mode"]=="WALKING":
                    valid_result=True
                    leg["end_time"]=(datetime.strptime(leg["start_time"],"%H:%M:%S")+timedelta(seconds=leg["duration_sec"])).strftime('%H:%M:%S')
                    if i !=len(journey)-1:
                        journey[i+1]["start_time"]=leg['end_time']


                #if leg is transit, we must run our machine learning model to
                #ensure a bus will arrive after the previous stage of the journey
                #is complete
                if leg["travel_mode"]=="TRANSIT":
                    if not isinstance(leg["departure_stop"], int):
                        start_stop=get_station_number(leg["departure_stop"], leg["start_lat"], leg["start_lon"])
                    else:
                        start_stop=leg["departure_stop"]
                    if not isinstance(leg["arrival_stop"], int):
                        end_stop=get_station_number(leg["arrival_stop"], leg["end_lat"], leg["end_lon"])
                    else:
                        end_stop=leg["arrival_stop"]
                    if end_stop is None:
                        print('Cant identify stop')

                    #finds all relevant trips that serve the start_stop and journey given by google maps
                    services=get_services(day_info['day_long'],  day_info["date"])
                    trips=get_relevant_stop_times_per_routes_and_stops([start_stop], [leg["route"]],  services, leg["start_time"])
                    trips=self.format_trips_into_dict_with_routes_as_key(trips)
                    machine_learning_inputs = self.serialize_machine_learning_input(
                                                                        leg["start_time"],
                                                                        day_info["day"],
                                                                        day_info["month"],
                                                                        day_info["date"],
                                                                        start_stop,
                                                                        weather,
                                                                        leg["route"],
                                                                        trips)
                    #runs our machine learning on all relevant trips
                    results = self.get_arrival_times(machine_learning_inputs)

                    #loops through the results and runs machine learning on bus arrival times at destination
                    valid_result=False
                    #updates start, end and journey duration in legs.
                    for res in results:
                        #no walking as first stage.
                        if (i==0 and res['arrival_time']>= time) or (i>0 and res['arrival_time']>=leg['start_time']):
                            if res['arrival_time']>= time:
                                index=results.index(res)
                                leg['later_bus_arrivals']=results[index:]
                                leg['start_time']=res['arrival_time']
                                if StopTimes.objects.filter(trip_id=res['trip_id'], stop__stopid_short=end_stop).count()==0:
                                    print('no valid trips')
                                    valid_result=False
                                    break
                                #runs machine learning to find predicted arrival time
                                trips=StopTimes.objects.get(trip_id=res['trip_id'], stop__stopid_short=end_stop)
                                leg['end_time']=trips.arrival_time.strftime('%H:%M:%S')
                                trips=self.format_trips_into_dict_with_routes_as_key([trips])
                                machine_learning_inputs = self.serialize_machine_learning_input(
                                                                                    leg['end_time'],
                                                                                    day_info["day"],
                                                                                    day_info["month"],
                                                                                    day_info["date"],
                                                                                    end_stop,
                                                                                    weather,
                                                                                    leg["route"],
                                                                                    trips)
                                #runs our machine learning on all relevant trips
                                results_end_time = self.get_arrival_times(machine_learning_inputs)
                                leg['end_time']=results_end_time[0]['arrival_time']
                                leg['duration_sec']=(datetime.strptime(leg["end_time"],"%H:%M:%S")-datetime.strptime(leg["start_time"],"%H:%M:%S")).total_seconds()
                                #updates the start_time of next leg as end_time of current leg
                                if i !=len(journey)-1:
                                    journey[i+1]["start_time"]=leg['end_time']
                                valid_result=True
                                break
                    if valid_result==True:
                        end=leg['end_time']
                    #after the leg has been checked, if no valid result has Been
                    #found break out of the journey and dont add to results
                    if valid_result==False:
                        break
            duration=str((datetime.strptime(end,"%H:%M:%S")-datetime.strptime(start,"%H:%M:%S")).total_seconds())
            if valid_result==True and {'duration':duration, 'journey':journey} not in valid_results:
                valid_results+={'duration':duration, 'journey':journey},
        return valid_results

    def sort_routes(self, results):
        """
        Input: Routes results as json
        Output: Routes results sorted into a dictionary where route is key, then stops and times as values
        """
        for journey in range(0, len(results)):
            results[journey]['duration']=float(results[journey]['duration'])
        return sorted(results, key=lambda k: k["duration"])


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
            "markers" : [start_lat, start_lon, end_lat, end_lon]

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
                "departure_stop": start_stop,
                "markers" : [start_lat, start_lon, end_lat, end_lon]

        }

    def format_direct_route(self, trips, start_coord, end_coord, start_stations, end_stations, time):
        results=[]
        for trip in trips:
            route=[]
            end_name='destination'
            route+=self.make_walking_segment(start_coord['lat'], start_coord['lon'], trip.start_lat, trip.start_lon, trip.start_stop_name, start_stations[trip.start_stop_id_long]['walking_time'], start_stations[trip.start_stop_id_long]['distance'], time),
            route+=self.make_transit_segment(trip.start_lat, trip.start_lon, trip.end_lat, trip.end_lon, trip.end_stop_name, trip.route_short_name, trip.start_stop_id, trip.end_stop_id, trip.trip_headsign),
            route+=self.make_walking_segment(trip.end_lat, trip.end_lon, end_coord["lat"], end_coord['lon'], end_name, end_stations[trip.end_stop_id_long]['walking_time'], end_stations[trip.end_stop_id_long]['distance']),
            results+=route,
        return results

    def format_bus_crossover(self, trips, start_coord, end_coord, start_stations, end_stations, time):
        results=[]
        for trip in trips:
            route=[]
            leg1=trip[0]
            leg2=trip[1]
            end_name='destination'
            route+=self.make_walking_segment(start_coord['lat'], start_coord['lon'], leg1.start_lat, leg1.start_lon, leg1.start_stop_name, start_stations[leg1.start_stop_id_long]['walking_time'], start_stations[leg1.start_stop_id_long]['distance'], time),
            route+=self.make_transit_segment(leg1.start_lat, leg1.start_lon, leg1.end_lat, leg1.end_lon, leg1.end_stop_name, leg1.route_short_name, leg1.start_stop_id, leg1.end_stop_id, leg1.trip_headsign),
            route+=self.make_transit_segment(leg2.start_lat, leg2.start_lon, leg2.end_lat, leg2.end_lon, leg2.end_stop_name, leg2.route_short_name, leg2.start_stop_id, leg2.end_stop_id, leg2.trip_headsign),
            route+=self.make_walking_segment(leg2.end_lat, leg2.end_lon, end_coord["lat"], end_coord['lon'], end_name, end_stations[leg2.end_stop_id_long]['walking_time'], end_stations[leg2.end_stop_id_long]['distance']),
            results+=route,
        return results

    def get_routes_for_list_of_stops(self, list_stop_short):
        results={'all':[]}
        for stop in list_stop_short:
            #get all routes that serve a stop
            if stop!=None:
                bus_stop_info = self.get_bus_stop_info(str(stop))
                if bus_stop_info!=None:
                    results['all']+= self.get_routes(bus_stop_info)
                    results[stop]=self.get_routes(bus_stop_info)
        results['all'] = sorted(list(dict.fromkeys(results['all'])))
        return results

    def find_direct_routes(self, start_stations, end_stations, start_routes, end_routes, services, time):
        """
        Input: start poition as dictionary with lat long as keys, end position as dictionary with lat long
               as keys.
        Our own routing which finds a direct route from one station to another.
        Output: 10 routes from start to stop order by stop_ids(for future walking calc)
        """
        #holds information 'start_stations', 'end_stations, 'date', 'start_time', 'end_time' for query
        inputs={}
        #get time 30 minutes before hand to allow for prediction model difference
        inputs['start_time']=(datetime.strptime(time,"%H:%M:%S")-timedelta(minutes=30)).strftime('%H:%M:%S')
        inputs['end_time']=(datetime.strptime(time,"%H:%M:%S")+timedelta(minutes=60)).strftime('%H:%M:%S')

        common_routes=[]
        index=0
        for start_route in start_routes['all']:
            for end_route_index in range(index, len(end_routes['all'])):
                if start_route==end_routes['all'][end_route_index]:
                    common_routes+=start_route,
                    index=end_route_index
                    break
                if start_route<end_routes['all'][end_route_index]:
                    index=end_route_index
                    break
        if len(common_routes)==0:
            print("no common route-no direct")
            return[]
        inputs['start_stations']=tuple(start_stations['list_stop_long'])
        inputs['end_stations']=tuple(end_stations['list_stop_long'])

        inputs['services']=[]
        for service in services:
            inputs['services']+=service.service_id,
        #Finds all trip info for direct routes from one of the given start stations and stop stations
        #within a given time on a specific day.
        #Attributes returned
        #'trip_id', 'arrival_time', 'departure_time', 'trip_headsign', 'route_short_name',
        #'start_stop_id', start_stop_id_long', start_stop_name, 'start_lat', 'start_lon', 'start_num',
        #''end_stop_id', 'end_lat', 'end_lon', 'end_num', end_stop_id_long, end_stop_name'
        for start_station in start_stations['list_stop_long']:
            results=[]
            inputs['common_routes']=[]
            inputs['start_stations']=start_station
            for route in start_routes[start_stations[start_station]['short']]:
                if route in common_routes:
                    inputs['common_routes']=route,
                    trips=StopTimes.objects.raw("SELECT distinct t.trip_headsign, r.route_short_name, st1.trip_id,"\
                    +" st1.departure_time, s1.stop_id as start_stop_id_long, s1.stopID_short as start_stop_id, s1.stop_name as start_stop_name,"\
                    +"s1.stop_lat as start_lat, s1.stop_lon as start_lon, st1.stop_sequence as start_num, "\
                    +"st2.arrival_time, s2.stopID_short as end_stop_id, s2.stop_id as end_stop_id_long, "\
                    +"s2.stop_name as end_stop_name, s2.stop_lat as end_lat, s2.stop_lon as end_lon, "\
                    +"st2.stop_sequence as end_num FROM website.stop_times as st1, website.stop_times as st2,"\
                    +" website.trips as t, website.routes as r, website.stops as s1, "\
                    + "website.stops as s2  where st1.route_short_name in %(common_routes)s and st2.route_short_name in %(common_routes)s and st1.stop_id =  %(start_stations)s"\
                    +" and st2.stop_id in  %(end_stations)s and st1.stop_sequence<st2.stop_sequence and st1.departure_time>=%(start_time)s and "\
                    +"st1.departure_time<=%(end_time)s and st2.departure_time>%(start_time)s"\
                    +" and st1.trip_id=t.trip_id and t.service_id in %(services)s and st1.trip_id=st2.trip_id"\
                    +"  and r.route_id=t.route_id and s1.stop_id=st1.stop_id "\
                    +" and s2.stop_id=st2.stop_id limit 1;",inputs)
                    if len(trips)>0:
                        results+=trips
            if len(results)!=0:
                return results
        return []

    def bus_crossover(self, start_stations, start_routes, end_stations, end_routes, services, time):
        # start_stations={'list_stop_long':['8220DB000037'], 'list_stop_short':['37'], '8220DB000037':{'short':37}}
        # start_routes={'all':['9'], 37:['9']}
        # end_stations={'list_stop_long':['8220DB000895'], 'list_stop_short':[895], '8220DB000895':{'short':895}}
        # end_routes={'all':['140', '142'], 895:['140', '142']}

        stoptimes_all_start_stops=get_relevant_stop_times_per_routes_and_stops(start_stations['list_stop_short'], start_routes['all'], services, time)
        possible_crossovers_stops_leg1=StopTimes.objects.filter(trip_id__in=stoptimes_all_start_stops).values('stop__stopid_short')
        stoptimes_all_end_stops=get_relevant_stop_times_per_routes_and_stops(end_stations['list_stop_short'], end_routes['all'], services, time)
        possible_crossovers_stops_leg2=StopTimes.objects.filter(trip_id__in=stoptimes_all_end_stops).values('stop__stopid_short')
        crossovers=Stops.objects.filter(Q(stopid_short__in=possible_crossovers_stops_leg1)&Q(stopid_short__in=possible_crossovers_stops_leg2)).values('stop_id', 'stopid_short')
        if not crossovers.exists():
            print('no crossover')
            return []
        results=[]
        crossover_stations={'list_stop_long':[], 'list_stop_short':[]}
        for crossover in crossovers:
            crossover_stations['list_stop_long']+=crossover['stop_id'],
            crossover_stations['list_stop_short']+=crossover['stopid_short'],
            crossover_stations[crossover['stop_id']]={'short': crossover['stopid_short']}
        crossover_routes=self.get_routes_for_list_of_stops(crossover_stations['list_stop_short'])
        all_leg1s=self.find_direct_routes(start_stations, crossover_stations, start_routes, crossover_routes, services, time)
        for leg1 in all_leg1s:
            leg2=self.find_direct_routes({'list_stop_long':[leg1.end_stop_id_long], 'list_stop_short':[leg1.end_stop_id], leg1.end_stop_id_long:{'short':leg1.end_stop_id}}, end_stations, {'all':sorted(list(dict.fromkeys(crossover_routes[leg1.end_stop_id]))), leg1.end_stop_id:crossover_routes[leg1.end_stop_id]}, end_routes, services, leg1.arrival_time.strftime("%H:%M:%S"))
            if len(leg2)!=0:
                results+=[leg1, leg2[0]],
        return results


    def format_response(self, results):
        response = []
        count = 0
        #results = results[:3]
        for result in results:
            route_breakdown = {}
            route_breakdown["directions"] = []
            for i in range(0, len(result['journey'])):
                if int(result["journey"][i]["duration_sec"]) == 0:
                    time = 0,
                elif int(result["journey"][i]["duration_sec"]) < 60:
                    time = 1,
                else:
                    time = result["journey"][i]["duration_sec"] // 60
                route_dict = {
                    "instruction": result["journey"][i]["instruction"],
                    "time": time,
                }
                route_dict["travel_mode"] = ""
                if result["journey"][i]["travel_mode"] == "TRANSIT":
                    route_dict["travel_mode"] = result["journey"][i]["route"]
                else:
                    route_dict["travel_mode"] = "WALKING"

                if route_dict["travel_mode"] != "WALKING":
                    route_dict["instruction"] = route_dict["instruction"].replace("Bus", route_dict["travel_mode"])
                route_breakdown["duration"] = 0
                for time in route_breakdown["directions"]:
                    route_breakdown["duration"] += time["time"]
                route_breakdown["directions"] += [route_dict]

            response += [route_breakdown]
        return response[0:3]

    """        for i in range(0,len(results)):
            result=results[i]
            route_breakdown = {"instructions": {'total_journey_time':[], 'instruction_breakdown':[]}, "markers": [], "polylines": [], "busInfo": {'route':[]}, "travel_mode": []}
            route_breakdown['instructions']['total_journey_time']=result['duration']
            for j in range(0, len(result['route'])):
                segment=result['route'][j]
                route_breakdown['travel_mode']+=segment['travel_mode'],
                if segment['travel_mode']=='WALKING':
                    route_breakdown["instructions"]['instruction_breakdown']+=[segment['instruction']+ '\t Distance'+str(segment['distance'])+'km.']
                else:
                    route_breakdown["instructions"]['instruction_breakdown']+=[segment['instruction']]
                if segment['travel_mode']=='TRANSIT':
                    route_breakdown["instructions"]['instruction_breakdown'][j]+="\nDeparture stop: "+str(segment['arrival_stop'])
                    route_breakdown["instructions"]['instruction_breakdown'][j]+="\nPredicted bus departure time: "+str(segment['arrival_stop'])
                    route_breakdown["instructions"]['instruction_breakdown'][j]+="\nArrival stop: "+str(segment['arrival_stop'])
                    if len(segment['later_bus_arrivals']) !=0:
                        route_breakdown["instructions"]['instruction_breakdown'][j]+="\nLater departure times: "
                        for k in range(0, len(segment['later_bus_arrivals'])):
                            route_breakdown["instructions"]['instruction_breakdown'][j]+=str(segment['later_bus_arrivals'][k]['arrival_time'])+","
                        route_breakdown["instructions"]['instruction_breakdown'][j]=route_breakdown["instructions"]['instruction_breakdown'][j][:-1]
                route_breakdown["instructions"]['instruction_breakdown'][j]+='\nJourney leg travel time: '+str(segment['duration_sec'])
                for marker in segment['markers']:
                    if marker not in route_breakdown['markers']:
                            route_breakdown['markers']+=marker,
                if 'polyline' in segment.keys():
                    route_breakdown['polylines']+=segment['polyline'],
                if segment['travel_mode']=='TRANSIT':
                    route_breakdown['busInfo']['route']+=segment['route'],
            response+=route_breakdown,
    """



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


class TouristPlanner(views.APIView):
    """
    Returns best route through series of tourist destinations
    """

    def get(self, request):
        """
        Input: user http request
        Output: array of lowest cost route
        """
        attractions = self.get_attractions()
        home = self.get_home()
        home_coords = self.get_home_coords(home)
        attractions = self.remove_home_from_attractions(attractions, home)
        attractions = list(permutations(attractions))
        attractions = self.convert_tuples_to_list(attractions)
        attractions = self.add_home(attractions, home)
        best_route = self.get_best_route(attractions)
        best_route_formatted = self.format_route(best_route, home, home_coords)
        return Response(best_route_formatted)

    def format_route(self, best_route, home, home_coords):
        """
        Input: best route as an array
        Output:best route formatted as json
        """

        results = []
        for i in range(len(best_route[0])-1):
            if best_route[0][i] != home and best_route[0][i+1] != home:
                start_lat = Touristattractions.objects.filter(name=best_route[0][i])[0].lat
                start_lon = Touristattractions.objects.filter(name=best_route[0][i])[0].lon
                end_lat = Touristattractions.objects.filter(name=best_route[0][i+1])[0].lat
                end_lon = Touristattractions.objects.filter(name=best_route[0][i+1])[0].lon
            elif best_route[0][i] == home:
                start_lat = home_coords["lat"]
                start_lon = home_coords["lon"]
                end_lat = Touristattractions.objects.filter(name=best_route[0][i+1])[0].lat
                end_lon = Touristattractions.objects.filter(name=best_route[0][i+1])[0].lon
            else:
                start_lat = Touristattractions.objects.filter(name=best_route[0][i])[0].lat
                start_lon = Touristattractions.objects.filter(name=best_route[0][i])[0].lon
                end_lat = home_coords["lat"]
                end_lon = home_coords["lon"]

            results += [{
                "number": i+1,
                "attraction": best_route[0][i] + " to " + best_route[0][i+1],
                "start_lat": start_lat,
                "start_lon": start_lon,
                "end_lat": end_lat,
                "end_lon": end_lon
            }]

        return results

    def get_attractions(self):
        """
        Input: request from user
        Output: attractions as array
        """
        return literal_eval(self.request.GET.get("attractions", ["this", "didn't", "work"]))


    def get_home(self):
        """
        Input: request from user
        Output: home as string
        """
        return self.request.GET.get("home")

    def remove_home_from_attractions(self, attractions, home):
        """
        Input: attractions as array, home as string
        Output: home removed from attractions
        """
        while home in attractions:
            attractions.remove(home)
        return attractions

    def convert_tuples_to_list(self, attractions):
        """
        Input: List of tuples
        Output: List of lists
        """
        for i in range(len(attractions)):
            attractions[i] = list(attractions[i])
        return attractions

    def add_home(self, permutations, home):
        """
        Input: permutations as array of arrays, home as string
        Output: home added to start and end of each permutation
        """
        if permutations[0][0] != home:
            for i in range(len(permutations)):
                permutations[i] = [home] + permutations[i] + [home]
        return permutations

    def get_best_route(self, attractions):
        """
        Input: permutations as array of arrays
        Output: lowest cost permutation as array, cost of permutation
        """
        minimum = float("inf")
        lowest_cost_permutation = []
        r = redis.Redis(host="localhost", port=6379, db=0)

        for permutation in attractions:
            total_cost = 0
            i = 0
            while total_cost < minimum and i < len(permutation)-1:
                if r.exists(str(permutation[i]) + " " + str(permutation[i+1])):
                    cost = r.get(str(permutation[i]) + " " + str(permutation[i+1]))
                    total_cost += int(cost.decode())
                elif i == 0:
                    cost = self.get_cost_from_api(permutation[i], permutation[i+1])
                    r.set(str(permutation[i]) + " " + str(permutation[i+1]), cost, ex=3600)
                    total_cost += cost
                elif i == len(permutation)-2:
                    cost = self.get_cost_from_api(permutation[i], permutation[i+1])
                    r.set(str(permutation[i]) + " " + str(permutation[i+1]), cost, ex=3600)
                    total_cost += cost
                else:
                    cost = self.get_cost_from_database(permutation[i], permutation[i+1])
                    r.set(str(permutation[i]) + " " + str(permutation[i+1]), cost, ex=3600)
                    total_cost += cost
                i += 1
            if total_cost < minimum:
                lowest_cost_permutation = permutation
                minimum = total_cost

            return lowest_cost_permutation, minimum

    def get_home_coords(self, home):
        """
        Input: home as string
        Output: home coordinates as dicitonary
        """

        if Touristattractions.objects.filter(name__contains=home).exists():
            info = Touristattractions.objects.filter(name__contains=home)[0]
            return {"lat": info.lat, "lon": info.lon}
        else:
            call = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="+home.replace(" ", "+")+"&inputtype=textquery&fields=photos,formatted_address,name,opening_hours,geometry&key=" + os.getenv("GOOGLE")
            response = requests.get(call).text
            info = json.loads(response)["candidates"][0]
            name = info["name"]
            lat = info["geometry"]["location"]["lat"]
            lon = info["geometry"]["location"]["lng"]

            new_place = Touristattractions(
                name = name,
                lat = lat,
                lon = lon,
                description = "",
                rating = 0.0,
                raters = 0,
                address = ""
            )

            new_place.save()
            return {"lat": lat, "lon": lon}



    def get_cost_from_api(self, origin, destination):
        """
        Input: origin, destination as string
        Output: cost as int
        """
        call = "https://maps.googleapis.com/maps/api/directions/json?origin=" + origin + "&destination=" + destination + "&key=" + os.getenv("GOOGLE") + "&mode=transit&transit_mode=bus&region=IE"
        response = requests.get(call)
        response_json = json.loads(response.text)
        result = response_json["routes"][0]["legs"][0]["distance"]["value"]
        return result

    def get_cost_from_database(self, origin, destination):
        """
        Input: origin, destination as string
        Output: cost as int
        """
        return Costs.objects.filter(origin=origin, destination=destination)[0].cost

class GetTouristAttractions(generics.ListCreateAPIView):
    """
    Handles returning results from database for journey planner attraction info
    """
    queryset = Touristattractions.objects.all()
    serializer_class = RouteSerializer

class RouteView(generics.ListCreateAPIView):
    """
    Shows routes table
    """
    queryset = Routes.objects.all()
    serializer_class = RouteSerializer
