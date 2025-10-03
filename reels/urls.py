from django.urls import path

from .views import upload_reel, reel_list
app_name='reels'
urlpatterns = [
    path('reels/', reel_list, name='reel_list'),
    path('reels/upload/', upload_reel, name='upload_reel'),
]
