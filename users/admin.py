from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "is_owner",
                    "is_active",
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
                    "license_img",
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
            {
                "fields": (
                    "address_sgg_code",
                    "address_sido",
                    "address_sgg",
                )
            },
        ),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
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
    list_display = ("username", "email")
