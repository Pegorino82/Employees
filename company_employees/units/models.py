from django.db import models


class Unit(models.Model):
    title = models.CharField(
        max_length=128,
        null=False,
        blank=False
    )
