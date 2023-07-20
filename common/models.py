import uuid
from django.db import models


class CommonModel(models.Model):

    """Common Model"""

    created_at = models.DateTimeField(
        verbose_name="만든날짜",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="변경날짜",
        auto_now=True,
    )

    # do not make Database Table
    class Meta:
        abstract = True


class CommonPKModel(models.Model):

    """Common Model"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    # do not make Database Table
    class Meta:
        abstract = True
