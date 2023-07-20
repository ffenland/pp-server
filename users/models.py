from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    # Veil Useless field
    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    # id = uuid string
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
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
    is_owner = models.BooleanField(
        default=False,
    )

    # pharmacist
    license_number = models.CharField(
        max_length=6,
    )
    college = models.CharField(
        max_length=20,
        null=True,
    )
    year_of_admission = models.PositiveSmallIntegerField(
        null=True,
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
    # WorkingSchedule one to many

    # for newbie
    is_incomplete = models.BooleanField(default=True)
