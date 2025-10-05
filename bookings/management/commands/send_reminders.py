bookings/management/commands/send_reminders.py
from django.core.management.base import BaseCommand
from bookings.utils import send_event_reminders

class Command(BaseCommand):
    help = 'Send event reminders 24 hours before the event'

    def handle(self, *args, **kwargs):
        send_event_reminders()
        self.stdout.write(self.style.SUCCESS('Reminders sent.'))
