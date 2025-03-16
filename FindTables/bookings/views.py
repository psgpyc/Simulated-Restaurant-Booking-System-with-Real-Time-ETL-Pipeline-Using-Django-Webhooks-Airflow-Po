from rest_framework import generics, views
from django.http import Http404
from django.shortcuts import render
from rest_framework.response import Response
from datetime import datetime

from bookings.models import BookingPlatform, Restaurant, Table, Reservations, Customer, ReservationTags, Experience, Orders, OrderItem,MenuItem
from bookings.serializers import (
    BookingPlatformSerializer, RestaurantSerializer, TableSerializer, 
    ReservationsCreateSerializer, ReservationsListSerializer, ReservationListDetailsSerialiser,
    OrdersListSerializer)



def booking_form_view(request):
    return render(request, "booking_form.html")


def place_order_view(request):
    return render(request, "place_order.html")

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


class OrdersListApiView(generics.ListAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersListSerializer

class OrdersCreateApiView(views.APIView):
    def get_object(self, pk):
        """
            Returns a customer id associated with the order
        """
        try:
            return Customer.objects.get(pk=pk)
        except Reservations.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):

        # validate that is_completed key exists in the request data

        if 'is_completed' not in request.data:
            return Response({'error': "Miss 'is_completed' in request data"}, status=400)
        
        if "order_items" not in request.data:
                return Response({'error': 'Missing "order_items" in request data'}, status=400)
            

        cus_id = self.get_object(pk=pk)

        ord_obj, created = Orders.objects.get_or_create(customer_id=cus_id, is_completed=False)

        
        menu_items = request.data.pop("order_items")

        if created:

            # Ensure "order_items" is a non-empty list.
            if not isinstance(menu_items, list) or not menu_items:
                return Response({'error': '"order_items" must be a non-empty list'}, status=400)
                
            through_obj = [
                OrderItem(
                    order=ord_obj,
                    menu_item=MenuItem.objects.get(id=item['menu_item']),
                    quantity=item['quantity']
                )
                for item in menu_items

            ]
            OrderItem.objects.bulk_create(through_obj)

            try:
                ord_obj.calculate_total_price()
            except Exception as e:
                return Response({'error': f'Error calculating total price: {str(e)}'}, status=500)
            
            return Response({'data':'Your order has been created'})



        if not created: 
            if request.data.get('is_completed') is True:
                # order is updated but has not been completed
                ord_obj.is_completed = request.data['is_completed']
                try:
                    ord_obj.save()
                except Exception as e:
                    return Response({'error': f'error updating order {str(e)}'}, status=500)
                
                return Response({'data':'Your order has been completed'})

            if request.data['is_completed'] is False:
                for each_menu_item in menu_items:
                    try:
                        menu_item_obj = MenuItem.objects.get(id=each_menu_item['menu_item'])
                    except Exception as e:
                        return Response({'error': f'error fetching menu item {str(e)}'})
                    order_item_obj, created = OrderItem.objects.get_or_create(order=ord_obj, menu_item=menu_item_obj)
                    if not created:
                        order_item_obj.quantity += each_menu_item['quantity']
                        try:
                            order_item_obj.save()
                        except Exception as e:
                            return Response({'error': f'error updating order quantity {str(e)}'})
                    if created:
                        order_item_obj.quantity = each_menu_item['quantity']
                        try:
                            order_item_obj.save()
                        except Exception as e:
                            return Response({'error': f'error updating order quantity {str(e)}'})
                        
                ord_obj.calculate_total_price()

       

                return Response({'data':'Your order has been updated'})