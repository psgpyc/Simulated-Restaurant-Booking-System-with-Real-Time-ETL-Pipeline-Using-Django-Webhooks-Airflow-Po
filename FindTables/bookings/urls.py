from django.urls import path
from bookings.views import BookiPlatformListAPIView, RestaurantListAPIView, TableListAPIView, ReservationCreateAPIView, ReservationListAPIView


urlpatterns = [
    path('booking_platform/', BookiPlatformListAPIView.as_view(), name='booking_platform_list_view'),
    path('restaurants/', RestaurantListAPIView.as_view(), name='restaurant_api_list_view'), 
    path('tables/', TableListAPIView.as_view(), name='tables_api_list_view'),
    path('reservations/create', ReservationCreateAPIView.as_view(), name='reservation_api_list_view'),
    path('reservations/list', ReservationListAPIView.as_view(), name='reservation_api_list_view')

    
]
