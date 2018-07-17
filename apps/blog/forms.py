# -*- coding:utf-8 -*-
from blog.models import PageDetail
from django.forms import ModelForm


class PublishForm(ModelForm):
    class Meta:
        model = PageDetail
        fields = ['title', 'category', 'author', 'detail', 'image', 'tags']   # 表单提交字段

__author__ = 'KoiSato'
