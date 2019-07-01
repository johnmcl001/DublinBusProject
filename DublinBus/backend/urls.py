"""
Create backend urls here
"""

from django.urls import path, include
from rest_framework import routers
from .views import *

# Declare common routes for rest api
ROUTER = routers.DefaultRouter()
ROUTER.register(r"stops", StopsView, "stop")
ROUTER.register(r"routes", RoutesView, "route")
ROUTER.register(r"stoptimes", StopTimesView, "stoptimes")
ROUTER.register(r"trips", TripsView, "trips")

# Specify url patterns within project
urlpatterns = [
    path("", include(ROUTER.urls)),
    path("stop/<str:stopnumber>/<str:time>/<str:date>/", SearchByStop.as_view()),
    path("route/", SearchByRoute.as_view()),
    path("destination/", SearchByDestination.as_view())

]
