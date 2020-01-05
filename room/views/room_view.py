import logging
import ast

from room.models.patient import Patient
from room.models.room import Room
from django.http import HttpResponse
from rest_framework import status
from django.template import loader
from utils.detail import Type, Success, Error

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
    patients = [Patient.objects.get(pk=i) for i in patient_queue]
    patients_got = [Patient.objects.get(pk=i) for i in patient_got_queue]
    context = {
        'room': room,
        'patients': patients,
        'patients_got': patients_got,
    }
    template = loader.get_template('room/room_detail.html')
    return HttpResponse(template.render(context, request))


def room_update_queue(request, room_id):
    patient_queue = request.POST.get('patient_queue')
    room = Room.objects.get(pk=room_id)
    room.patient_queue = patient_queue
    room.save()

    detail = Success.ROOM_QUEUE_UPDATED
    log_detail = {
        'id': room.id,
        'type': Type.SUCCESS,
        'detail': detail
    }
    logger.info(log_detail)

    return HttpResponse(detail, status=status.HTTP_200_OK)


def room_roll_back(request, room_id):
    patient_id = request.POST.get('patient_id')
    patient = Patient.objects.get(pk=patient_id)
    patient.entry_time = None
    patient.status = 0
    patient.save()

    room = Room.objects.get(pk=room_id)
    room.remove_got_queue(patient.id)
    patient_queue = request.POST.get('patient_queue')
    room.patient_queue = patient_queue
    room.save()

    detail = Success.ROOM_ROLL_BACKED
    log_detail = {
        'id': room.id,
        'type': Type.SUCCESS,
        'detail': detail
    }
    logger.info(log_detail)

    return HttpResponse(detail, status=status.HTTP_200_OK)
