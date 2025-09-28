from django.db import models
from django.utils import timezone
from accounts.models import User


class Artist(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='artist_images/', blank=True, null=True)

    def _str_(self):
        return self.name

class Venue(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()

    def _str_(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def _str_(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now().date() > self.date

    def _str_(self):
        return self.name


TICKET_TYPE_CHOICES = (
    ('Regular', 'Regular'),
    ('VIP', 'VIP'),
    ('VVIP', 'VVIP'),
)

class EventTicket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.CharField(max_length=50, choices=TICKET_TYPE_CHOICES, default='Regular')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def _str_(self):
        return f"{self.event.name} - {self.ticket_type} - ₦{self.price}"

    def is_sold_out(self):
        return self.quantity <= 0


class Review(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    review = models.TextField(blank=True, null=True)

class Favorite(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

class EventHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    interacted_at = models.DateTimeField(auto_now_add=True)
    interaction_type = models.CharField(max_length=255)  # e.g. 'attended', 'booked'


class TicketQR(models.Model):
    ticket = models.OneToOneField(EventTicket, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)

    def _str_(self):
        return f"QR for {self.ticket}"

