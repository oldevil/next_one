from django.db import models
from room.models.patient import Patient
import datetime


class Room(models.Model):
    number = models.IntegerField('手术室编号')
    current_patient = models.ForeignKey(Patient, blank=True, null=True, on_delete=models.SET_NULL)
    entry_time = models.DateTimeField('入室时间', blank=True, null=True)
    patient_queue = models.CharField('病人队列', max_length=200, blank=True, null=True)
