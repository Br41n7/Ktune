from django.urls import path
from . import views

app_name = 'events'  # Enables namespacing like 'events:event_list'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    
    path('search/', views.event_search, name='event_search'),
    path('recommendations/', views.event_recommendations, name='event_recommendations'),
    path('reminders/', views.event_reminders, name='event_reminders'),
    path('history/', views.event_history, name='event_history'),
    
    path('<int:event_id>/favorite/add/', views.add_favorite, name='add_favorite'),
    path('<int:event_id>/favorite/remove/', views.remove_favorite, name='remove_favorite'),
    path('create/',views.create_event,name='create_event'),
]
