import logging
import ast

from datetime import date
from room.models.patient import Patient
from room.models.room import Room
from django.http import HttpResponse
from rest_framework import status
from django.template import loader
from utils.detail import Type, Success, Error
from utils.date_util import next_workday

logger = logging.getLogger('room')


def room_index(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms,
    }
    template = loader.get_template('room/room_index.html')
    return HttpResponse(template.render(context, request))


def room_detail(request, room_id):
    room = Room.objects.get(pk=room_id)
    patient_queue = ast.literal_eval(room.patient_queue)
    patient_got_queue = ast.literal_eval(room.patient_got_queue)
    patient_tomorrow_queue = ast.literal_eval(room.patient_tomorrow_queue)
    patients = [Patient.objects.get(pk=i) for i in patient_queue]
    patients_got = [Patient.objects.get(pk=i) for i in patient_got_queue]
    patients_tomorrow = [Patient.objects.get(pk=i) for i in patient_tomorrow_queue]
    patients_in_project = Patient.objects.filter(room=room, status=3)
    context = {
        'room': room,
        'patients': patients,
        'patients_got': patients_got,
        'patients_tomorrow': patients_tomorrow,
        'patients_in_project': patients_in_project,
    }
    template = loader.get_template('room/room_detail.html')
    return HttpResponse(template.render(context, request))


def room_update_queue(request, room_id):
    room = Room.objects.get(pk=room_id)

    if request.POST.get('queue'):
        queue = request.POST.get('queue')
        target = request.POST.get('target')
        room = Room.objects.get(pk=room_id)
        setattr(room, target, queue)
        room.save()

    if request.POST.get('patient_id'):
        patient = Patient.objects.get(pk=request.POST.get('patient_id'))
        if patient.status in (0, 1, 2):
            room.remove_queue(patient.id)
        patient.entry_time = None
        patient.status = int(request.POST.get('status'))
        if patient.status == 0:
            patient.operation_date = date.today()
        elif patient.status == 2:
            patient.operation_date = next_workday()
        elif patient.status == 3:
            patient.operation_date = None
        patient.save()

    detail = Success.ROOM_QUEUE_UPDATED
    log_detail = {
        'id': room.id,
        'type': Type.SUCCESS,
        'detail': detail
    }
    logger.info(log_detail)

    return HttpResponse(detail, status=status.HTTP_200_OK)
