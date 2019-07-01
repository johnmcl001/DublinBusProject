"""
Tests for django backend
"""

from django.test import RequestFactory, TestCase

from .views import *


# Create your tests here.


class SeactByStopTest(TestCase):
    """
    UnitTests for SearchByStops Feature
    """

    def setUp(self):
        """
        Setup fake models for testing
        """
        Stops.objects.create(
            index=1,
            stop_lat=53,
            zone_id=0,
            stop_lon=-6,
            stop_id="12315403365",
            stop_name="Abberley",
            location_type=0,
        )

        Trips.objects.create(
            route_id="60-1-b12-1",
            direction_id=0,
            trip_headsign="Shanard Road (Shanard Avenue) - Saint John's Road East",
            shape_id="60-1-b12-1.1.O",
            service_id="2_merged_7780 ",
            trip_id="14733.2.60-1-b12-1.1.O"
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

    def test_serialize_machine_learning_input(self):
        """
        Should return machine learning inputs as json type
        """
        stop_number = "2007"
        weather = {"temp": "20", "precipitation": "34%", "wind": "23"}
        routes = ["7b", "7d", "46a", "47", "84x", "116", "145", "155"]
        direction = 1
        result = {
            "stop_number": stop_number,
            "weather": weather,
            "routes": routes,
            "direction": direction
        }
        self.assertEqual(self.test_view.serialize_machine_learning_input(
            stop_number,
            weather,
            routes,
            direction), result)

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

    def test_get_routes(self):
        self.assertEqual(self.test_view.get_routes("7556"), 0)
