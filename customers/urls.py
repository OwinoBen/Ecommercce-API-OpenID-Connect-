from django.urls import path, include
from rest_framework import routers

from .views import CustomerViewSet

app_name = 'customers'

route = routers.SimpleRouter(trailing_slash=False)
route.register('', CustomerViewSet, basename='customers')

urlpatterns = [
    path('', include(route.urls))
]
