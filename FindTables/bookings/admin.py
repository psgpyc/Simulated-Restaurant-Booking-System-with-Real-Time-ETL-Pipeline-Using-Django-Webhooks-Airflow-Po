from django.contrib import admin
from  bookings.models import BookingPlatform, Restaurant, Reservations, Table, Customer,WebhookEvent, ReservationTags, Experience, MenuItem, Orders, OrderItem

admin.site.register(BookingPlatform)
admin.site.register(Restaurant)
admin.site.register(Table)
admin.site.register(Reservations)
admin.site.register(Customer)
admin.site.register(ReservationTags)
admin.site.register(Experience)
admin.site.register(WebhookEvent)

admin.site.register(MenuItem)
admin.site.register(Orders)
admin.site.register(OrderItem)