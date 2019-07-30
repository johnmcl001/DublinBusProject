"""
Tests for django backend
"""

from django.test import RequestFactory, TestCase

from .views import *
from datetime import datetime, timedelta, date

# Create your tests here.


class SearchByStopTest(TestCase):
    """
    UnitTests for SearchByStops Feature
    """

    def setUp(self):
        """
        Setup fake models for testing
        """
        Forecast.objects.create(
            date = '02-07-2019',
            start_time = '22:00',
            end_time = '23:00',
            temperature = '19',
            cloud_percent = '11',
            rain = '2',
            description='Sunny',
        )
        Forecast.objects.create(
            date = '03-2-2019',
            start_time = '21:00',
            end_time = '22:00',
            temperature = '19',
            cloud_percent = '11',
            rain = '2',
            description='Sunny',
        )

        Trips.objects.create(
            route = Routes.objects.create(
                route_id='7b long',
                route_type=2,
                agency=Agency.objects.create(
                    agency_url = '04',
                    agency_name = 'DB',
                    agency_timezone = 'Dublin/Europe',
                    agency_id = '03',
                    agency_lang='en'
                ),
                route_short_name='7d',
            ),
            direction_id = 1,
            trip_headsign = 'towards town',
            shape_id = 'ascd',
            service = Calendar.objects.create(
                service_id = "12345",
                start_date = "20190303",
                end_date = "20190615",
                monday = "1",
                tuesday = "0",
                wednesday = "0",
                thursday = "0",
                friday = "0",
                saturday = "0",
                sunday = "0"
            ),
            trip = StopTimes.objects.create(
                    trip_id = "1.1.60-79-b12-1.346.I",
                    arrival_time = "07:30:00 ",
                    departure_time = "07:30:00",
                    stop = Stops.objects.create(
                        stop_lat = 123,
                        zone_id = 123,
                        stop_lon = 123,
                        stop_id = 'big7556',
                        stop_name = 'testname',
                        location_type = 0,
                        stopid_short ='7556',
                    ),
                    stop_sequence = "1",
                    stop_headsign = "Aston Quay",
                    shape_dist_traveled = None,
            ),
        )

        Routes.objects.create(
            route_id='7d long',
            route_type=2,
            agency=Agency.objects.create(
                agency_url = '03',
                agency_name = 'DB',
                agency_timezone = 'Dublin/Europe',
                agency_id = '04',
                agency_lang='en'
            ),
            route_short_name='7d',
        )

        self.factory = RequestFactory()
        self.request_specific = self.factory.get("/api/stop/?stop=2007&route=7D&time=14:00&date=02-07-2019")
        self.request_not_specific = self.factory.get("/api/stop/?stop=2007")
        self.test_view_specific = self.setup_view(SearchByStop(),
                                                  self.request_specific)
        self.test_view_not_specific = self.setup_view(SearchByStop(),
                                                  self.request_not_specific)

        def tearDown(self):
            del self.test_view

    def setup_view(self, view, request, *args, **kwargs):
        """
        Sets up view so its methods can be called and tested
        """
        view.request = request
        view.args = args
        view.kwargs = kwargs
        return view

    def test_get_time_now(self):
        """
        Should return time now as a string
        """
        now = datetime.now().strftime("%H:%M")
        self.assertEqual(self.test_view_not_specific.get_time(), now)

    def test_get_time_specified(self):
        """
        Should return time specified in url as a string
        """
        self.assertEqual(self.test_view_specific.get_time(), "14:00")

    def test_get_day_today(self):
        """
        Should return today as a string
        """
        today = datetime.now().strftime("%a")
        self.assertEqual(self.test_view_not_specific.get_day_and_date()["day"],             today)

    def test_get_day_specified(self):
        """
        Should return day specified in url as a string
        """
        self.assertEqual(self.test_view_specific.get_day_and_date()["day"], "Tue")

    def test_get_date_today(self):
        """
        Should return date now as a string
        """
        today = datetime.now().strftime("%d-%m-%Y")
        self.assertEqual(self.test_view_not_specific.get_day_and_date()["date"], today)

    def test_get_date_specified(self):
        """
        Should return date specified in url as a string
        """
        self.assertEqual(self.test_view_specific.get_day_and_date()["date"], "02-07-2019")

    def test_get_weather(self):
        """
        Should return weather forecast as dictionary
        """
        expected_results = {
            "temperature": '19',
            "cloud": '11',
            "rain": '2',
            "description": 'Sunny',
        }
        self.assertEqual(self.test_view_specific.get_weather("22:39", '02-07-2019'), expected_results)

    def test_get_bus_stop_info(self):
        """
        Should return info for a stop as a dictionary
        """
        expected_result = {
          "lat":53.2480439849,
          "long":-6.12315403365,
          "name":"Abberley",
          "routes":[
             [
                "7D",
                "7B"
             ]
          ]
       }
        self.assertEqual(self.test_view_specific.get_bus_stop_info("7556"), expected_result)

    def test_get_routes_none_specified(self):
        """
        Should return route info
        """
        bus_stop_info = {
          "lat":53.2480439849,
          "long":-6.12315403365,
          "name":"Abberley",
          "routes":[
             [
                "7D",
                "7B"
             ]
          ]
        }
        self.assertEqual(self.test_view_not_specific.get_routes(bus_stop_info),
                                                    ["7D", "7B"])

    def test_get_routes_specified(self):
        """
        Should return route info
        """
        bus_stop_info = {
          "lat":53.2480439849,
          "long":-6.12315403365,
          "name":"Abberley",
          "routes":[
             [
                "7D",
                "7B"
             ]
          ]
        }
        self.assertEqual(self.test_view_specific.get_routes(bus_stop_info),
                                                    ["7D"])

    def test_get_direction(self):
        """
        Should return direction per route per stop as a dictionary
        """
        expected_results = {"7d": {"direction_id": 1, "trip_headsign": "towards town"}}
        self.assertEqual(self.test_view_specific.get_direction(['7d'], "7556"), expected_results)

    def test_serialize_machine_learning_input(self):
        """
        Should return machine learning inputs as json type
        """
        time = "23:39"
        day = "Tue"
        date = "02-07-2019"
        stop_number = "2007"
        weather = {"temp": "20", "precipitation": "34%", "wind": "23"}
        routes = ["7b", "7d", "46a", "47", "84x", "116", "145", "155"]
        directions = {"7d": "1"}
        result = {
            "time": time,
            "day": day,
            "date": date,
            "stop_number": stop_number,
            "weather": weather,
            "routes": routes,
            "directions": directions
        }
        self.assertEqual(self.test_view_specific.serialize_machine_learning_input(
            time,
            day,
            date,
            stop_number,
            weather,
            routes,
            directions), result)

    def test_get_arrival_times(self):
        """
        Should return route number, arrival time and travel time
        """
        pass

    def test_sort_results(self):
        """
        Should return machine learning results sorted as json
        """
        test_input = [
            {"route": "46a", "arrival_time": 4, "travel_time": None},
            {"route": "39a", "arrival_time": 2, "travel_time": None},
            {"route": "145", "arrival_time": 1, "travel_time": None},
            {"route": "46a", "arrival_time": 8, "travel_time": None},
            {"route": "155", "arrival_time": 6, "travel_time": None}
        ]
        test_output = [
            {"route": "145", "arrival_time": 1, "travel_time": None},
            {"route": "39a", "arrival_time": 2, "travel_time": None},
            {"route": "46a", "arrival_time": 4, "travel_time": None},
            {"route": "155", "arrival_time": 6, "travel_time": None},
            {"route": "46a", "arrival_time": 8, "travel_time": None},
        ]
        self.assertEqual(self.test_view_specific.sort_results(test_input), test_output)



