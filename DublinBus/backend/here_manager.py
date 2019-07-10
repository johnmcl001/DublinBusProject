"""
Manages Here API calls and returns
"""


class HereManager:

    def get_response(start):
        """
        Input: none
        Output: list of stations
        """
        api = 'https://transit.api.here.com/v3/stations/by_geocoord.json?center='+start['lat']+'%2C'+start['lon']+'&radius='+1000+'&app_id='+SECRET+'&app_code='+SECRET
        if response.status_code != 200:
            return("This service is currently unavailable")
        else:
            return response.json()["Res"]["Stations"]["Stn"]

    def get_stations(data):
        """
        Input: list of stations
        Output: Station info as dict
        """
        stations = {}
        for station in len(data):
            id = Stops.objects.filter(stop_name__contains=station["name"])

            if len(id) != 1:
                id = Stops.objects.filter(stop_lon__contains=station["x"],
                                          stop_lat__contains=station["y"])
                if len(id) != 0:
                    id = Stops.objects.filter(stop_lon__contains=station["x"][:-1], stop_lat__contains=station["y"][:-1])
            stations[id.stopid_short] = {
                'name':data[i]['name'],
                'distance':data[i]['distance'],
                'duration':data[i]['duration'],
                'Transport':data[i]['Transports']
            }

        return stations
