from django.contrib import admin
from .models import Schedule, Day

# Register your models here.


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ("date", "am", "pm", "is_regular")


admin.site.register(Schedule)
