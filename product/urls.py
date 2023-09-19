from django.urls import path, include
from rest_framework import routers
from .views import ProductViewSet

app_name = 'products'

route = routers.SimpleRouter(trailing_slash=False)
route.register('', ProductViewSet, basename='products')
urlpatterns = [
    path('', include(route.urls))
]
