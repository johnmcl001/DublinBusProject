"""
Tests for django backend
"""

from django.test import RequestFactory, TestCase

from .views import *
import datetime


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
            date = '02-2-2019',
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
                        index = 12,
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
        self.request = self.factory.get("/api/stop/?stop=2007&time=14:00:00&day=wed")
        self.test_view = self.setup_view(SearchByStop(), self.request)

    def setup_view(self, view, request, *args, **kwargs):
        """
        Sets up view so its methods can be called and tested
        """
        view.request = request
        view.args = args
        view.kwargs = kwargs
        return view

    def test_get_params_stop(self):
        """
        Should return time as a string
        """
        self.assertEqual(self.test_view.get_params("stop"), "2007")

    def test_get_params_time(self):
        """
        Should return stop number as a string
        """
        self.assertEqual(self.test_view.get_params("time"), "14:00:00")

    def test_get_params_day(self):
        """
        Should return day as a string
        """
        self.assertEqual(self.test_view.get_params("day"), "wed")

    def test_get_weather(self):
        expected_results = {
            "temperature": '19',
            "cloud_percent": '11',
            "rain": '2',
            "description": 'Sunny',
        }
        self.assertEqual(self.test_view.get_weather("23:39", '02-2-2019'), expected_results)

    def test_get_routes(self):
        self.assertEqual(self.test_view.get_routes("7556"), ['7D', '7B'])

    def test_get_direction(self):
        expected_results = {"7d": {"direction_id": 1, "trip_headsign": "towards town"}}
        self.assertEqual(self.test_view.get_direction(['7d'], "7556"), expected_results)

    def test_serialize_machine_learning_input(self):
        """
        Should return machine learning inputs as json type
        """
        stop_number = "2007"
        weather = {"temp": "20", "precipitation": "34%", "wind": "23"}
        routes = ["7b", "7d", "46a", "47", "84x", "116", "145", "155"]
        directions = {"7d": "1"}
        result = {
            "stop_number": stop_number,
            "weather": weather,
            "routes": routes,
            "directions": directions
        }
        self.assertEqual(self.test_view.serialize_machine_learning_input(
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
        self.assertEqual(self.test_view.sort_results(test_input), test_output)

