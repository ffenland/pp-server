from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator
from common.models import CommonPKModel

# Create your models here.


class Day(models.Model):
    date_validator = RegexValidator(
        regex=r"^(?:\d{8}|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)$",
        message="Date should be a valid 8-digit number or a day of the week.",
    )

    date = models.CharField(
        max_length=9,
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
        return self.date.endswith("day")


class Schedule(CommonPKModel):
    days = models.ManyToManyField(
        "schedules.Day",
    )

    def __str__(self):
        return f"{self.user.username}'s schedule"


class Resume(CommonPKModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    schedule = models.ManyToManyField(
        "schedules.Schedule",
    )
    description = models.TextField()


class Recruit(CommonPKModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    schedule = models.ManyToManyField(
        "schedules.Schedule",
    )
    description = models.TextField()
