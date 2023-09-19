from django.urls import path, include
from rest_framework import routers

from accounts.views import AuthViewSet, TokenObtainView

app_name = 'accounts'

route = routers.SimpleRouter(trailing_slash=False)
route.register('auth', AuthViewSet, basename='auth')
route.register('token', TokenObtainView, basename='token')

urlpatterns = [
    path('', include(route.urls)),
]
