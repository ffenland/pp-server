from django.db import models
from django.conf import settings


class RecordKindChoice(models.TextChoices):
    LIKE = ("like", "좋아요")
    BAD = ("bad", "싫어요")
    FAV = ("fav", "북마크")


# Create your models here.
class ResumeLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    resume = models.ForeignKey(
        "schedules.Resume",
        on_delete=models.CASCADE,
    )


class PostRecord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    kind = models.CharField(
        max_length=4,
        choices=RecordKindChoice.choices,
    )
    post = models.ForeignKey(
        "posts.post",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )


class ReplyRecord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    reply = models.ForeignKey(
        "posts.reply",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    kind = models.CharField(
        max_length=4,
        choices=RecordKindChoice.choices,
    )
