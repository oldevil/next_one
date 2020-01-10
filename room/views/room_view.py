import logging
import ast

from datetime import date
from django.core.cache import cache
from django.http import HttpResponse
from django.template import loader
from rest_framework import status
from room.models.patient import Patient
from room.models.room import Room
from utils.detail import Type, Success, Error, Message
from utils.date_util import next_workday
from utils.decorators import logit
from conf.config import cache_ttl

logger = logging.getLogger('room')


@logit
def room_index(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms,
    }
    template = loader.get_template('room/room_index.html')
    return HttpResponse(template.render(context, request))


@logit
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


@logit
def room_update_queue(request, room_id):
    room = Room.objects.get(pk=room_id)
    key = 'room_{}_sorting'.format(room.id)
    value = request.POST.get('value')

    if not cache.get(key) or cache.get(key) != value:
        log_type = Type.ERROR
        detail = Error.ROOM_SORTING_TIMEOUT
        message = Message.ROOM_SORTING_TIMEOUT
        status_code = status.HTTP_403_FORBIDDEN
    else:
        cache.set(key, value, cache_ttl)
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
        log_type = Type.SUCCESS
        detail = Success.ROOM_QUEUE_UPDATED
        message = detail
        status_code = status.HTTP_200_OK

    log_detail = {
        'id': room_id,
        'type': log_type,
        'detail': detail,
    }
    logger.info(log_detail)

    return HttpResponse(message, status=status_code)


@logit
def room_cache_api(request):
    operation = request.POST.get('operation')
    key = request.POST.get('key')
    value = request.POST.get('value')

    if operation == 'get_or_set':
        if cache.get(key):
            message = Error.ROOM_BLOCKING
            status_code = status.HTTP_403_FORBIDDEN
        else:
            cache.set(key, value, cache_ttl)
            message = Type.SUCCESS
            status_code = status.HTTP_200_OK
    elif operation == 'delete':
        if cache.get(key) and cache.get(key) == value:
            cache.delete(key)
        message = Type.SUCCESS
        status_code = status.HTTP_200_OK
    else:  # operation == 'get'
        if cache.get(key):
            message = Error.ROOM_BLOCKING
            status_code = status.HTTP_403_FORBIDDEN
        else:
            message = Type.SUCCESS
            status_code = status.HTTP_200_OK

    return HttpResponse(message, status=status_code)
