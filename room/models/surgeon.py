from django.db import models


class Surgeon(models.Model):
    SEGMENT = (
        (0, '前节'),
        (1, '后节')
    )

    name = models.CharField('姓名', max_length=200, blank=True, null=True)
    segment = models.IntegerField('节', choices=SEGMENT, blank=True, null=True)
