from django.contrib import admin
from .models import TrainingSite
from .models import Soldier
from .models import Event
from django.contrib.auth.models import Group

# admin.site.register(TrainingSite, TrainingSiteAdmin)
admin.site.register(Soldier)

# Remove Groups
admin.site.unregister(Group)


# admin.site.register(Event)

@admin.register(TrainingSite)
class TrainingSiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    ordering = ('name',)
    search_fields = ('name', 'address')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name', 'site'), 'event_date', 'description', 'manager', 'approved')
    list_display = ('name', 'event_date', 'site')
    list_filter = ('event_date', 'site')
    ordering = ('event_date',)
