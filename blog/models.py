#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'vinman'

from django.db import models
from django.db.models import F
from core.models import BaseModel

# Create your models here.

#用来修改admin中显示的app名称,因为admin app 名称是用 str.title()显示的,所以修改str类的title方法就可以实现.
class string_with_title(str):
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self

class Base(BaseModel):
    """
    (标签、分类、主题、专题) 的基础类
    """
    name = models.CharField(u'名称', max_length=30)
    # 冗余计数
    count = models.IntegerField(u'引用', default=0)

    def __unicode__(self):
        return self.name

    def increase(self, num=1):
        self.count = F('count') + num
        self.save()

    def decrease(self, num=1):
        self.count = F('count') - num
        self.save()

    class Meta:
        abstract = True


class Tag(Base):
    """
    标签 Model
    """

    class Meta:
        verbose_name = u'标签'
        verbose_name_plural = u'标签'

class Category(Base):
    """
    分类 Model
    """
    
    class Meta:
        verbose_name = u'分类'
        verbose_name_plural = u'分类'

class Theme(Base):
    """
    主题 Model
    """
    class Meta:
        verbose_name = u'主题'
        verbose_name_plural = u'主题'

class Topic(Base):
    """
    专题 Model
    """
    class Meta:
        verbose_name = u'专题'
        verbose_name_plural = u'专题'




