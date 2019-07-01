__author__ = 'LJJ'
__date__ = '2019/6/27 上午2:04'

import functools
from django.shortcuts import redirect
from django.http import Http404

from utils import restful


# 用户必须登录的装饰器
def xxz_login_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return restful.un_auth(message='请先登录!')
            else:
                return redirect('/')

    return wrapper


# 要求该用户必须是超级管理员的装饰器
def xxz_superuser_required(func):
    # 这个工具函数保留传入函数func的所有参数
    @functools.wraps(func)
    def decorator(request, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            raise Http404()
    return decorator
