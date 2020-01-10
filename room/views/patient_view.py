import logging
import datetime
import ast

from datetime import date
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import ObjectDoesNotExist
from django.core.cache import cache
from django.core.mail import send_mail
from rest_framework import status
from room.models.patient import Patient
from room.models.room import Room
from room.models.assistant import Assistant
from room.models.surgeon import Surgeon
from utils.detail import Type, Success, Error, Message
from utils.date_util import next_workday, today_is_workday
from utils.decorators import logit

logger = logging.getLogger('patient')


@logit
def patient_detail(request, patient_id, room_id):
    rooms = Room.objects.all()
    assistants = Assistant.objects.all()
    anterior_surgeons = Surgeon.objects.filter(segment=0)
    posterior_surgeons = Surgeon.objects.filter(segment=1)
    try:
        patient = Patient.objects.get(pk=patient_id)
        context = {
            'id': patient.id,
            'name': patient.name,
            'surgeon': patient.surgeon,
            'assistant': patient.assistant,
            'room_id': patient.room.id,
            'operation_date': str(patient.operation_date),
            'rooms': rooms,
            'assistants': assistants,
            'anterior_surgeons': anterior_surgeons,
            'posterior_surgeons': posterior_surgeons,
            'redirect': 'detail',
            'submit': '修改',
        }
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('room:room_detail', kwargs={'room_id': room_id}))
    template = loader.get_template('room/patient_detail.html')
    return HttpResponse(template.render(context, request))


@logit
def patient_create(request):
    rooms = Room.objects.all()
    assistants = Assistant.objects.all()
    anterior_surgeons = Surgeon.objects.filter(segment=0)
    posterior_surgeons = Surgeon.objects.filter(segment=1)
    if request.POST.get('room_id'):
        room_id = int(request.POST.get('room_id'))
        redirect = 'detail'
    else:
        room_id = ''
        redirect = 'index'
    context = {
        'name': '',
        'surgeon': '',
        'assistant': '',
        'room_id': room_id,
        'operation_date': str(next_workday()),
        'rooms': rooms,
        'assistants': assistants,
        'anterior_surgeons': anterior_surgeons,
        'posterior_surgeons': posterior_surgeons,
        'redirect': redirect,
        'submit': '新建',
    }
    template = loader.get_template('room/patient_detail.html')
    return HttpResponse(template.render(context, request))


@logit
def patient_edit(request):
    room_id = int(request.POST.get('room_id'))
    room = Room.objects.get(pk=room_id)
    operation_date = request.POST.get('operation_date')
    if operation_date:
        operation_date = date.fromisoformat(operation_date)
    else:
        operation_date = None
    if operation_date == date.today():
        patient_status = 0
    elif operation_date == next_workday():
        patient_status = 2
    else:
        patient_status = 3

    if request.POST.get('id'):
        try:
            patient = Patient.objects.get(pk=request.POST.get('id'))
            detail = Success.PATIENT_EDITED
            if patient.room.id != room.id or patient.operation_date != operation_date:
                if patient.status in (0, 2):
                    patient.room.remove_queue(patient.id)
                if patient_status == 0:
                    room.append_queue(patient.id)
                elif patient_status == 2:
                    room.append_queue(patient.id, 'patient_tomorrow_queue')
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('room:room_detail', kwargs={'room_id': room_id}))
    else:
        patient = Patient.objects.create()
        patient.save()
        if patient_status == 0:
            room.append_queue(patient.id)
        elif patient_status == 2:
            room.append_queue(patient.id, 'patient_tomorrow_queue')
        detail = Success.PATIENT_CREATED

    patient.name = request.POST.get('name')
    surgeon = request.POST.get('surgeon')
    if surgeon:
        try:
            patient.surgeon = Surgeon.objects.get(pk=surgeon)
        except ObjectDoesNotExist:
            pass
    assistant = request.POST.get('assistant')
    if assistant:
        try:
            patient.assistant = Assistant.objects.get(pk=assistant)
        except ObjectDoesNotExist:
            pass
    patient.status = patient_status
    patient.room = room
    patient.operation_date = operation_date
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
        return HttpResponseRedirect(reverse('room:room_detail', kwargs={'room_id': room_id}))


