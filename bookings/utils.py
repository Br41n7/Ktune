from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import Booking
import datetime

def send_event_reminders():
    tomorrow = timezone.now() + datetime.timedelta(days=1)
    start = tomorrow.replace(hour=0, minute=0, second=0)
    end = tomorrow.replace(hour=23, minute=59, second=59)

    bookings = Booking.objects.filter(event_date_range=(start, end), reminded=False)

    for booking in bookings:
        subject = f"Reminder: {booking.event.title} is tomorrow!"
        html_message = render_to_string('emails/event_reminder.html', {
            'user': booking.user,
            'event': booking.event,
        })
        email = EmailMessage(subject, html_message, to=[booking.user.email])
        email.content_subtype = 'html'
        email.send()

        booking.reminded = True
        booking.save()
