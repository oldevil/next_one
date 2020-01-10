import logging

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import ObjectDoesNotExist
from rest_framework import status
from room.models.assistant import Assistant
from utils.detail import Type, Success, Error, Message
from utils.decorators import logit

logger = logging.getLogger('assistant')


@logit
def assistant_detail(request, assistant_id):
    try:
        assistant = Assistant.objects.get(pk=assistant_id)
        context = {
            'id': assistant_id,
            'name': assistant.name,
            'email': assistant.email,
            'submit': '修改',
        }
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('room:assistant_index'))
    template = loader.get_template('room/assistant_detail.html')
    return HttpResponse(template.render(context, request))


@logit
def assistant_create(request):
    context = {
        'name': '',
        'email': '',
        'submit': '新建',
    }
    template = loader.get_template('room/assistant_detail.html')
    return HttpResponse(template.render(context, request))


@logit
def assistant_edit(request):
    if request.POST.get('id'):
        try:
            assistant = Assistant.objects.get(pk=request.POST.get('id'))
            detail = Success.ASSISTANT_EDITED
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('room:assistant_index'))
    else:
        assistant = Assistant.objects.create()
        assistant.save()
        detail = Success.ASSISTANT_CREATED
    assistant.name = request.POST.get('name')
    assistant.email = request.POST.get('email')
    assistant.save()

    log_detail = {
        'id': assistant.id,
        'type': Type.SUCCESS,
        'detail': detail
    }
    logger.info(log_detail)

    return HttpResponseRedirect(reverse('room:assistant_index'))


@logit
def assistant_index(request):
    assistants = Assistant.objects.all()
    context = {
        'assistants': assistants,
    }
    template = loader.get_template('room/assistant_index.html')
    return HttpResponse(template.render(context, request))


@logit
def assistant_delete(request):
    assistant_id = int(request.POST.get('assistant_id'))
    try:
        assistant = Assistant.objects.get(pk=assistant_id)
        assistant.delete()
        log_type = Type.SUCCESS
        detail = Success.ASSISTANT_DELETED
        message = detail
        status_code = status.HTTP_200_OK
    except ObjectDoesNotExist:
        log_type = Type.ERROR
        detail = Error.ASSISTANT_ALREADY_DELETED
        message = Message.ASSISTANT_ALREADY_DELETED
        status_code = status.HTTP_404_NOT_FOUND

    log_detail = {
        'id': assistant_id,
        'type': log_type,
        'detail': detail,
    }
    logger.info(log_detail)

    return HttpResponse(message, status=status_code)
