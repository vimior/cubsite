#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'vinman'

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse("Hello cubsite!")