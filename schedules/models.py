from django.conf import settings
from django.db import models
from common.models import CommonPKModel

# Create your models here.


class Day(models.Model):
    date = models.CharField(max_length=9)
    am = models.BooleanField(
        default=True,
    )
    pm = models.BooleanField(
        default=True,
    )

    def __str__(self):
        if self.am and self.pm:
            return f"{self.date} allday"
        elif self.am:
            return f"{self.date} am"
        else:
            return f"{self.date} pm"


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
