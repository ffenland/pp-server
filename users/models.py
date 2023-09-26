from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from common.models import CommonPKModel


class User(AbstractUser):
    # Veil Useless field
    first_name = models.CharField(
        max_length=150,
        editable=False,
        null=True,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
        null=True,
    )
    # me information
    # id = uuid string
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    is_complete = models.BooleanField(
        default=False,
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
        unique=True,
    )
    naver_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    kakao_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    avatar = models.URLField(
        null=True,
    )

    # pharmacist
    license_number = models.CharField(
        max_length=6,
        null=True,
    )
    license_img = models.URLField(null=True)
    college = models.CharField(
        max_length=20,
        null=True,
    )
    year_of_admission = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2150)],
        default=1900,
    )

    # for Owner
    is_owner_complete = models.BooleanField(
        default=False,
    )

    # for recruit
    address_sido_code = models.CharField(
        max_length=2,
        null=True,
    )
    address_sgg_code = models.CharField(
        max_length=3,
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
