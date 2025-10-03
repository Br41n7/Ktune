import requests
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from bookings.models import Booking
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def initialize_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "email": request.user.email,
        "amount": int(booking.total_cost * 100),  # Convert to kobo
        "callback_url": request.build_absolute_uri('/payments/verify/'),
        "metadata": {
            "booking_id": booking.id,
            "user_id": request.user.id,
        }
    }

    response = requests.post("https://api.paystack.co/transaction/initialize", json=data, headers=headers)
    result = response.json()

    if result.get('status'):
        return redirect(result['data']['authorization_url'])
    else:
        return redirect('booking_cancelled')


def verify_payment(request):
    ref = request.GET.get('reference')
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }

    response = requests.get(f"https://api.paystack.co/transaction/verify/{ref}", headers=headers)
    result = response.json()

    if result['data']['status'] == 'success':
        metadata = result['data']['metadata']
        booking_id = metadata.get('booking_id')

        from bookings.models import Booking, BookingHistory
        booking = Booking.objects.get(id=booking_id)

        booking.status = 'booked'
        booking.save()

        # Decrease ticket quantity
        ticket = EventTicket.objects.filter(event=booking.event).first()
        if ticket:
            ticket.quantity -= booking.quantity
            ticket.save()

        BookingHistory.objects.create(
            user=booking.user,
            booking=booking,
            status='booked'
        )

        return redirect('booking_success')

    return redirect('booking_cancelled')
