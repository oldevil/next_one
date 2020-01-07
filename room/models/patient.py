from django.db import models
from room.models.room import Room
from room.models.surgeon import Surgeon
from room.models.assistant import Assistant


class Patient(models.Model):
    STATUS_CHOICES = (
        (0, '未接'),
        (1, '已接'),
        (2, '明日'),
        (3, '计划'),
    )

    name = models.CharField('姓名', max_length=200, blank=True, null=True)
    surgeon = models.ForeignKey(Surgeon, blank=True, null=True, on_delete=models.SET_NULL)
    assistant = models.ForeignKey(Assistant, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.IntegerField('病人状态', choices=STATUS_CHOICES, blank=True, null=True)
    room = models.ForeignKey(Room, blank=True, null=True, on_delete=models.SET_NULL)
    entry_time = models.DateTimeField('入室时间', blank=True, null=True)
    operation_date = models.DateField('手术日期', blank=True, null=True)
