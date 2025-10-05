from django.contrib import admin
from django.utils.ipv6 import clean_ipv6_address
from .models import Event
# Register your models here.
#

admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display=['name','created']
    list_filter=['created']
