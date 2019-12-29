import logging
import datetime
import ast

from room.models.patient import Patient
from room.models.room import Room
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import status
from django.template import loader
from utils.detail import Type, Success, Error
from django.urls import reverse

logger = logging.getLogger('patient')


def patient_detail(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    context = {
        'id': patient_id,
        'name': patient.name,
        'surgeon': patient.surgeon,
        'assistant': patient.assistant,
        'room_number': patient.room_number if patient.room_number else '',
        'submit': '修改',
    }
    template = loader.get_template('room/patient_detail.html')
    return HttpResponse(template.render(context, request))


def patient_create(request):
    context = {
        'name': '',
        'surgeon': '',
        'assistant': '',
        'room_number': '',
        'submit': '新建',
    }
    template = loader.get_template('room/patient_detail.html')
    return HttpResponse(template.render(context, request))


def patient_edit(request):
    if request.POST.get('id'):
        patient = Patient.objects.get(pk=request.POST.get('id'))
        detail = Success.PATIENT_EDITED
        status_code = status.HTTP_200_OK
    else:
        patient = Patient.objects.create()
        patient.save()
        detail = Success.PATIENT_CREATED
        status_code = status.HTTP_201_CREATED

    room_number = request.POST.get('room_number')
    if room_number != '':
        if patient.room_number != int(room_number):
            if patient.room_number:
                Room.objects.filter(number=patient.room_number)[0].remove_queue(patient.id)
            Room.objects.filter(number=room_number)[0].append_queue(patient.id)

    patient.name = request.POST.get('name')
    patient.surgeon = request.POST.get('surgeon')
    patient.assistant = request.POST.get('assistant')
    if room_number != '':
        patient.room_number = request.POST.get('room_number')

    patient.save()
    log_detail = {
        'id': patient.id,
        'type': Type.SUCCESS,
        'detail': detail
    }
    logger.info(log_detail)
    return HttpResponseRedirect(reverse('room:room_index'))
    # return HttpResponse(detail, status=status_code)


def patient_get_in(request, patient_id):
    # TODO logger
    patient = Patient.objects.get(pk=patient_id)
    patient.status = 1
    patient.save()

    room = Room.objects.filter(number=patient.room_number)[0]
    if room.current_patient:
        room.current_patient.delete()
    room.current_patient = patient
    room.entry_time = datetime.datetime.now()
    patient_queue = ast.literal_eval(room.patient_queue)
    patient_queue.pop(0)
    room.patient_queue = str(patient_queue)
    room.save()

    return HttpResponseRedirect(reverse('room:room_index'))
