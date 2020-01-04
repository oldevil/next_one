import logging
import datetime
import ast

from room.models.patient import Patient
from room.models.room import Room
from room.models.assistant import Assistant
from room.models.surgeon import Surgeon
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import status
from django.template import loader
from utils.detail import Type, Success, Error
from django.urls import reverse
from django.core.mail import send_mail

logger = logging.getLogger('patient')


def patient_detail(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    rooms = Room.objects.all()
    assistants = Assistant.objects.all()
    anterior_surgeons = Surgeon.objects.filter(segment=0)
    posterior_surgeons = Surgeon.objects.filter(segment=1)
    context = {
        'id': patient_id,
        'name': patient.name,
        'surgeon': patient.surgeon,
        'assistant': patient.assistant,
        'room_number': patient.room_number if patient.room_number else '',
        'rooms': rooms,
        'assistants': assistants,
        'anterior_surgeons': anterior_surgeons,
        'posterior_surgeons': posterior_surgeons,
        'redirect': 'detail',
        'submit': '修改',
    }
    template = loader.get_template('room/patient_detail.html')
    return HttpResponse(template.render(context, request))


def patient_create(request):
    rooms = Room.objects.all()
    assistants = Assistant.objects.all()
    anterior_surgeons = Surgeon.objects.filter(segment=0)
    posterior_surgeons = Surgeon.objects.filter(segment=1)
    if request.POST.get('room_number'):
        room_number = int(request.POST.get('room_number'))
        redirect = 'detail'
    else:
        room_number = ''
        redirect = 'index'
    context = {
        'name': '',
        'surgeon': '',
        'assistant': '',
        'room_number': room_number,
        'rooms': rooms,
        'assistants': assistants,
        'anterior_surgeons': anterior_surgeons,
        'posterior_surgeons': posterior_surgeons,
        'redirect': redirect,
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
    surgeon = request.POST.get('surgeon')
    if surgeon:
        patient.surgeon = Surgeon.objects.get(pk=surgeon)
    assistant = request.POST.get('assistant')
    if assistant:
        patient.assistant = Assistant.objects.get(pk=assistant)
    if room_number != '':
        patient.room_number = request.POST.get('room_number')

    patient.save()
    log_detail = {
        'id': patient.id,
        'type': Type.SUCCESS,
        'detail': detail
    }
    logger.info(log_detail)
    redirect = request.POST.get('redirect')
    if redirect == 'index':
        return HttpResponseRedirect(reverse('room:room_index'))
    elif redirect == 'detail':
        return HttpResponseRedirect(reverse('room:room_detail', kwargs={'room_id': Room.objects.filter(number=room_number)[0].id}))


def patient_get_in(request, patient_id):
    # TODO logger
    patient = Patient.objects.get(pk=patient_id)
    patient.status = 1
    patient.save()

    if patient.assistant:
        send_mail(
            '{}间患者{}已接'.format(patient.room_number, patient.name),
            '请不要迟到，喵~',
            'Next-one-Admin-J<1010301308@pku.edu.cn>',
            [patient.assistant.email],
            fail_silently=False,
        )

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


def patient_delete(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    room = Room.objects.filter(number=patient.room_number)[0]
    patient_queue = ast.literal_eval(room.patient_queue)
    patient_queue.remove(patient.id)
    room.patient_queue = str(patient_queue)
    patient.delete()
    room.save()

    return HttpResponseRedirect(reverse('room:room_detail', kwargs={'room_id': room.id}))
