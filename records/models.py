from django.db import models
from django.conf import settings
from schedules.models import Recruit, Resume
# Create your models here.


class Record(models.Model):
    class RecordKindChoice(models.TextChoices):
        LIKE = ("like", "좋아요")
        BAD = ("bad", "싫어요")
        FAV = ("fav", "북마크")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    kind = models.CharField(
        max_length=4,
        choices=RecordKindChoice.choices,
    )
    resume = models.
