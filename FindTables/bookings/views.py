from rest_framework import generics, views
from django.shortcuts import render
from rest_framework.response import Response
from datetime import datetime

from bookings.models import BookingPlatform, Restaurant, Table, Reservations, Customer
from bookings.serializers import BookingPlatformSerializer, RestaurantSerializer, TableSerializer, ReservationsCreateSerializer, ReservationsListSerializer


def booking_form_view(request):
    return render(request, "booking_form.html")

class BookiPlatformListAPIView(generics.ListAPIView):
    queryset = BookingPlatform.objects.all()
    serializer_class = BookingPlatformSerializer

class RestaurantListAPIView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class TableListAPIView(generics.ListAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class ReservationListAPIView(generics.ListAPIView):
    queryset = Reservations.objects.all()
    serializer_class = ReservationsListSerializer

   
class ReservationCreateAPIView(views.APIView):
    def post(self, request):
        data = request.data
        customer_data = {
            'name': f"{data.pop('first_name')} {data.pop('last_name')}",
            'phone_number': f"{data.pop('country_code')}-{data.pop('phone')}",
            'email': data.pop('email')
        }

        source = data.pop('source')

        customer_id, created = Customer.objects.get_or_create(**customer_data)
        reservation_platform = BookingPlatform.objects.get(name=source)
        restaurant = Restaurant.objects.first()

        data['reservation_time'] = datetime.strptime(f'{data.pop("reservation_date")} {data.pop("reservation_time")}', "%Y-%m-%d %H:%M")
        data['restaurant'] = restaurant.id
        data['reservation_platform'] = reservation_platform.id
        data['guest'] = customer_id.id

        serializer = ReservationsCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'data':'Your reservation has been successful!'})
        
        return Response({'data':'Issue with your data'})

