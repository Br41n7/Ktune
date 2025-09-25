from django.urls import path
from . import views

app_name = 'bookings'  # Enables namespaced URLs like 'bookings:book_ticket'

urlpatterns = [
    path('book/<int:event_id>/', views.book_ticket, name='book_ticket'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('history/', views.booking_history, name='booking_history'),

    # Optional: Success & denied pages
    path('success/', views.booking_success, name='booking_success'),
    path('cancelled/', views.booking_cancelled, name='booking_cancelled'),
    path('denied/', views.access_denied, name='access_denied'),
]
