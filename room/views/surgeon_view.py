import logging

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import ObjectDoesNotExist
from rest_framework import status
from room.models.surgeon import Surgeon
from utils.detail import Type, Success, Error, Message
from utils.decorators import logit

logger = logging.getLogger('surgeon')


@logit
def surgeon_detail(request, surgeon_id):
    try:
        surgeon = Surgeon.objects.get(pk=surgeon_id)
        context = {
            'id': surgeon_id,
            'name': surgeon.name,
            'segment': surgeon.segment,
            'submit': '修改',
        }
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('room:surgeon_index'))
    template = loader.get_template('room/surgeon_detail.html')
    return HttpResponse(template.render(context, request))


@logit
def surgeon_create(request):
    context = {
        'name': '',
        'segment': '',
        'submit': '新建',
    }
    template = loader.get_template('room/surgeon_detail.html')
    return HttpResponse(template.render(context, request))


@logit
def surgeon_edit(request):
    if request.POST.get('id'):
        try:
            surgeon = Surgeon.objects.get(pk=request.POST.get('id'))
            detail = Success.SURGEON_EDITED
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('room:surgeon_index'))
    else:
        surgeon = Surgeon.objects.create()
        surgeon.save()
        detail = Success.SURGEON_CREATED
    surgeon.name = request.POST.get('name')
    surgeon.segment = request.POST.get('segment')
    surgeon.save()

    log_detail = {
        'id': surgeon.id,
        'type': Type.SUCCESS,
        'detail': detail
    }
    logger.info(log_detail)

    return HttpResponseRedirect(reverse('room:surgeon_index'))


@logit
def surgeon_index(request):
    anterior_surgeons = Surgeon.objects.filter(segment=0)
    posterior_surgeons = Surgeon.objects.filter(segment=1)
    context = {
        'anterior_surgeons': anterior_surgeons,
        'posterior_surgeons': posterior_surgeons,
    }
    template = loader.get_template('room/surgeon_index.html')
    return HttpResponse(template.render(context, request))


@logit
def surgeon_delete(request):
    surgeon_id = int(request.POST.get('surgeon_id'))
    try:
        surgeon = Surgeon.objects.get(pk=surgeon_id)
        surgeon.delete()
        log_type = Type.SUCCESS
        detail = Success.SURGEON_DELETED
        message = detail
        status_code = status.HTTP_200_OK
    except ObjectDoesNotExist:
        log_type = Type.ERROR
        detail = Error.SURGEON_ALREADY_DELETED
        message = Message.SURGEON_ALREADY_DELETED
        status_code = status.HTTP_404_NOT_FOUND

    log_detail = {
        'id': surgeon_id,
        'type': log_type,
        'detail': detail
    }
    logger.info(log_detail)

    return HttpResponse(message, status=status_code)
