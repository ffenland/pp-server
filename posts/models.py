from django.db import models
from django.conf import settings
from common.models import CommonModel

# Create your models here.


class Post(CommonModel):
    class PostKindChoices(models.TextChoices):
        QUE = ("question", "질문")
        LIFE = ("life", "일상")
        INFO = ("info", "정보")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=30,
    )
    kind = models.CharField(
        max_length=8,
        choices=PostKindChoices.choices,
    )
    article = models.TextField()

    def __str__(self):
        return self.title


class Reply(CommonModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    article = models.CharField(
        max_length=150,
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reply = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="second_reply",
    )

    def __str__(self):
        return self.article
