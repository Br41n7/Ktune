from django.contrib import admin
from .models import Event,EventTicket
# Register your models here.
#
admin.site.register(EventTicket)
admin.site.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display=['title','created','host','artist','price']
    list_filter=['created']
