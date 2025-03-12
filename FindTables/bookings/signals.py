from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
import json
from bookings.models import Reservations, WebhookEvent


PIPELINE_URL = "http://localhost:6000/webhook" 

@receiver(post_save, sender=Reservations)
def send_reservation_webhook(sender, instance, created, **kwargs):
    """
        Sends a webhook event whenever a new reservation is created or updated
    """
    event_type = "created" if created else "updated"

    payload = {
        "reservation_id": instance.id,
        "guest": instance.guest.name,
        "size": instance.size,
        "reservation_time": instance.reservation_time.isoformat(),
        "status": instance.status,
        "platform": instance.reservation_platform.name if instance.reservation_platform else 'Walk ins',

    }

    # Store webhook event in the database
    WebhookEvent.objects.create(
        reservation=instance,
        event_type=event_type,
        data=payload,
    )

    # Send webhook request to the pipeline
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(PIPELINE_URL, data=json.dumps(payload), headers=headers)
        print(response.status_code)
        response.raise_for_status()  # Raise exception if request fails
    except requests.RequestException as e:
        print(f"Webhook Error: {e}")  # Log the error