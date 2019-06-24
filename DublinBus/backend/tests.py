from django.test import TestCase
from .models import *

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
        Should return tuple with coordinates
        """
        stop = Stops.objects.filter(stop_id__endswith=3365)
        stop_name = stop.values("stop_name")[0]["stop_name"]
        self.assertEqual(stop_name, "Abberley")
