from django.db.models.fields import return_None
from django.http.response import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Event, Favorite, EventHistory,Category
from .forms import EventForm, EventSearchForm  # Make sure this exists

@login_required
def create_event(request):
    if not request.user.is_host:
        return HttpResponseForbidden("You are not authorize to create events")
    if request.method=='POST':
        form=EventForm(request.POST,request.FILES)
        if form.is_valid():
            event=form.save(commit=False)
            event.host=request.user
            event.save()
            return redirect('event_detail',pk=event.pk)
    else:
        form=EventForm()
    return render(request,'events/create_event.html',{'form':form})



def event_list(request):
    events = Event.objects.all().order_by('date')
    categories=Category.objects.all()
    artist = request.GET.get('artist')
    venue = request.GET.get('venue')
    date = request.GET.get('date')

    if artist:
        events = events.filter(artist__id=artist)
    if venue:
        events = events.filter(venue__id=venue)
    if date:
        events = events.filter(date=date)

    paginator = Paginator(events, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'events/event_list.html', {'page_obj': page_obj})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})


@login_required
def event_recommendations(request):
    user_interests = request.user.interests.all()  # Ensure `interests` field exists
    recommended_events = Event.objects.filter(category__in=user_interests)
    return render(request, 'events/recommended_events.html', {'events': recommended_events})


def event_reminders(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now())
    for event in upcoming_events:
        # TODO: Implement actual reminder logic (e.g., email, push notifications)
        pass
    return redirect('events:event_list')


def event_search(request):
    if request.method == "GET":
        form = EventSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            events = Event.objects.filter(
                name__icontains=query
            ) | Event.objects.filter(
                artist_name_icontains=query
            ) | Event.objects.filter(
                venue_name_icontains=query
            )
            return render(request, 'events/search_results.html', {'events': events})
    else:
        form = EventSearchForm()
    return render(request, 'events/search_form.html', {'form': form})


@login_required
def add_favorite(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    Favorite.objects.get_or_create(event=event, user=request.user)
    return redirect('events:event_detail', pk=event_id)


@login_required
def remove_favorite(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    Favorite.objects.filter(event=event, user=request.user).delete()
    return redirect('events:event_detail', pk=event_id)


@login_required
def event_history(request):
    history = EventHistory.objects.filter(user=request.user).order_by('-interacted_at')
    return render(request, 'accounts/event_history.html', {'event_history': history})
