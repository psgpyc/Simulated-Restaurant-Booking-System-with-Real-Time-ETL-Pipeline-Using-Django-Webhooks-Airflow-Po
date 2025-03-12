from rest_framework import serializers
from bookings.models import BookingPlatform, Restaurant, Table, Customer,Reservations


class BookingPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingPlatform
        fields = ['name']


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'address']


class TableSerializer(serializers.ModelSerializer):
    belongs_to = RestaurantSerializer()

    class Meta:
        model = Table
        fields = '__all__'
        depth = 2

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number']


class ReservationsCreateSerializer(serializers.ModelSerializer):
    reservation_platform = serializers.PrimaryKeyRelatedField(queryset=BookingPlatform.objects.all())
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
    guest = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = Reservations
        fields = ['reservation_platform', 'restaurant', 'guest' ,'size','reservation_time', 'status']
    


class ReservationsListSerializer(serializers.ModelSerializer):
    reservation_platform = BookingPlatformSerializer()
    restaurant = RestaurantSerializer()
    guest = CustomerSerializer()

    class Meta:
        model = Reservations
        fields = ['reservation_platform', 'restaurant', 'guest', 'reservation_time']
        