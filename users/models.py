from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from common.models import CommonPKModel


class User(AbstractUser, CommonPKModel):
    # Veil Useless field
    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    # me information
    # id = uuid string
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    is_active = models.BooleanField(
        "active",
        default=False,
        help_text=(
            "유저가 프로필 설정을 한번이라도 완료 해야 active 상태가 됩니다.",
            "Unselect this instead of deleting accounts.",
        ),
    )
    is_owner = models.BooleanField(
        default=False,
    )
    # Account
    email = models.EmailField(
        unique=True,
    )
    phone = models.CharField(
        max_length=11,
        null=True,
        blank=True,
    )
    naver_id = models.CharField(
        max_length=10,
        null=True,
        blank=True,
    )
    kakao_id = models.CharField(
        max_length=10,
        null=True,
        blank=True,
    )

    # pharmacist
    license_number = models.CharField(
        max_length=6,
    )
    license_img = models.URLField(null=True)
    college = models.CharField(
        max_length=20,
        null=True,
    )
    year_of_admission = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2050)],
        default=1900,
    )

    # for Owner

    # for recruit
    address_sgg_code = models.CharField(
        max_length=5,
        null=True,
    )
    address_sido = models.CharField(
        max_length=10,
        null=True,
    )
    address_sgg = models.CharField(
        max_length=10,
        null=True,
    )
