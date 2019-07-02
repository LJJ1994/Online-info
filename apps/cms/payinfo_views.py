__author__ = 'LJJ'
__date__ = '2019/7/2 下午12:23'
import os
import qiniu
from urllib import parse
from datetime import datetime

from django.conf import settings
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import View
from django.core.paginator import Paginator
from django.utils.timezone import make_aware

from apps.payinfo.models import PayInfo
from apps.xfzauth.decorators import xxz_login_required
from utils import restful
from .forms import UploadFileForm


class PayinfoListView(View):
    def get(self, request):
        """
        通过p获取分页数据
        :param request:?p=xxx
        :return: data
        """
        page = int(request.GET.get('p',1))
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')

        payinfoes = PayInfo.objects.all()

        if start or end:
            if start:
                start_date = datetime.strptime(start, '%Y/%m/%d')
            else:
                start_date = datetime(year=2019,month=6,day=1)

            if end:
                end_date = datetime.strptime(end, '%Y/%m/%d')
            else:
                end_date = datetime.today()
            payinfoes = payinfoes.filter(pub_time__range=(make_aware(start_date), make_aware(end_date)))

        if title:
            payinfoes = payinfoes.filter(title__icontains=title)

        paginator = Paginator(payinfoes, 2)
        page_obj = paginator.page(page)

        context_data = self.get_paginator_data(paginator, page_obj)

        context = {
            'payinfoes': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,
            'start': start,
            'end': end,
            'title': title,
            'url_query': '&' + parse.urlencode({
                'start': start or '',
                'end': end or '',
                'title': title or '',
            })
        }

        print('#'*30)
        print(context['url_query'])
        context.update(context_data)

        return render(request, 'cms/payinfo_list.html', context=context)

    def get_paginator_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count -1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

        return {
            'left_pages': left_pages,
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }


class EditPayinfoView(View):
    """
    编辑资讯付费类视图
    """
    def get(self, request):
        payinfo_id = int(request.GET.get('payinfo_id'))
        payinfo = PayInfo.objects.get(pk=payinfo_id)
        context = {
            'payinfo': payinfo
        }

        return render(request, 'cms/pub_payinfo.html', context=context)

    def post(self, request):
        title = request.POST.get('title')
        profile = request.POST.get('profile')
        price = request.POST.get('price')
        file = request.POST.get('file_path')
        pk = int(request.POST.get('pk')) # 某个资讯的主键

        try:
            PayInfo.objects.filter(pk=pk).update(title=title, profile=profile, price=price, file=file)
            return restful.ok(message='资讯编辑成功!')
        except:
            return restful.param_error(message="该资讯不存在或参数错误!")


class WritePayinfoView(View):
    """
    编写付费资讯类视图
    """
    def get(self, request):
        return render(request, 'cms/pub_payinfo.html')

    def post(self, request):

        title = request.POST.get('title')
        profile = request.POST.get('profile')
        price = request.POST.get('price')
        file = request.POST.get('file_path')

        try:
            PayInfo.objects.create(title=title, file=file, profile=profile, price=price)
            return restful.ok(message='创建付费资讯文章成功!')
        except PayInfo.DoesNotExist:
            return restful.param_error(message='请求参数错误!')


@require_POST
def delete_payinfo(request):
    """
    删除某篇付费资讯
    :param request: news_id
    :return:
    """
    payinfo_id = request.POST.get('payinfo_id')
    payinfo = PayInfo.objects.filter(pk=payinfo_id)
    payinfo.delete()

    return restful.ok(message='付费资讯删除成功!')