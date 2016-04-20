#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'vinman'

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    """
    模型基础类
    """
    user = models.ForeignKey(User, verbose_name=u'创建者', blank=True, null=True)

    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)

    is_deleted = models.BooleanField(u'是否已删除', default=False)
    is_active = models.BooleanField(u'是否激活', default=True)

    class Meta:
        abstract = True
        ordering = ['-create_time']

