#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'vinman'

from django.contrib import admin
from django.contrib.admin.sites import AdminSite

# Register your models here.

AdminSite.site_header = 'CubSite Administrator'
AdminSite.site_title = 'CubSite Administrator'

