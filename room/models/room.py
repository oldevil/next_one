import ast

from django.db import models


class Room(models.Model):
    number = models.IntegerField('手术室编号', blank=True, null=True)
    patient_got_queue = models.CharField('已接病人队列', max_length=200, blank=True, null=True, default='[]')
    patient_queue = models.CharField('病人队列', max_length=200, blank=True, null=True, default='[]')

    def append_queue(self, patient_id):
        queue = ast.literal_eval(self.patient_queue)
        queue.append(patient_id)
        self.patient_queue = str(queue)
        self.save()

    def remove_queue(self, patient_id):
        queue = ast.literal_eval(self.patient_queue)
        queue.remove(patient_id)
        self.patient_queue = str(queue)
        self.save()

    def append_got_queue(self, patient_id):
        queue = ast.literal_eval(self.patient_got_queue)
        queue.append(patient_id)
        self.patient_got_queue = str(queue)
        self.save()

    def remove_got_queue(self, patient_id):
        queue = ast.literal_eval(self.patient_got_queue)
        queue.remove(patient_id)
        self.patient_got_queue = str(queue)
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
