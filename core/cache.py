#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'vinman'

import redis
from django.conf import settings

connection = redis.Redis(
    host=getattr(settings, 'REDIS_HOST', 'localhost'),
    port=getattr(settings, 'REDIS_PORT', 6739),
    db=getattr(settings, 'REDIS_DB', 0),
    password=getattr(settings, 'REDIS_PASSWORD', None),
    socket_timeout=getattr(settings, 'REDIS_SOCKET_TIMEOUT', None),
    connection_pool=getattr(settings, 'REDIS_CONNECTION_POOL', None),
    charset=getattr(settings, 'REDIS_CHARSET', 'utf-8'),
)
