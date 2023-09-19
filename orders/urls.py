from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import OrderView

app_name = 'orders'

router = SimpleRouter(trailing_slash=False)
router.register('', OrderView, basename='orders')
urlpatterns = [
    path('', include(router.urls))
]
