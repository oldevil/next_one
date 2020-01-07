import ast

from django.db import models


class Room(models.Model):
    status_map = {
        0: 'patient_queue',
        1: 'patient_got_queue',
        2: 'patient_tomorrow_queue',
    }

    number = models.IntegerField('手术室编号', blank=True, null=True)
    patient_got_queue = models.CharField('已接病人队列', max_length=200, blank=True, null=True, default='[]')
    patient_queue = models.CharField('未接病人队列', max_length=200, blank=True, null=True, default='[]')
    patient_tomorrow_queue = models.CharField('明日病人队列', max_length=200, blank=True, null=True, default='[]')

    def append_queue(self, patient_id, target='patient_queue'):
        queue = ast.literal_eval(getattr(self, target))
        queue.append(patient_id)
        setattr(self, target, str(queue))
        self.save()

    def remove_queue(self, patient_id):
        from room.models.patient import Patient
        target = self.status_map[Patient.objects.get(pk=patient_id).status]
        queue = ast.literal_eval(getattr(self, target))
        queue.remove(patient_id)
        setattr(self, target, str(queue))
        self.save()

    def get_next_patient(self):
        from room.models.patient import Patient
        if self.patient_queue == '[]':
            return None
        return Patient.objects.get(pk=ast.literal_eval(self.patient_queue)[0])

    def get_current_patient(self):
        from room.models.patient import Patient
        if self.patient_got_queue == '[]':
            return None
        return Patient.objects.get(pk=ast.literal_eval(self.patient_got_queue)[-1])
