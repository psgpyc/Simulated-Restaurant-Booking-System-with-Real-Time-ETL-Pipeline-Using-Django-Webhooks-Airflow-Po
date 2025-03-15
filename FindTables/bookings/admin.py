from django.contrib import admin
from  bookings.models import BookingPlatform, Restaurant, Reservations, Table, Customer,WebhookEvent, ReservationTags, Experience, MenuItem, Orders, OrderItem

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number','email' ,'created_at')  # add any other fields you want to display


admin.site.register(BookingPlatform)
admin.site.register(Restaurant)
admin.site.register(Table)
admin.site.register(Reservations)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(ReservationTags)
admin.site.register(Experience)
admin.site.register(WebhookEvent)

admin.site.register(MenuItem)
admin.site.register(Orders)
admin.site.register(OrderItem)