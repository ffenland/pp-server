import uuid
from django.db import models
from django.conf import settings
from common.models import CommonModel, CommonPKModel

# Create your models here.


class Pharmacy(CommonModel, CommonPKModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    title = models.CharField(
        max_length=20,
    )
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    reg_number = models.CharField(
        null=True,
        blank=True,
        max_length=10,
    )
    address_road = models.CharField(
        max_length=30,
    )
    address_detail = models.CharField(
        max_length=30,
    )
    address_sgg_code = models.CharField(
        max_length=5,
    )
    address_sido = models.CharField(
        max_length=10,
    )
    address_sgg = models.CharField(
        max_length=10,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Pharmacies"
