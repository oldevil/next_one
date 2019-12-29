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
    # return HttpResponse(request.environ['HTTP_USER_AGENT'])
    rooms = Room.objects.order_by('number')
    context = {
        'rooms': rooms,
    }
    template = loader.get_template('room/room_index.html')
    return HttpResponse(template.render(context, request))


def room_detail(request, room_id):
    room = Room.objects.get(pk=room_id)
    patient_queue = ast.literal_eval(room.patient_queue)
    patients = [Patient.objects.get(pk=i) for i in patient_queue]
    context = {
        'patients': patients,
    }
    template = loader.get_template('room/room_detail.html')
    return HttpResponse(template.render(context, request))
