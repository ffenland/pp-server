from django.db import models
from django.conf import settings
from common.models import CommonModel

# Create your models here.


class Post(CommonModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=30,
    )
    article = models.TextField()


class Reply(CommonModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=150,
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reply = models.ForeignKey("self", on_delete=models.CASCADE)
