# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u5220\u9664')),
                ('is_active', models.BooleanField(default=True, verbose_name='\u662f\u5426\u6fc0\u6d3b')),
                ('name', models.CharField(max_length=30, verbose_name='\u540d\u79f0')),
                ('count', models.IntegerField(default=0, verbose_name='\u5f15\u7528')),
                ('user', models.ForeignKey(verbose_name='\u521b\u5efa\u8005', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u5206\u7c7b',
                'verbose_name_plural': '\u5206\u7c7b',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u5220\u9664')),
                ('is_active', models.BooleanField(default=True, verbose_name='\u662f\u5426\u6fc0\u6d3b')),
                ('name', models.CharField(max_length=30, verbose_name='\u540d\u79f0')),
                ('count', models.IntegerField(default=0, verbose_name='\u5f15\u7528')),
                ('user', models.ForeignKey(verbose_name='\u521b\u5efa\u8005', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u6807\u7b7e',
                'verbose_name_plural': '\u6807\u7b7e',
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u5220\u9664')),
                ('is_active', models.BooleanField(default=True, verbose_name='\u662f\u5426\u6fc0\u6d3b')),
                ('name', models.CharField(max_length=30, verbose_name='\u540d\u79f0')),
                ('count', models.IntegerField(default=0, verbose_name='\u5f15\u7528')),
                ('user', models.ForeignKey(verbose_name='\u521b\u5efa\u8005', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u4e3b\u9898',
                'verbose_name_plural': '\u4e3b\u9898',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u5220\u9664')),
                ('is_active', models.BooleanField(default=True, verbose_name='\u662f\u5426\u6fc0\u6d3b')),
                ('name', models.CharField(max_length=30, verbose_name='\u540d\u79f0')),
                ('count', models.IntegerField(default=0, verbose_name='\u5f15\u7528')),
                ('user', models.ForeignKey(verbose_name='\u521b\u5efa\u8005', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u4e13\u9898',
                'verbose_name_plural': '\u4e13\u9898',
            },
        ),
    ]
