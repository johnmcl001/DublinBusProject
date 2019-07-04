"""
Create backend urls here
"""

from django.urls import path, include
from rest_framework import routers
from .views import *


# Specify url patterns within project
urlpatterns = [
    path("stop/", SearchByStop.as_view()),
    path("route/", SearchByRoute.as_view()),
    path("destination/", SearchByDestination.as_view())

]
