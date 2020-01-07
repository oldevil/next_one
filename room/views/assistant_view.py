import logging

from room.models.assistant import Assistant
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from utils.detail import Type, Success, Error
from django.urls import reverse

logger = logging.getLogger('assistant')


def assistant_detail(request, assistant_id):
    assistant = Assistant.objects.get(pk=assistant_id)
    context = {
        'id': assistant_id,
        'name': assistant.name,
        'email': assistant.email,
        'submit': '修改',
    }
    template = loader.get_template('room/assistant_detail.html')
    return HttpResponse(template.render(context, request))


def assistant_create(request):
    context = {
        'name': '',
        'email': '',
        'submit': '新建',
    }
    template = loader.get_template('room/assistant_detail.html')
    return HttpResponse(template.render(context, request))


def assistant_edit(request):
    if request.POST.get('id'):
        assistant = Assistant.objects.get(pk=request.POST.get('id'))
        detail = Success.ASSISTANT_EDITED
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


def assistant_index(request):
    assistants = Assistant.objects.all()
    context = {
        'assistants': assistants,
    }
    template = loader.get_template('room/assistant_index.html')
    return HttpResponse(template.render(context, request))


def assistant_delete(request, assistant_id):
    assistant = Assistant.objects.get(pk=assistant_id)
    assistant.delete()

    detail = Success.ASSISTANT_DELETED
    log_detail = {
        'id': assistant.id,
        'type': Type.SUCCESS,
        'detail': detail
    }
    logger.info(log_detail)

    return HttpResponseRedirect(reverse('room:assistant_index'))
