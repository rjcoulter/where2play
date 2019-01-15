from django.contrib import admin

from .models import Facility
from .models import Court
from .models import Time_Slot
from .models import Our_User
from .models import Reserved_Time_Slot

# Register your models here.


class CourtInLine(admin.TabularInline):
    model = Court

class Time_SlotInLine(admin.TabularInline):
    model = Time_Slot

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['F_Name', 'F_Type', 'Location']
    inlines = [CourtInLine, ]

@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ['C_Name', 'C_Type', 'current_count']
    inlines = [Time_SlotInLine, ]

@admin.register(Time_Slot)
class Time_SlotAdmin(admin.ModelAdmin):
    list_display = ['court', 'date', 'time', 'available', 'signup_count']

@admin.register(Our_User)
class Our_UserAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type']

@admin.register(Reserved_Time_Slot)
class Reserved_Time_Slot(admin.ModelAdmin):
    list_display = ['person', 'facility', 'court', 'date', 'time']
