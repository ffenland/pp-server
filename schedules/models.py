from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator
from common.models import CommonPKModel, CommonModel

# Create your models here.


class Day(models.Model):
    date_validator = RegexValidator(
        regex=r"^(?:\d{10}|mon|tue|wed|thu|fri|sat|sun)$",
        message="Date should be a valid 8-digit number or a day of the week.",
    )

    date = models.CharField(
        max_length=10,
        validators=[date_validator],
    )
    am = models.BooleanField(
        default=True,
    )
    pm = models.BooleanField(
        default=True,
    )

    class Meta:
        unique_together = ["date", "am", "pm"]

    def __str__(self):
        if self.am and self.pm:
            return f"{self.date} allday"
        elif self.am:
            return f"{self.date} am"
        else:
            return f"{self.date} pm"

    def is_regular(self):
        return len(self.date) == 3


class Schedule(CommonPKModel):
    days = models.ManyToManyField(
        "schedules.Day",
    )


class Resume(CommonPKModel, CommonModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    schedule = models.ForeignKey(
        "schedules.Schedule",
        null=True,
        on_delete=models.SET_NULL,
    )
    description = models.TextField()
    is_recruit = models.BooleanField(default=False)
    address_sido_code = models.CharField(
        max_length=2,
    )
    address_sgg_code = models.CharField(
        max_length=3,
    )
    address2_sido_code = models.CharField(
        max_length=2,
        null=True,
    )
    address2_sgg_code = models.CharField(
        max_length=3,
        null=True,
    )
