from django.db import models
from django.conf import settings

# Create your models here.


class Record(models.Model):
    class RecordKindChoice(models.TextChoices):
        LIKE = ("like", "좋아요")
        BAD = ("bad", "싫어요")
        FAV = ("fav", "북마크")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    resume = models.ForeignKey(
        "schedules.Resume",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        "posts.post",
        null=True,
        blank=True,
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

    def __str__(self):
        if self.post:
            return f"{self.post.title} {self.kind} by {self.user}"
        elif self.resume:
            return f"{self.resume.user}'s resume {self.kind} by {self.user}"
        elif self.reply:
            return f"{self.reply.user}'s reply {self.kind} by {self.user}"
        else:
            return f"some kind of Record{self.id}"
