from django.db.models import Q
from .serializers import *
from .models import *
from datetime import datetime, timedelta, date

def get_services(day, date):
    date=(datetime.strptime(date,"%d-%m-%Y")).strftime('%Y%m%d')
    not_running=CalendarDates.objects.filter(date=date, exception_type=2).values('service_id')
    extra=CalendarDates.objects.filter(date=date, exception_type=1).values('service_id')
    services=Calendar.objects.filter((Q(**{day:1}, start_date__lte=date, end_date__gte=date) | Q(service_id__in=extra)) & ~Q(service_id__in=not_running))
    return services

def get_trip_object(route, services, value=False):
    if value:
        return Trips.objects.filter(service__in=services, route__route_short_name=route).values(value)
    return Trips.objects.filter(service__in=services, route__route_short_name=route)

def get_relevant_stop_times_per_routes_and_stops(stop_numbers, route_numbers, day, time, date):
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
    start_time=(datetime.strptime(time,"%H:%M:%S")-timedelta(minutes=30)).strftime('%H:%M:%S')
    end_time=(datetime.strptime(time,"%H:%M:%S")+timedelta(minutes=60)).strftime('%H:%M:%S')
    services=Calendar.objects.filter(**{day:1}, start_date__lte=date, end_date__gte=date)
    long_ids=Routes.objects.filter(route_short_name__in=route_numbers)
    trips=Trips.objects.filter(route_id__in=long_ids, service_id__in=services).values('trip_id')
    trips=StopTimes.objects.filter(trip_id__in=trips, departure_time__gte=start_time, departure_time__lte=end_time, stop__stopid_short__in=stop_numbers).order_by('departure_time')
    return trips


def get_direction( day, date, route_numbers, stop_number):
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
        allRoutes=Trips.objects.filter(route__route_short_name=route, trip__in=allTrips, service_id__in=services).values('direction_id', 'route__route_long_name').distinct()
        if len(allRoutes) > 0:
            directions[route] = allRoutes[0]
    return directions

def get_station_number( name, dest_lat, dest_lon):
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

def walking_time(distance, speed=4):
    """
    Input: distance from stop, speed is by default 4km/hr
    Output: time(in seconds) needed to walk to the bus stops
    """
    return round((float(distance)/float(speed))*3600)

def get_stations_nearby(dest_lat, dest_lon, num_stations=8, radius=5):
    """
    Input: Centre point coordinates
    Output: Dictionary of stops with stop id as key and distance in m from centre point as value
    """
    default_radius=1 #km
    station_list=[]
    #for results that are not null, the more stations we check the better
    #trade off-response time
    while default_radius<radius and len(station_list)<10:
        station_list=Stops.objects.raw('SELECT distinct(stop_id), stopID_short,'\
        +' ( 6371 * acos( cos( radians(%(dest_lat)s) ) * cos( radians( stop_lat ) ) *'\
        + ' cos( radians( stop_lon ) - radians(%(dest_lon)s) ) + sin( radians(%(dest_lat)s) )'\
        +' * sin( radians( stop_lat ) ) ) ) AS distance FROM website.stops HAVING distance < '\
        +'%(default_radius)s ORDER BY distance limit 20;',{'dest_lat':str(dest_lat), 'dest_lon':str(dest_lon), 'default_radius':str(default_radius)})
        default_radius+=.5
    if (len(list(station_list))==0):
        print("No stations found nearby")
        return None

    station_dict={'list_stop_long':[], 'list_stop_short':[]}
    for station in station_list:
        station_dict['list_stop_long']+=station.stop_id,
        station_dict['list_stop_short']+=station.stopid_short,
        station_dict[station.stop_id]={'short': station.stopid_short, 'distance':round(station.distance*1000), 'walking_time':walking_time(station.distance)}
    return station_dict
