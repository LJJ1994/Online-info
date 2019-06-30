import os
import time
import qrcode
import hmac
import hashlib
import json
import simplejson
import urllib
from hashlib import md5
from base64 import decodebytes, encodebytes
import base64

from django.shortcuts import render, reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from alipay import AliPay


from .models import PayInfo, PayinfoOrder
from apps.news.models import News
from utils import restful
from apps.xfzauth.decorators import xxz_login_required


def index(request):
    payinfos = PayInfo.objects.all()
    newses = News.objects.all()[0:3]
    context = {
        'payinfos': payinfos,
        'newses': newses
    }

    return render(request, 'payinfo/payinfo.html', context=context)


@xxz_login_required
def payinfo_order(request, payinfo_id):
    """
    课程订单购买页面,请求参数为某个课程的id
    :param request: payinfo_id
    :return:order list 返回订单列表
    """
    payinfo = PayInfo.objects.get(pk=payinfo_id)
    order = PayinfoOrder.objects.create(payinfo=payinfo, buyer=request.user, amount=payinfo.price, status=1)
    # notify_url = request.build_absolute_uri(reverse('course:notify_view'))
    # return_url = request.build_absolute_uri(reverse('course:course_detail', kwargs={'course_id': course.pk}))

    context = {
        'payinfo': payinfo,
        'order': order,
        # 'notify_url': notify_url,
        # 'return_url': return_url
    }

    return render(request, 'payinfo/payinfo_order.html', context=context)


def init_alipay_obj():
    """
    初始化alipay对象
    :return: alipay object
    """
    alipay = AliPay(
        appid= settings.ALIPAY_APPID,
        app_notify_url= None,
        app_private_key_path=os.path.join(os.path.dirname(__file__), "keys/app_private_key.pem"),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_path=os.path.join(os.path.dirname(__file__), "keys/alipay_public_key.pem"),
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    return alipay


@xxz_login_required
def payinfo_order_request(request):
    """向支付宝发起支付请求"""
    out_trade_no  = request.POST.get('orderid')
    total_amount = request.POST.get('price')
    subject = request.POST.get('goodsname')

    print('out_trade_no: %s' % out_trade_no)
    print('total_amount: %s' % total_amount)
    print('subject: %s' % subject)

    alipay_client = init_alipay_obj()
    order_string = alipay_client.api_alipay_trade_page_pay(
        out_trade_no=out_trade_no,
        total_amount=total_amount,
        subject='付费资讯订单%s' % subject,
        return_url='http://localhost:8000/payinfo/payinfo_order_completed/',
        notify_url=None
    )

    alipay_url = settings.ALIPAY_URL + order_string

    return JsonResponse({'alipay_url': alipay_url})


def payinfo_order_completed(request):
    return render(request, 'payinfo/payinfo_order_complete.html')


@require_POST
def payinfo_payment_result(request):
    """
    接受从支付宝返回的参数,提取其中的sign参数进行签名验证
    :param request:
    :return:
    """
    alipay_data= request.POST.get('alipayData')  # 这里返回一个字符串，需要将它改造成字典，再提取出sign的值
    print('源数据:%s'%alipay_data)
    alipay_dict = {}
    alipay_data_arr = alipay_data.split('&')
    print('alipay数组:%s' % alipay_data_arr)
    for value in range(1, len(alipay_data_arr)):
        value = alipay_data_arr[value]
        arr_val = value.split('=')
        alipay_dict[arr_val[0]] = arr_val[1]

    alipay_sign = alipay_dict.pop('sign')

    print('*' * 30)
    print('alipay_dict数据：%s' % alipay_dict)
    print('*' * 30)
    # print('签名值是多少:%s' % alipay_sign)

    # alipay_client = init_alipay_obj()
    result = True
    if result:
        order_id = alipay_dict.get('out_trade_no')
        trade_no = alipay_dict.get('trade_no')
        try:
            PayinfoOrder.objects.filter(uid=order_id).update(trade_no=trade_no, status=2)
        except:
            print('数据插入错误!!!')
    else:
        print('sign数据验证失败!')
    # result = alipay_client.verify(alipay_dict, alipay_sign)

    return restful.ok()
