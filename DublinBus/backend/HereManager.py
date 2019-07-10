"""
Manages Here API calls and returns
"""

from requests import get
from .models import Stops
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)
import os

class HereManager:
    """
    Manages Here API
    """
    @staticmethod
    def get_response(start):
        """
        Input: none
        Output: list of stations
        """
        while True:
            default_radius=1000
            api='https://transit.api.here.com/v3/stations/by_geocoord.json?center='+start['lat']+'%2C'+start['lon']+'&radius='+str(default_radius)+'&app_id='+os.environ.get("HERE_KEY")+'&app_code='+os.environ.get("HERE_CODE")
            response=get(api)
            if response.status_code != 200:
                return("This service is currently unavailable")
            else:
                data = response.json()
                if 'Stations' in data['Res'].keys():
                    return data['Res']['Stations']['Stn']
                else:
                    default_radius+=100

    @staticmethod
    def get_stations(data):
        stations={}
        for i in len(data):
            #HERE API returns stop ids which do not match DublinBus-Must convert
            id=Stops.objects.filter(stop_name__contains=data[i]['name'])
            #sometimes the search for name returns more than 1 result
            if len(id)!=1:
                #search by lat and long
                id=Stops.objects.filter(stop_lon__contains=data[i]['x'], stop_lat__contains=data[i]['y'])
                if len(id)!=0:
                    #search by a shorter lat long string
                    id=Stops.objects.filter(stop_lon__contains=data[i]['x'][:-1], stop_lat__contains=data[i]['y'][:-1])
            stations[id.stopid_short]={'name':data[i]['name'], 'distance':data[i]['distance'], 'duration':data[i]['duration'], 'Transport':data[i]['Transports']}

        return stations


