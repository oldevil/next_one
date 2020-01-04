from django.db import models
from room.models.surgeon import Surgeon
from room.models.assistant import Assistant


class Patient(models.Model):
    STATUS_CHOICES = (
        (0, '未接'),
        (1, '已接')
    )

    name = models.CharField('姓名', max_length=200, blank=True, null=True)
    surgeon = models.ForeignKey(Surgeon, blank=True, null=True, on_delete=models.SET_NULL)
    assistant = models.ForeignKey(Assistant, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.IntegerField('病人状态', choices=STATUS_CHOICES, default=0)
    room_number = models.IntegerField('手术室编号', blank=True, null=True)
