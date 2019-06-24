"""
Tests for django backend
"""

from django.test import TestCase
from .models import Routes, Stops

# Create your tests here.


class StopsTests(TestCase):
    """
    UnitTests for Stops Model
    """
    def setUp(self):
        """
        Setup fake model for testing
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

    def test_query_stop_name(self):
        """
        Should return stop name string
        """
        stop = Stops.objects.filter(stop_id__endswith=3365)
        stop_name = stop.values("stop_name")[0]["stop_name"]
        self.assertEqual(stop_name, "Abberley")

class RoutesTests(TestCase):
    """
    Unit tests for Routes Model
    """
    def setUp(self):
        """
        Set up fake model for testing
        """
        Routes.objects.create(
            route_id="1",
            route_type=1,
            agency_id="2",
            route_short_name="test"
        )

    def test_query_short_name(self):
        """
        Should return route name string
        """
        route = Routes.objects.filter(route_id="1")
        short_name = route.values("route_short_name")[0]["route_short_name"]
        self.assertEqual(short_name, "test")
