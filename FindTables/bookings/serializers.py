from rest_framework import serializers
from bookings.models import BookingPlatform, Restaurant, Table, Customer,Reservations, Experience, ReservationTags


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
    source = serializers.PrimaryKeyRelatedField(queryset=BookingPlatform.objects.all())
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
    guest = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    experience = serializers.PrimaryKeyRelatedField(queryset=Experience.objects.all())
    tags = serializers.PrimaryKeyRelatedField(queryset=ReservationTags.objects.all(), many=True)

    class Meta:
        model = Reservations
        fields = ['source', 'has_tags' ,'restaurant', 'experience', 'tags' , 'guest' ,'size','reservation_time', 'status', 'visit_notes']
    


class ReservationsListSerializer(serializers.ModelSerializer):
    source = BookingPlatformSerializer()
    restaurant = RestaurantSerializer()
    guest = CustomerSerializer()

    class Meta:
        model = Reservations
        fields = ['source', 'restaurant', 'guest', 'reservation_time']
        
# beyond creation


class ReservationListDetailsSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields = '__all__'
        depth = 1

