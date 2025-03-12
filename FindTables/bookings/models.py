from django.db import models


class BookingPlatform(models.Model):
    name = models.CharField(max_length=100, unique=True)
    api_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    class Meta:
        unique_together = ["name", "address"]

    def __str__(self):
        return f"{self.name} at {self.address}"


class Table(models.Model):
    table_number = models.CharField(max_length=10)
    capacity = models.IntegerField()
    belongs_to = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['table_number', 'belongs_to']

    def __str__(self):
        return f"Table {self.table_number}"


class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)

    class Meta:
        unique_together = ['name', 'phone_number']

    def __str__(self):
        return f"{self.name} - {self.phone_number}"



class Reservations(models.Model):
    """Stores restaurant reservation details"""

    reservation_platform = models.ForeignKey(BookingPlatform, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    reservation_time = models.DateTimeField()
    guest = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    size = models.IntegerField()
    status = models.CharField(
        max_length=20, 
        choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled'), ('no_show', 'No Show')], 
        default='confirmed'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Reservations'
    
    def __str__(self):
        return f"Reservation at {self.reservation_time}"


class WebhookEvent(models.Model):
    """Simulates real-time updates from booking platforms."""
    reservation = models.ForeignKey(Reservations, on_delete=models.CASCADE, related_name='webhook_events')
    event_type = models.CharField(
        max_length=50, 
        choices=[('created', 'Created'), ('updated', 'Updated'), ('cancelled', 'Cancelled')]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data = models.JSONField()
    
    def __str__(self):
        return f"{self.event_type} - {self.reservation}"