class StopsAutoCompleteTest(TestCase):
    """
    UnitTests for StopsAutoComplete
    """

    def setUp(self):
        """
        Setup fake models for testing
        """
        Forecast.objects.create(
            date = '02-07-2019',
            start_time = '22:00',
            end_time = '23:00',
            temperature = '19',
            cloud_percent = '11',
            rain = '2',
            description='Sunny',
        )
        Forecast.objects.create(
            date = '03-2-2019',
            start_time = '21:00',
            end_time = '22:00',
            temperature = '19',
            cloud_percent = '11',
            rain = '2',
            description='Sunny',
        )

        Trips.objects.create(
            route = Routes.objects.create(
                route_id='7b long',
                route_type=2,
                agency=Agency.objects.create(
                    agency_url = '04',
                    agency_name = 'DB',
                    agency_timezone = 'Dublin/Europe',
                    agency_id = '03',
                    agency_lang='en'
                ),
                route_short_name='7d',
            ),
            direction_id = 1,
            trip_headsign = 'towards town',
            shape_id = 'ascd',
            service = Calendar.objects.create(
                service_id = "12345",
                start_date = "20190303",
                end_date = "20190615",
                monday = "1",
                tuesday = "0",
                wednesday = "0",
                thursday = "0",
                friday = "0",
                saturday = "0",
                sunday = "0"
            ),
            trip = StopTimes.objects.create(
                    trip_id = "1.1.60-79-b12-1.346.I",
                    arrival_time = "07:30:00 ",
                    departure_time = "07:30:00",
                    stop = Stops.objects.create(
                        stop_lat = 123,
                        zone_id = 123,
                        stop_lon = 123,
                        stop_id = 'big7556',
                        stop_name = 'testname',
                        location_type = 0,
                        stopid_short ='7556',
                    ),
                    stop_sequence = "1",
                    stop_headsign = "Aston Quay",
                    shape_dist_traveled = None,
            ),
        )

        Routes.objects.create(
            route_id='7d long',
            route_type=2,
            agency=Agency.objects.create(
                agency_url = '03',
                agency_name = 'DB',
                agency_timezone = 'Dublin/Europe',
                agency_id = '04',
                agency_lang='en'
            ),
            route_short_name='7d',
        )

        self.factory = RequestFactory()

        self.request = self.factory.get("/api/stop/?route=46a&day=monday&direction=Dun Laoghaire")
        self.test_view = self.setup_view(StopsAutocomplete(),
                                                  self.request)

        def tearDown(self):
            del self.test_view

    def setup_view(self, view, request, *args, **kwargs):
        """
        Sets up view so its methods can be called and tested
        """
        view.request = request
        view.args = args
        view.kwargs = kwargs
        return view

    def test_get_params(self):
        """
        Should return url params as dict
        """
        expected = {
            "route": "46a",
            "direction": "Dun Laoghaire",
        }
        self.assertEqual(self.test_view.get_params(), expected)

