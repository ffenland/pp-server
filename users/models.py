from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from common.models import CommonPKModel
from common.utils import cf_id_to_url


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
    is_approved = models.BooleanField(
        default=False,
    )
    is_complete = models.BooleanField(
        default=False,
    )
    is_owner = models.BooleanField(
        default=False,
    )
    # Account
    nickname = models.CharField(
        max_length=8,
    )
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
    avatar = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    # pharmacist
    license_number = models.CharField(
        unique=True,
        max_length=6,
        null=True,
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
    address_str = models.CharField(
        max_length=20,
        null=True,
    )

    @property
    def license_image(self):
        return (
            cf_id_to_url(
                self.photo_set.filter(description="License Image").first().cf_id,
                "avatar",
            )
            if self.photo_set.filter(description="License Image").first()
            else "면허증 미첨부"
        )


class UserStatus(CommonPKModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    username_modify_limit = models.PositiveIntegerField(default=3)


class UserSchool(CommonPKModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hakbun_modify_limit = models.PositiveIntegerField(default=1)
    college = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )
    hakbun = models.IntegerField
    year_of_admission = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2150)],
        default=1900,
    )
