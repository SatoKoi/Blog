# -*- coding:utf-8 -*-
from django import forms
from pure_pagination import PageNotAnInteger, Paginator
from django.forms.utils import ErrorList
from collections import defaultdict


def super_range(start: "str or int", stop: "str or int or None" = None, step: int = 1):
    """自定义range"""
    def yield_range(start, stop, step, type=None):
        while start <= stop:
            if start < stop:
                if type == 1:
                    if not 91 <= start <= 96:
                        yield chr(start)
                else:
                    yield start
            start += step

    if stop is not None:
        assert isinstance(start, type(stop)), "The type of start must be the same as the type of stop"
        if isinstance(start, str):
            start = ord(start[0])
            stop = ord(stop[0]) + 1
            assert start <= stop, "start must be smaller than stop"
            return yield_range(start, stop, step, type=1)
        if isinstance(start, int):
            assert start <= stop, "start must be smaller than stop"
            return yield_range(start, stop, step)
    else:
        if isinstance(start, int):
            return yield_range(0, start, step)
        if isinstance(start, str):
            if start[0] <= "Z":
                return yield_range(ord("A"), ord(start[0]) + 1, step, type=1)
            elif "a" < start[0] <= "z":
                return yield_range(ord('a'), ord(start[0]) + 1, step, type=1)


def getFormTips(form):
    """获取表单错误信息"""
    # forms.forms.NON_FIELD_ERRORS == __all__, 这里获取form里_errors中的__all__(自定义错误字段属性)
    errors = {}
    for key in form.base_fields.keys():
        if key in form._errors:
            errors[key] = form._errors.setdefault(forms.forms.NON_FIELD_ERRORS, ErrorList(error_class=None))
    return errors


def split_tags(tag_string):
    """分离标签集"""
    import re
    res_array = re.split('[,\s]', tag_string)
    return [res for res in res_array if res]


def get_date(date, split_flag='-'):
    """获取日期"""
    try:
        year, month, day = date.split(split_flag)
    except ValueError:
        year, month = date.split(split_flag)
        day = False
    return {
        'year': year,
        'month': month,
        'day': day
    }


def paginate(request, pages, count):
    """pure_pagination分页功能"""
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    if len(pages) > 0:
        p = Paginator(pages, count, request=request)
        return p.page(page)


def get_bread_dict(_id, name):
    return {
        'id': _id,
        'name': name
    }


MSG_DICT = {
    "reset": "重置密码成功",
    "error": "操作非法!"
}