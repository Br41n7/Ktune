from django.core.mail import send_mail,EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BookingForm
from .models import Booking, BookingHistory
from events.models import Event, EventTicket


@login_required
def book_ticket(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    ticket = EventTicket.objects.filter(event=event).first()
    booking=Booking.objects.get(user_email=email,id=booking_id)
    if not ticket or ticket.quantity <= 0:
        messages.error(request, "Sorry, this event is sold out.")
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



        if result['data']['status']=='success':
                booking.status=booked
                booking.save()

        send_mail(
            subject='Booking Confirmation',
            message=f'Thank you {request.user.username}, your booking for "{event.title}" has been confirmed.',
            from_mail=None,
            recipient_list=[request.user.email],
            fail_silently=True

        )                        


                # Reduce available tickets
        ticket.quantity -= booking.quantity
        ticket.save()

                # Log booking history
        BookingHistory.objects.create(
            user=request.user,
            booking=booking,
            status='booked'
        )

        return redirect('initialize_payment',booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'bookings/book_ticket.html', {
        'form': form,
        'event': event,
        'ticket': ticket
    })


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

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
    messages.success(request, "Booking cancelled.")
    return redirect('booking_cancelled')


@login_required
def booking_history(request):
    history = BookingHistory.objects.filter(user=request.user).select_related('booking', 'booking__event').order_by('-booked_at')
    if status_filter == 'booked':
        history=history.filter(status='booked')
    elif status_filter == 'cancelled':
        history=history.filter(status='cancelled')

    return render(request, 'accounts/booking_history.html', {'booking_history': history})


def booking_success(request):
    return render(request, 'bookings/booking_success.html')


def booking_cancelled(request):
    return render(request, 'bookings/booking_cancelled.html')


def access_denied(request):
    return render(request, 'bookings/access_denied.html')
