from django.db import models
from django.conf import settings
from common.models import CommonModel, CommonPKModel


class Photo(CommonModel, CommonPKModel):
    cf_id = models.URLField()
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    description = models.CharField(
        max_length=140,
    )
    pharmacy = models.ForeignKey(
        "pharmacies.Pharmacy",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return "Photo File"
