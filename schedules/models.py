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
    is_active = models.BooleanField(default=True)
    address_sido_code = models.CharField(
        max_length=2,
    )
    address_sgg_code = models.CharField(
        max_length=3,
    )
    address_str = models.CharField(
        max_length=20,
    )

    @property
    def is_regular(self):
        # Schedule에 연결된 Day 중 첫 번째 Day의 date 필드의 길이가 3이면 True, 그렇지 않으면 False 반환
        first_day = self.schedule.days.first()
        return len(first_day.date) == 3

    @property
    def address_str(self):
        return self.user.address_str

    @property
    def address_sido_code(self):
        return self.user.address_sido_code

    @property
    def address_sgg_code(self):
        return self.user.address_sgg_code


class SurveyAnswer(models.Model):
    answer = models.CharField(max_length=10)


class SurveyQuestion(models.Model):
    question = models.CharField(max_length=100)
    is_recruit = models.BooleanField(default=False)
    answer_choice = models.ManyToManyField(
        SurveyAnswer,
    )


class SurveyResult(CommonPKModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        SurveyQuestion,
        on_delete=models.SET_NULL,
        null=True,
    )
    answer = models.ForeignKey(
        SurveyAnswer,
        null=True,
        on_delete=models.SET_NULL,
    )
    answer_detail = models.CharField(
        max_length=100,
        null=True,
    )