@logit
def patient_get_in(request):
    room_id = int(request.POST.get('room_id'))
    patient_id = int(request.POST.get('patient_id'))
    room = Room.objects.get(pk=room_id)
    if cache.get('room_{}_sorting'.format(room_id)):
        log_type = Type.ERROR
        detail = Error.ROOM_BLOCKING
        message = Message.ROOM_BLOCKING
        status_code = status.HTTP_403_FORBIDDEN
    else:
        try:
            patient = Patient.objects.get(pk=patient_id)
            assert room.get_next_patient() and room.get_next_patient().id == patient_id
            patient.status = 1
            patient.entry_time = datetime.datetime.now()
            patient.room.remove_queue(patient.id)
            patient.room.append_queue(patient_id, 'patient_got_queue')
            patient.save()

            if patient.assistant:
                send_mail(
                    '{}间患者{}已接'.format(patient.room.number, patient.name),
                    '请不要迟到，喵~',
                    'Next-one-Admin-J<1010301308@pku.edu.cn>',
                    [patient.assistant.email],
                    fail_silently=False,
                )

            log_type = Type.SUCCESS
            detail = Success.PATIENT_GOT_IN
            message = detail
            status_code = status.HTTP_200_OK
        except ObjectDoesNotExist:
            log_type = Type.ERROR
            detail = Error.PATIENT_NOT_EXIST
            message = Message.PATIENT_NOT_EXIST
            status_code = status.HTTP_404_NOT_FOUND
        except AssertionError:
            log_type = Type.ERROR
            detail = Error.PATIENT_NOT_IN_QUEUE
            message = Message.PATIENT_NOT_IN_QUEUE
            status_code = status.HTTP_404_NOT_FOUND

    log_detail = {
        'id': patient_id,
        'type': log_type,
        'detail': detail,
    }
    logger.info(log_detail)

    return HttpResponse(message, status=status_code)


@logit
def patient_delete(request):
    room_id = int(request.POST.get('room_id'))
    patient_id = int(request.POST.get('patient_id'))
    if cache.get('room_{}_sorting'.format(room_id)):
        log_type = Type.ERROR
        detail = Error.ROOM_BLOCKING
        message = Message.ROOM_BLOCKING
        status_code = status.HTTP_403_FORBIDDEN
    else:
        try:
            patient = Patient.objects.get(pk=patient_id)
            assert patient.room.id == room_id
            if patient.status in (0, 2):
                patient.room.remove_queue(patient.id)
            patient.delete()
            log_type = Type.SUCCESS
            detail = Success.PATIENT_DELETED
            message = detail
            status_code = status.HTTP_200_OK
        except ObjectDoesNotExist:
            log_type = Type.ERROR
            detail = Error.PATIENT_ALREADY_DELETED
            message = Message.PATIENT_ALREADY_DELETED
            status_code = status.HTTP_404_NOT_FOUND
        except AssertionError:
            log_type = Type.ERROR
            detail = Error.PATIENT_MOVED
            message = Message.PATIENT_MOVED
            status_code = status.HTTP_404_NOT_FOUND

    log_detail = {
        'id': patient_id,
        'type': log_type,
        'detail': detail,
    }
    logger.info(log_detail)

    return HttpResponse(message, status=status_code)


def patient_delete_got_patients():
    patients = Patient.objects.filter(status=1)
    for patient in patients:
        patient.room.remove_queue(patient.id)
        patient.delete()

    detail = Success.PATIENT_GOT_DELETED
    log_detail = {
        'id': [patient.id for patient in patients],
        'type': Type.SUCCESS,
        'detail': detail,
    }
    logger.info(log_detail)


def patient_check_tomorrow_queue():
    rooms = Room.objects.all()
    patient_ids = []
    if today_is_workday():
        for room in rooms:
            patient_tomorrow_queue = ast.literal_eval(room.patient_tomorrow_queue)
            patient_queue = ast.literal_eval(room.patient_queue)
            patient_queue.extend(patient_tomorrow_queue)
            room.patient_queue = str(patient_queue)
            room.patient_tomorrow_queue = '[]'
            room.save()
            for patient_id in patient_tomorrow_queue:
                patient_ids.append(patient_id)
                patient = Patient.objects.get(pk=patient_id)
                patient.status = 0
                patient.save()

    detail = Success.PATIENT_TOMORROW_QUEUE_CHECKED
    log_detail = {
        'id': patient_ids,
        'type': Type.SUCCESS,
        'detail': detail,
    }
    logger.info(log_detail)


def patient_check_project():
    patients = Patient.objects.filter(status=3)
    patient_ids = []
    for patient in patients:
        if patient.operation_date == next_workday():
            patient_ids.append(patient.id)
            patient.room.append_queue(patient.id, 'patient_tomorrow_queue')
            patient.status = 2
            patient.save()

    detail = Success.PATIENT_PROJECT_CHECKED
    log_detail = {
        'id': patient_ids,
        'type': Type.SUCCESS,
        'detail': detail,
    }
    logger.info(log_detail)


@logit
def patient_daily_check(request):
    patient_delete_got_patients()
    patient_check_tomorrow_queue()
    patient_check_project()

    detail = Success.PATIENT_DAILY_CHECKED
    log_detail = {
        'type': Type.SUCCESS,
        'detail': detail,
    }
    logger.info(log_detail)

    return HttpResponse(detail, status=status.HTTP_200_OK)
