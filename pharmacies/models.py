from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings
from common.models import CommonModel, CommonPKModel

# Create your models here.


class Pharmacy(CommonModel, CommonPKModel):
    title = models.CharField(
        max_length=20,
    )
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pharmacy",
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


class Account(CommonPKModel):
    class AccountNames(models.TextChoices):
        CASH = ("cash", "현금매출")
        CARD = ("card", "카드매출")
        PREPARE = ("prepare", "조제료")
        INCOME = ("income", "입금액")

    name = models.TextField(choices=AccountNames.choices)
    ammount = models.PositiveIntegerField()
    date = models.DateField()
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)

    def __str__(self):
        # Extract weekday, month, day, and year from the date field

        month = self.date.month
        day = self.date.day
        year = self.date.year
        date_str = f"{year}/{month}/{day}"
        return f"{date_str} : {self.name} : {self.ammount} : {self.pharmacy}"
