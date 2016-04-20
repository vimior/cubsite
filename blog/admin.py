#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'vinman'

from django.contrib import admin
from core.admin import BaseModelAdmin
from blog.models import Tag, Category, Theme, Topic

# Register your models here.

class CAdmin(BaseModelAdmin):
    """
    (标签、分类、主题、专题) 的通用 Admin
    """
    fields = ['name', 'is_active']
    list_display = ['name', 'count', 'create_time', 'is_active']



admin.site.register([Tag, Category, Theme, Topic], CAdmin)