class TouristPlannerTest(TestCase):
    """
    UnitTests for StopsAutoComplete
    """

    def setUp(self):
        """
        Setup fake models for testing
        """
        Touristattractions.objects.create(
            name="C",
            lat=3.3,
            lon=4.4,
            description="this",
            rating=3.3,
            raters=2,
            address="ee"
        )
        Costs.objects.create(
            origin=Touristattractions.objects.create(
                name="A",
                lat=3.3,
                lon=4.4,
                description="this",
                rating=3.3,
                raters=2,
                address="ee"
            ),
            destination=Touristattractions.objects.create(
                name="B",
                lat=3.3,
                lon=4.4,
                description="this",
                rating=3.3,
                raters=2,
                address="ee"
            ),
            cost=7
        )

        self.factory = RequestFactory()

        self.request = self.factory.get("""/api/touristplanner/?attractions=["Trinity+College+Dublin","The+Spire","Guinness+Storehouse"]&home=Westin""")
        self.test_view = self.setup_view(TouristPlanner(),
                                                  self.request)

        def tearDown(self):
            del self.test_view

    def setup_view(self, view, request, *args, **kwargs):
        """
        Sets up view so its methods can be called and tested
        """
        view.request = request
        view.args = args
        view.kwargs = kwargs
        return view

    def test_get_attractions(self):
        """
        Should return tourist attractions as array
        """
        expected = [
            "Trinity College Dublin",
            "The Spire",
            "Guinness Storehouse",
            "Westin"
        ]
        self.assertEqual(self.test_view.get_attractions(), expected)

    def test_get_home(self):
        """
        Should return home as string
        """
        self.assertEqual(self.test_view.get_home(), "Westin")

    def test_remove_home_from_attractions(self):
        """
        Should return attractions without home as array
        """
        test_input = [
            "Trinity College Dublin",
            "The Spire",
            "Guinness Storehouse",
            "Westin"
        ]

        expected = [
            "Trinity College Dublin",
            "The Spire",
            "Guinness Storehouse",
        ]
        self.assertEqual(self.test_view.remove_home_from_attractions(test_input, "Westin"), expected)

    def test_compute_permutations(self):
        """
        Should return all permutations of attractions
        """
        test_input = ["A", "B", "C"]
        expected = [
            ['A', 'B', 'C'],
            ['B', 'A', 'C'],
            ['C', 'A', 'B'],
            ['A', 'C', 'B'],
            ['B', 'C', 'A'],
            ['C', 'B', 'A'],

        ]
        self.assertEqual(self.test_view.compute_permutations(len(test_input),
                                                             test_input),
                                                            expected)

    def test_add_home(self):
        """
        Should return permuatations with home added as array of arrays
        """
        test_input = [
            ['A', 'B', 'C'],
            ['B', 'A', 'C'],
            ['C', 'A', 'B'],
            ['A', 'C', 'B'],
            ['B', 'C', 'A'],
            ['C', 'B', 'A'],

        ]
        expected = [
            ['D', 'A', 'B', 'C', 'D'],
            ['D', 'B', 'A', 'C', 'D'],
            ['D', 'C', 'A', 'B', 'D'],
            ['D', 'A', 'C', 'B', 'D'],
            ['D', 'B', 'C', 'A', 'D'],
            ['D', 'C', 'B', 'A', 'D'],

        ]
        self.assertEqual(self.test_view.add_home(test_input, "D"), expected)

    def test_get_cost_from_database(self):
        """
        Should return cost as int
        """
        self.assertEqual(self.test_view.get_cost_from_database("A", "B"), 7)
