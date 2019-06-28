import os
import time
import hmac
import hashlib
from hashlib import md5
from django.shortcuts import render, reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
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


@xxz_login_required
def course_order(request, course_id):
    """
    课程订单,请求参数为某个课程的id
    :param request: course_id
    :return:order list 返回订单列表
    """
    course = Course.objects.get(pk=course_id)
    order = CourseOrder.objects.create(course=course, buyer=request.user, amount=course.price, status=1)
    notify_url = request.build_absolute_uri(reverse('course:notify_view'))
    return_url = request.build_absolute_uri(reverse('course:course_detail', kwargs={'course_id': course.pk}))
    context = {
        'course': course,
        'order': order,
        'notify_url': notify_url,
        'return_url': return_url
    }

    return render(request, 'course/course_order.html', context=context)


@xxz_login_required
def course_order_key(request):
    """
    获取课程key
    :param request:
    :return: key
    """
    goodsname = request.POST.get('goodsname')
    istype = request.POST.get('istype')
    notify_url = request.POST.get('notify_url')
    orderid = request.POST.get('orderid')
    price = request.POST.get('price')
    return_url = request.POST.get('return_url')

    token = 'e6110f92abcb11040ba153967847b7a6'
    uid = '49dc532695baa99e16e01bc0'
    orderuid = str(request.user.pk)
    key = md5((goodsname + istype + notify_url + orderid + orderuid + price + return_url + token + uid).encode('utf-8')).hexdigest()

    return restful.ok(data={'key': key})


@csrf_exempt
def notify_view(request):
    """
    通知给自己服务器的视图函数
    :param request:
    :return:
    """
    orderid = request.POST.get('orderid')
    CourseOrder.objects.filter(pk=orderid).update(status=2)

    return restful.ok()