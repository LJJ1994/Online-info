__author__ = 'LJJ'
__date__ = '2019/6/25 下午11:07'

from datetime import datetime
from django import template
from django.utils.timezone import now as now_func, localtime


register = template.Library()


@register.filter
def time_since(value):
    """
    这个函数主要处理time距离现在的时间距离
    1.如果时间间隔小于1分钟以内，那么就显示“刚刚”
    2.如果是大于1分钟小于1小时，那么就显示“xx分钟前”
    3.如果是大于1小时小于24小时，那么就显示“xx小时前”
    4.如果是大于24小时小于30天以内，那么就显示“xx天前”
    5.否则就是显示具体的时间
    :param value: time
    :return: timestamp
    """
    if not isinstance(value, datetime):
        return value

    now = now_func()
    timestamp = (now - value).total_seconds()

    if timestamp < 60:
        return '刚刚'

    elif timestamp >= 60 and timestamp <60*60:
        minutes = int(timestamp/60)
        return '%s分钟前' % minutes

    elif timestamp >= 60*60 and timestamp < 60*60*24:
        hours = int(timestamp/60/60)
        return '%s小时前' % hours

    elif timestamp >= 60*60*24 and timestamp < 60*60*24*30:
        days = int(timestamp/60/60/24)
        return '%s天前' % days

    else:
        return value.strftime('%Y/%m/%d %H:%M')


