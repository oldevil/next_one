from django.db import models


class Assistant(models.Model):
    name = models.CharField('姓名', max_length=200, blank=True, null=True)
    email = models.CharField('邮箱', max_length=200, blank=True, null=True)
