import random
from io import BytesIO

from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, reverse
from django.http import JsonResponse, HttpResponse
from django.core.cache import cache
from django.contrib.auth import get_user_model

from .forms import FormLogin, RegisterForm
from utils import restful
from utils.captcha.captcha import Captcha
from utils.yuntongxun.sms import CCP

User = get_user_model()


@require_POST
def login_view(request):
    """
    用户登录逻辑
    :param request:
    :return: json数据
    """
    forms = FormLogin(request.POST)

    if forms.is_valid():
        telephone = forms.cleaned_data.get('telephone')
        password = forms.cleaned_data.get('password')
        remember = forms.cleaned_data.get('remember')
        user = authenticate(request, username=telephone, password=password)

        if user:
            if user.is_active:
                login(request, user)

                if remember:
                    request.session.set_expiry(None)

                else:
                    request.session.set_expiry(0)

                return restful.result(message='登录成功')

            else:
                return restful.un_auth(message='你的账号已经被冻结！', data={})

        else:
            return restful.param_error(message='输入的账号或密码错误', data={})

    else:
        errors = forms.get_errors()
        print(errors)

        return restful.un_auth(message=errors)
        # return JsonResponse({'code':400, 'message': '', 'data': errors})


def logout_view(request):
    """
    用户退出逻辑
    :param request:
    :return:重定向到首页
    """
    logout(request)

    return redirect(reverse('index'))


def img_captcha(request):
    """
    生成4位图片验证码
    :param request:
    :return: img
    """
    text, image = Captcha.gene_code()
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)

    cache.set(text.lower(), text.lower(), 5*60)
    print('图形验证码: %s' % cache.get(text.lower()))

    response = HttpResponse(content_type='image/png')
    response.write(out.read())
    response['Content-length'] = out.tell()

    return response


def sms_captcha(request):
    """
    生成短信验证码
    :param request:
    :return:
    """
    telephone = request.GET.get('telephone')
    sms_code = "%06d" % random.randint(0,999999)
    print('短信验证码： %s' % sms_code)
    cache.set(telephone, sms_code, 5*60)

    print(cache.get(telephone))

    ccp = CCP()
    # result = ccp.send_template_sms(telephone, [sms_code, 5*60], 1)

    return restful.ok(message='短信验证码发送成功!')


@require_POST
def register(request):
    """
    注册逻辑
    :param request:
    :return:
    """
    forms = RegisterForm(request.POST)
    if forms.is_valid():
        telephone = forms.cleaned_data.get('telephone')
        password = forms.cleaned_data.get('password1')
        username = forms.cleaned_data.get('username')

        User.objects.create_user(telephone=telephone, username=username, password=password)
        user = authenticate(telephone=telephone, password=password)
        print('user:--------------->%s' % user)  # 返回的是手机号,而前端用手机号注册
        if user:
            login(request, user)
            return restful.ok(message='注册成功!')
        else:
            return restful.ok(message='注册成功!')

    else:
        error = forms.get_errors()
        return restful.param_error(message=error)
