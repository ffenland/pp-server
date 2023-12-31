from django.db import models
from django.conf import settings
from common.models import CommonModel, CommonPKModel

# Create your models here.


class Post(CommonModel, CommonPKModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=30,
    )
    kind = models.CharField(
        max_length=8,
    )
    article = models.TextField()
    view_count = models.PositiveIntegerField(
        default=0,
        editable=False,
    )

    def __str__(self):
        return f"{self.kind}/{self.title} by {self.user}"


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
