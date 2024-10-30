from django.urls import path
from .views import ReceiveCoordinates

urlpatterns = [
    path('send-coordinates/', ReceiveCoordinates.as_view(), name='send-coordinates'),
]
