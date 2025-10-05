from django.urls import path
from . import views

app_name='artist'

urlpatterns =[
    path('artist/profile/',views.artist_profile,name='artist_profile'),
    path('artist/edit/',views.edit_artist_profile,name='edit_artist_profile'),
    path('artists/',views.artist_list,name='artist_list'),
    path('artists/<int:artist_id>/',views.artist_detail,name='artist_detail'),
    path('<str:username>/',views.artist_profile_view,name='artist_profile'),
    path('<str:username>/follow/',views.follow_artist,name='follow_artist'),
]
