import logging

from room.models.surgeon import Surgeon
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from utils.detail import Type, Success, Error
from django.urls import reverse

logger = logging.getLogger('surgeon')


def surgeon_detail(request, surgeon_id):
    surgeon = Surgeon.objects.get(pk=surgeon_id)
    context = {
        'id': surgeon_id,
        'name': surgeon.name,
        'segment': surgeon.segment,
        'submit': '修改',
    }
    template = loader.get_template('room/surgeon_detail.html')
    return HttpResponse(template.render(context, request))


def surgeon_create(request):
    context = {
        'name': '',
        'segment': '',
        'submit': '新建',
    }
    template = loader.get_template('room/surgeon_detail.html')
    return HttpResponse(template.render(context, request))


def surgeon_edit(request):
    if request.POST.get('id'):
        surgeon = Surgeon.objects.get(pk=request.POST.get('id'))
        detail = Success.SURGEON_EDITED
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


def surgeon_index(request):
    anterior_surgeons = Surgeon.objects.filter(segment=0)
    posterior_surgeons = Surgeon.objects.filter(segment=1)
    context = {
        'anterior_surgeons': anterior_surgeons,
        'posterior_surgeons': posterior_surgeons,
    }
    template = loader.get_template('room/surgeon_index.html')
    return HttpResponse(template.render(context, request))


def surgeon_delete(request, surgeon_id):
    surgeon = Surgeon.objects.get(pk=surgeon_id)
    surgeon.delete()

    detail = Success.SURGEON_DELETED
    log_detail = {
        'id': surgeon.id,
        'type': Type.SUCCESS,
        'detail': detail
    }
    logger.info(log_detail)

    return HttpResponseRedirect(reverse('room:surgeon_index'))
