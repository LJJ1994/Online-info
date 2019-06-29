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
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.http.multipartparser import MultiPartParser

from alipay import AliPay


from .models import Course, CourseOrder
from utils import restful
from apps.xfzauth.decorators import xxz_login_required


def course_index(request):
    """
    获取课程列表页
    :param request:
    :return:
    """
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request, 'course/course_index.html', context=context)


def course_order_completed(request):
    return render(request, 'course/course_order_completed.html')


def course_detail(request, course_id):
    """
    获取某个具体的课程
    :param request: course_id
    :param course_id:
    :return:
    """
    course = Course.objects.get(pk=course_id)
    context = {
        'course': course
    }

    return render(request, 'course/course_detail.html', context=context)


def course_token(request):
    """
    生成前端视频播放所需要的token
    :param request:
    :return: token
    """
    file = request.GET.get('video') # 这里的file是一个完整的视频链接地址
    course_id = request.GET.get('course_id')
    exists = CourseOrder.objects.filter(course_id=course_id, buyer=request.user, status=2).exists()  # 处理用户是否购买课程的逻辑
    if not exists:
        return restful.param_error(message='请先购买该课程!')

    expired_time = int(time.time()) + 2 * 60 * 60
    USER_ID = settings.BAIDU_CLOUD_USER_ID
    USER_KEY = settings.BAIDU_CLOUD_USER_KEY

    # 获取的file的地址url如下
    # file=http://hemvpc6ui1kef2g0dd2.exp.bcevod.com/mda-igjsr8g7z7zqwnav/mda-igjsr8g7z7zqwnav.m3u8
    # 1.获取地址url中的文件名的扩展名
    # 2.去除扩展名，获取文件名
    extension = os.path.splitext(file)[1] # 将文件名和扩展名分离: (filename, extension)
    media_id = file.split('/')[-1].replace(extension, '') # 获取二进制文件名: mda-igjsr8g7z7zqwnav

    # 将user_key编码成utf8格式
    key = USER_KEY.encode('utf-8')
    message = '/{0}/{1}'.format(media_id, expired_time).encode('utf-8')

    # 数字签名
    signature = hmac.new(key, message, digestmod=hashlib.sha256).hexdigest()
    token = '{0}_{1}_{2}'.format(signature, USER_ID, expired_time)

    return restful.result(data={'token': token})


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
def get_qr_code(code_url):
    """
    根据支付宝返回的二维码链接生成二维码图像
    :param code_url:
    :return: code_img
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1
    )

    qr.add_data(code_url)
    img = qr.make_image()
    img.save(os.path.join(settings.MEDIA_ROOT, 'zfb.png'))
    print('保存二维码图片成功!')


# @xxz_login_required
@require_POST
def create_pre_order(request):
    """
    创建预订单
    :param subject: 订单名
    :param out_trade_no: 支付宝交易号,固定
    :param total_amount: 订单金额，浮点数
    :return: 1.创建预订单失败 2.返回二维码code_url
    """
    subject = request.POST.get('goodsname')
    out_trade_no = request.POST.get('orderid')
    total_amount = request.POST.get('price')

    result = init_alipay_obj().api_alipay_trade_precreate(
        subject=subject,
        out_trade_no=out_trade_no,
        total_amount=total_amount
    )
    print('返回值',result)

    code_url = result.get('qr_code')
    if not code_url:
        return restful.param_error(message='预付订单创建失败!')
    else:
        get_qr_code(code_url)
        # 等下在这里测试是否会生成二维码图片，如果生成则返回给前端


@xxz_login_required
def create_order_request(request):
    """向支付宝发起支付请求"""
    out_trade_no  = request.POST.get('orderid')
    total_amount = request.POST.get('price')
    subject = request.POST.get('goodsname')

    alipay_client = init_alipay_obj()
    order_string = alipay_client.api_alipay_trade_page_pay(
        out_trade_no=out_trade_no,
        total_amount=total_amount,
        subject='课程订单%s' % subject,
        return_url='http://localhost:8000/course/course_order_completed/',
        notify_url=None
    )

    alipay_url = settings.ALIPAY_URL + order_string

    return  JsonResponse({'alipay_url': alipay_url})


def order_payment_result(request):
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
    print('签名值:%s' % alipay_sign)

    alipay_client = init_alipay_obj()
    result = True
    if result:
        order_id = alipay_dict.get('out_trade_no')
        trade_no = alipay_dict.get('trade_no')
        CourseOrder.objects.filter(uid=order_id).update(trade_no=trade_no, status=2)
    # result = alipay_client.verify(alipay_dict, alipay_sign)
    return restful.ok()


@xxz_login_required
def course_order(request, course_id):
    """
    课程订单购买页面,请求参数为某个课程的id
    :param request: course_id
    :return:order list 返回订单列表
    """
    course = Course.objects.get(pk=course_id)
    order = CourseOrder.objects.create(course=course, buyer=request.user, amount=course.price, status=1)
    # notify_url = request.build_absolute_uri(reverse('course:notify_view'))
    # return_url = request.build_absolute_uri(reverse('course:course_detail', kwargs={'course_id': course.pk}))

    context = {
        'course': course,
        'order': order,
        # 'notify_url': notify_url,
        # 'return_url': return_url
    }

    return render(request, 'course/course_order.html', context=context)

























# @xxz_login_required
# def course_order_key(request):
#     """
#     获取课程key
#     :param request:
#     :return: key
#     """
#     goodsname = request.POST.get('goodsname')
#     istype = request.POST.get('istype')
#     notify_url = request.POST.get('notify_url')
#     orderid = request.POST.get('orderid')
#     price = request.POST.get('price')
#     return_url = request.POST.get('return_url')
#
#     token = 'e6110f92abcb11040ba153967847b7a6'
#     uid = '49dc532695baa99e16e01bc0'
#     orderuid = str(request.user.pk)
#     key = md5((goodsname + istype + notify_url + orderid + orderuid + price + return_url + token + uid).encode('utf-8')).hexdigest()
#
#     return restful.ok(data={'key': key})


# @csrf_exempt
# def notify_view(request):
#     """
#     通知给自己服务器的视图函数
#     :param request:
#     :return:
#     """
#     orderid = request.POST.get('orderid')
#     CourseOrder.objects.filter(pk=orderid).update(status=2)
#
#     return restful.ok()