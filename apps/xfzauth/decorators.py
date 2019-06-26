__author__ = 'LJJ'
__date__ = '2019/6/27 上午2:04'
from django.shortcuts import redirect
from utils import restful


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
