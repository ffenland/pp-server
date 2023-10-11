from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe
from .models import User

# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def license_image_display(self, obj):
        return (
            mark_safe(f'<img src="{obj.license_image}" width="100" height="100" />')
            if obj.license_image != "면허증 미첨부"
            else "면허증 미첨부"
        )

    license_image_display.short_description = "License_Image"
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "is_owner",
                    "is_complete",
                    "is_approved",
                )
            },
        ),
        (
            ("Personal info"),
            {
                "fields": (
                    "phone",
                    "naver_id",
                    "kakao_id",
                ),
            },
        ),
        (
            ("약사정보"),
            {
                "fields": (
                    "license_number",
                    "college",
                    "year_of_admission",
                )
            },
        ),
        (
            ("일자리 정보"),
            {"fields": ("address_sido_code", "address_sgg_code", "address_str")},
        ),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            ("Important dates"),
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
                "classes": ("collapse",),
            },
        ),
    )
    list_display = (
        "username",
        "email",
        "license_image_display",
        "is_approved",
    )
    list_filter = ("is_approved",)
