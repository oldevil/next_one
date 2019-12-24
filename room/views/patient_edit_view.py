import logging

from room.models.patient import Patient
from django.http import HttpResponse
from rest_framework import status
from utils.detail import Type, Success, Error

logger = logging.getLogger('patient')


def patient_detail(request, patient_id):
    pass


def patient_edit(request):
    if request.POST.get('id'):
        patient = Patient.objects.get(pk=request.POST.get('id'))
        for key, value in request.POST.items():
            patient.__dict__[key] = value
        detail = Success.PATIENT_EDITED
        status_code = status.HTTP_200_OK
    else:
        patient = Patient(name=request.POST.get('name'), surgeon=request.POST.get('surgeon'), assistant=request.POST.get('assistant'))
        detail = Success.PATIENT_CREATED
        status_code = status.HTTP_201_CREATED

    patient.save()
    log_detail = {
        'id': patient.id,
        'type': Type.SUCCESS,
        'detail': detail
    }
    logger.info(log_detail)
    return HttpResponse(detail, status=status_code)
