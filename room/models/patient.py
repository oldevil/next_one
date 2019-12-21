from django.db import models


class Patient(models.Model):
    STATUS_CHOICES = (
        (0, '未接'),
        (1, '已接')
    )

    name = models.CharField('姓名', max_length=200)
    surgeon = models.CharField('主刀', max_length=200, blank=True, null=True)
    assistant = models.CharField('一助', max_length=200, blank=True, null=True)
    status = models.IntegerField('病人状态', choices=STATUS_CHOICES, default=0)
