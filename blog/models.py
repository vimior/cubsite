#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'vinman'

from django.db import models
from django.conf import settings
from django.db.models import F
from django.db.models.signals import m2m_changed, pre_delete, pre_save, post_delete, post_save

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
        app_label = string_with_title('blog', u'博客管理')


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


class Blog(BaseModel):
    """
    博客 Model
    """
    title = models.CharField(u'标题', max_length=100)

    category = models.ForeignKey(Category, verbose_name=u'分类')
    theme = models.ForeignKey(Theme, verbose_name=u'主题')
    topic = models.ForeignKey(Topic, verbose_name=u'专题', blank=True, null=True)
    tags = models.ManyToManyField(Tag, verbose_name=u'标签', blank=True)

    # 用于博客首页是否置顶展示
    is_recommended = models.BooleanField(u'是否推荐', default=False)
    # 概要，用于列表页显示
    summary = models.CharField(u'概要', max_length=512, blank=True)
    # 博客主体内容
    # content = RichTextField(u'内容')
    # 冗余计数
    click_count = models.IntegerField(u'点击量', default=0, editable=False)
    comment_count = models.IntegerField(u'评论数', default=0, editable=False)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'博客'
        verbose_name_plural = u'博客'

    def click(self, session_key, ip_addr):
        """
        点击统计,同一IP同一session视为相同点击
        :param session_key: 会话ID
        :param ip_addr: IP地址
        """
        from core.cache import connection
        cache_key = settings.BLOG_VISITORS_CACHE_KEY.format(self.id)
        if int(connection.zincrby(cache_key, '{0}-{1}'.format(ip_addr, session_key))) == 1:
            self.click_count = F('click_count') + 1
            self.save()
        if connection.zcard(cache_key) == 1:
            connection.expire(cache_key, settings.BLOG_VISITORS_CACHE_TIMEOUT)

    @property
    def tag_list(self):
        return self.tags.filter(is_deleted=False, is_active=True)


class Comment(BaseModel):
    """
    通用评论 Model
    """
    comment = models.CharField(u'评论内容', max_length=1000)
    username = models.CharField(u'用户名', max_length=64, blank=True)
    email = models.EmailField(u'邮箱')
    is_public = models.BooleanField(u'是否公开', default=True)
    ip_address = models.GenericIPAddressField(u'发布IP地址', unpack_ipv4=True, blank=True, null=True)

    class Meta:
        verbose_name = u'评论'
        verbose_name_plural = u'评论'

class BlogComment(Comment):
    """
    博客评论 Model,继承自通用评论
    """
    blog = models.ForeignKey(Blog, verbose_name=u'所属博客')

    def __unicode__(self):
        return '来自用户 {0} 对 {1} 的评论'.format(self.username or self.ip_address, self.blog.title)

    class Meta:
        verbose_name = u'博客评论'
        verbose_name_plural = u'博客评论'

def handle_in_batches(instances, method):
    for instance in instances:
        getattr(instance, method)()

def tags_changed(sender, **kwargs):
    """
    处理标签关联变化,主要对冗余计数进行加减操作
    """
    if kwargs.get('action') == 'pre_clear':
        handle_in_batches(kwargs.get('instance').tags.all(), 'decrease')
    elif kwargs.get('action') == 'post_remove':
        handle_in_batches(Tag.objects.filter(id__in=kwargs.get('pk_set')), 'decrease')
    elif kwargs.get('action') == 'post_add':
        handle_in_batches(Tag.objects.filter(id__in=kwargs.get('pk_set')), 'increase')

def blog_pre_save(sender, **kwargs):
    """
    博客保存前,对关联对象的冗余计数进行处理
    """
    curr = kwargs.get('instance')
    try:
        prev = Blog.objects.get(id=curr.id)
    except Blog.DoesNotExist:
        if not curr.is_deleted and curr.is_active:
            curr.theme.increase()
            curr.category.increase()
    else:
        prev_ps = prev.is_active and not prev.is_deleted
        curr_ps = curr.is_active and not curr.is_deleted
        for item in ['theme', 'category', 'topic']:
            prev_obj, curr_obj = getattr(prev, item), getattr(curr, item)

            if prev_obj and prev_ps and not curr_ps or prev_ps and prev_obj and not prev_obj == curr_obj:
                prev_obj.decrease()

            if curr_obj and curr_ps and not prev_ps or curr_ps and curr_obj and not prev_obj == curr_obj:
                curr_obj.increase()

def blog_pre_delete(sender, **kwargs):
    """
    博客删除前对冗余计数进行处理
    """

    instance = kwargs.get('instance')
    for item in ['theme', 'category', 'topic']:
        obj = getattr(instance, item)
        if obj:
            obj.decr()
    handle_in_batches(instance.tags.all(), 'decrease')


def blogcomment_pre_save(sender, **kwargs):
    """
    评论保存前对冗余计数进行必要的减处理
    """

    instance = kwargs.get('instance')
    if instance.id:
        try:
            old = BlogComment.objects.get(id=instance.id)
        except BlogComment.DoesNotExist:
            return
        if not old.is_deleted and old.is_active and old.is_public:
            blog = old.blog
            blog.comment_count = F('comment_count') - 1
            blog.save()


def blogcomment_post_save(sender, **kwargs):
    """
    评论保存前对冗余计数进行必要的加处理
    """

    instance = kwargs.get('instance')
    if not instance.is_deleted and instance.is_active and instance.is_public:
        blog = instance.blog
        blog.comment_count = F('comment_count') + 1
        blog.save()


def blogcomment_post_delete(sender, **kwargs):
    """
    评论删除前对冗余计数进行必要的减处理
    """

    instance = kwargs.get('instance')
    if not instance.is_deleted and instance.is_active and instance.is_public:
        blog = instance.blog
        blog.comment_count = F('comment_count') - 1
        blog.save()

# 关联信号
m2m_changed.connect(tags_changed, sender=Blog.tags.through)
pre_save.connect(blog_pre_save, sender=Blog)
pre_delete.connect(blog_pre_delete, sender=Blog)
pre_save.connect(blogcomment_pre_save, sender=BlogComment)
post_save.connect(blogcomment_post_save, sender=BlogComment)
post_delete.connect(blogcomment_post_delete, sender=BlogComment)
