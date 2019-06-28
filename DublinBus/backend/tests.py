"""
Tests for django backend
"""

from django.test import RequestFactory, TestCase
from django.test import Client
from django.urls import reverse


from .views import *

client = Client()

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

        """
        For this one I built each function one at a time and changed what
        the class was returning because I couldn't figure out how to
        call individual methods without returning the overall result
        """

    def setup_view(view, request, *args, **kwargs):
        view.request = request
        view.args = args
        view.kwargs = kwargs
        return view

    def test_get_stop_number(self):
        """
        Should return stop number as a string
        """
        request = self.factory.get("/api/stop/?stop=2007&time=14:00:00&day=wed")
        v = setup_view(SearchByStop(), request)
        self.assertEqual(v.get_params("stopnumber"), "2007")
