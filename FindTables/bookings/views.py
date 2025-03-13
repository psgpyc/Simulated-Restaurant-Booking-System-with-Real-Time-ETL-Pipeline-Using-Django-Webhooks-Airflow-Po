from rest_framework import generics, views
from django.http import Http404
from django.shortcuts import render
from rest_framework.response import Response
from datetime import datetime

from bookings.models import BookingPlatform, Restaurant, Table, Reservations, Customer, ReservationTags, Experience
from bookings.serializers import BookingPlatformSerializer, RestaurantSerializer, TableSerializer, ReservationsCreateSerializer, ReservationsListSerializer, ReservationListDetailsSerialiser


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
    queryset = Reservations.objects.all().order_by('-created_at')
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
        data['source'] = reservation_platform.id
        data['guest'] = customer_id.id
        data['experience'] = Experience.objects.get(name=data.pop('experience')).id
        data['tags'] = [ReservationTags.objects.get(name=each).id for each in data.pop('tags')]
        data['has_tags'] = True if len(data['tags']) > 0 else False




        serializer = ReservationsCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'data':'Your reservation has been successful!'})
        
        return Response({'data':'Issue with your data'})
    

class ReservationDetailAPIView(views.APIView):
    """
        Retrieve, update a reservation
    """
    def get_object(self, pk):
        try:
            return Reservations.objects.get(pk=pk)
        except Reservations.DoesNotExist:
            raise Http404
        
    def get(self, request,  pk, format=None):
        reservation_instance = self.get_object(pk=pk)
        serializer = ReservationListDetailsSerialiser(reservation_instance)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        reservation_instance = self.get_object(pk=pk)
        data = request.data.copy()
        # self.generate_valid(data=request.data)
        data['source'] =  BookingPlatform.objects.get(**data['source']).id
        data['guest'] = Customer.objects.get(**data['guest']).id
        data['restaurant'] = Restaurant.objects.get(**data['restaurant']).id
        data['experience'] = Experience.objects.get(**data['experience']).id
        data['tags'] = [ReservationTags.objects.get(**each).id for each in data.pop('tags')]

    
        serializer = ReservationsCreateSerializer(reservation_instance, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'data': serializer.data})
        
        return  Response({'data': 'error'})
