"""
Create backend urls here
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views

# Declare common routes for rest api
router = routers.DefaultRouter()
router.register(r"stop", views.StopView, "stop")
router.register(r"route", views.RouteView, "route")
router.register(r"destination", views.DestinationView, "destination")

# Specify url patterns within project
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls))
]
