"""
Create backend urls here
"""

from django.urls import path, include
from rest_framework import routers
from .views import *


# Specify url patterns within project
urlpatterns = [
    path("lead/", RouteView.as_view()),
    path("stop/", SearchByStop.as_view()),
    path("destination/", SearchByDestination.as_view()),
    path("stopsautocomplete/", StopsAutocomplete.as_view()),
    path("touristplanner/", TouristPlanner.as_view()),
    path("attractions/", GetTouristAttractions.as_view())
]
