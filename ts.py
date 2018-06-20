# -*- coding:utf-8 -*-
import re
import time

from datetime import date
from datetime import datetime
from collections import abc

__author__ = 'KoiSato'


def split_tags(tag_string):
    import re
    res_array = re.split('[,\s]', tag_string)
    return [res for res in res_array if res]


def get_date(date):
    try:
        year, month, day = date.split('-')
    except ValueError:
        year, month = date.split('-')
        day = None
    return {
        'year': year,
        'month': month,
        'day': day
    }


if __name__ == '__main__':
    # res = re.match(r'^(\w+[,\s])*java((,|\s+|,\s+)\w+)*$', 'python,java')
    # print(res)
    today = datetime.today()
    time.sleep(3)
    print((datetime.today() - today).days)
    # List = [1, 2]
    # try:
    #     print(List[int('3.')])
    # except (ValueError, IndexError):
    #     print(1)
    # print(isinstance(1, abc.Iterable))
    # print(get_date('2018-06'))
    # print(datetime.now().year)
    # print(date.today().year)
    # print(date.today())
    # result = re.split('java', "python,   java,jek    ,ad sad")
    # new = [split_tags(res) for res in result if res]
    # print(','.join([tag for tags in new for tag in tags]))
