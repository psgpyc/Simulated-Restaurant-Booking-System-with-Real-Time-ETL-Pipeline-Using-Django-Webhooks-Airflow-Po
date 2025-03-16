from django.db import models
from django.utils import timezone


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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['table_number', 'belongs_to']

    def __str__(self):
        return f"Table {self.table_number}"


class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['name', 'phone_number']

    def __str__(self):
        return f"{self.name} - {self.phone_number}"

class ReservationTags(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Experience(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Reservations(models.Model):
    """Stores restaurant reservation details"""

    source = models.ForeignKey(BookingPlatform, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    reservation_time = models.DateTimeField()
    experience = models.ForeignKey(Experience, on_delete=models.SET_NULL, null=True, blank=True)
    guest = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    size = models.IntegerField()
    status = models.CharField(
        max_length=20, 
        choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled'), ('no_show', 'No Show')], 
        default='confirmed'
    )
    payment_mode = models.CharField(
        max_length=20, 
        choices=[('on site', 'On Site'), ('card hold', 'Credit Card Hold'), ('pre payment', 'Pre Payment')], 
        default='on site'
    )
    tags = models.ManyToManyField(ReservationTags)
    has_tags = models.BooleanField(default=False)
    visit_notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
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
    


class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    course = models.CharField(
        max_length=50, 
        choices=[('started', 'Starter'),('mains', 'Main Course'),('dessert', 'Dessert'), ('sides', 'Sides')]
    )
    is_available = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.id}/{self.name}-{self.price}"
    

    
class Orders(models.Model):
    menu_items = models.ManyToManyField(MenuItem, through='OrderItem')
    customer_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_completed = models.BooleanField(default=False)


    def calculate_total_price(self):
        total = 0
        for order_item in self.orderitem_set.select_related('menu_item').all():
            total += order_item.menu_item.price * order_item.quantity
        self.total_price = total
        self.save(update_fields=['total_price'])



    def __str__(self):
        return f"Order {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    class Meta:
        ordering = ['-updated_at']



class OrderItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, )
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the OrderItem first
        self.order.calculate_total_price() 


    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"
