from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
import requests
import json
from django.db import transaction
from django.core.serializers.json import DjangoJSONEncoder


from bookings.models import Reservations, WebhookEvent, Orders
import time


PIPELINE_URL = "http://localhost:8080/api/v1/dags/etl_pipeline_dag/dagRuns" 
headers = {"Content-Type": "application/json"}
auth = ("admin", "nepal123")


def send_webhook(instance, created):
 
    data = {
        "conf": {
        "reservation_id": instance.id,
        "guest": {
             "customer_id": instance.guest.id,
             "customer_name": instance.guest.name,
             "customer_email": instance.guest.email, 
             "customer_phone": instance.guest.phone_number,
             "joined_date": instance.guest.created_at.isoformat()
        }, 
        "size": instance.size,
        "reservation_time": instance.reservation_time.isoformat(),
        "experience": instance.experience.name, 
        "payment_mode": instance.payment_mode, 
        "status": instance.status,
        "tags":[tag.name for tag in instance.tags.all()],
        "visit_notes": instance.visit_notes,
        "created_at": instance.created_at.isoformat(), 
        "updated_at": instance.updated_at.isoformat(), 
        "source": instance.source.name if instance.source else 'Walk ins',

    }
    }

    event_type = "created" if created else "updated"


    # # Store webhook event in the database
    WebhookEvent.objects.create(
        reservation=instance,
        event_type=event_type,
        data=data,
    )

    # # Send webhook request to the pipeline
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(PIPELINE_URL, json=data, headers=headers, auth=auth)
        response.raise_for_status()  # Raise exception if request fails
    except requests.RequestException as e:
        print(f"Webhook Error: {e}")  # Log the error



@receiver(post_save, sender=Reservations)
def send_reservation_webhook(sender, instance, created, **kwargs):
    """
        Sends a webhook event whenever a new reservation is created or updated
    """
    if created:
        if instance.has_tags:
            print('post_save, skipping...')
        else:
            print('post_save Invoked, processing....')
            transaction.on_commit(lambda: send_webhook(instance=instance, created=created))
    else:
        #not handeling update for now
        pass


@receiver(m2m_changed, sender=Reservations.tags.through)
def tags_update_signal(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        print('m2m Invoked, processing...')
        transaction.on_commit(lambda: send_webhook(instance=instance, created=False))
        
    

# Order Sending Signal
    
@receiver(post_save, sender=Orders)
def send_orders_webhook(sender, instance, created, **kwargs):
    """
        Sends a webhook event when a new order is created.
    """
    PIPELINE_URL = "http://localhost:8080/api/v1/dags/order_pipeline_dag/dagRuns"
    if not created:
        order_details = {
            'conf': {
            'order_id': instance.id,
            'customer_id': instance.customer_id.id,
            'order_items': [
                
                {"menu_item": obj.menu_item.id,  "quantity":obj.quantity}  for obj in instance.orderitem_set.all()
                
            ],
            'total_price': json.dumps(instance.total_price, cls=DjangoJSONEncoder),
            'ordered_on': instance.created_at.isoformat(),
            'updated_on': instance.updated_at.isoformat(),
            'order_status': instance.is_completed
            }
        }

        # # Send webhook request to the pipeline
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(PIPELINE_URL, json=order_details, headers=headers, auth=auth)
            response.raise_for_status()  # Raise exception if request fails
        except requests.RequestException as e:
            print(f"Webhook Error: {e}")  # Log the error    


