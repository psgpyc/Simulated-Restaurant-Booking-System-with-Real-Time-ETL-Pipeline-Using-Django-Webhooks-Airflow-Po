from rest_framework import generics
from bookings.models import BookingPlatform, Restaurant, Table, Reservations
from bookings.serializers import BookingPlatformSerializer, RestaurantSerializer, TableSerializer, ReservationsCreateSerializer, ReservationsListSerializer

class BookiPlatformListAPIView(generics.ListAPIView):
    queryset = BookingPlatform.objects.all()
    serializer_class = BookingPlatformSerializer

class RestaurantListAPIView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class TableListAPIView(generics.ListAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class ReservationCreateAPIView(generics.CreateAPIView):
    queryset = Reservations.objects.all()
    serializer_class = ReservationsCreateSerializer

class ReservationListAPIView(generics.ListAPIView):
    queryset = Reservations.objects.all()
    serializer_class = ReservationsListSerializer

   
