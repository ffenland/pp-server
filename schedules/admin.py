from django.contrib import admin
from .models import Schedule, Day, Resume

# Register your models here.


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ("date", "am", "pm", "is_regular")


admin.site.register(Schedule)


class ResumeAdmin(admin.ModelAdmin):
    readonly_fields = (
        "address_str",
        "address_sido_code",
        "address_sgg_code",
    )


admin.site.register(Resume, ResumeAdmin)
