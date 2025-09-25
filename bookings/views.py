from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Booking, BookingHistory
from events.models import Event, EventTicket

@login_required
def book_ticket(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    ticket = EventTicket.objects.filter(event=event).first()

    if not ticket or ticket.quantity <= 0:
        return render(request, 'bookings/sold_out.html', {'event': event})

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            if booking.quantity > ticket.quantity:
                form.add_error('quantity', 'Not enough tickets available.')
            else:
                booking.event = event
                booking.user = request.user
                booking.total_cost = ticket.price * booking.quantity
                booking.save()

                # Update ticket quantity
                ticket.quantity -= booking.quantity
                ticket.save()

                # Save booking history
                BookingHistory.objects.create(
                    user=request.user,
                    booking=booking,
                    status='booked'
                )

                return redirect('booking_success')  # Ensure this URL exists
    else:
        form = BookingForm()

    return render(request, 'bookings/book_ticket.html', {'form': form, 'event': event})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.user != booking.user:
        return redirect('access_denied')

    # Refund ticket quantity
    ticket = EventTicket.objects.filter(event=booking.event).first()
    if ticket:
        ticket.quantity += booking.quantity
        ticket.save()

    BookingHistory.objects.create(
        user=request.user,
        booking=booking,
        status='cancelled'
    )

    booking.delete()
    return redirect('booking_cancelled')  # Ensure this URL exists


@login_required
def booking_history(request):
    history = BookingHistory.objects.filter(user=request.user).order_by('-booked_at')
    return render(request, 'accounts/booking_history.html', {'booking_history': history})

def booking_success(request):
    return render(request, 'bookings/booking_success.html')

def booking_cancelled(request):
    return render(request, 'bookings/booking_cancelled.html')

def access_denied(request):
    return render(request, 'bookings/access_denied.html')


