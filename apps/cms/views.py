import os
import qiniu
from urllib import parse
from datetime import datetime

from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_POST, require_GET
from django.core.paginator import Paginator
from django.utils.timezone import make_aware
from django.contrib.auth import logout

from apps.news.models import NewsCategory
from utils import restful
from .forms import EditNewsCategoryForm, WriteNewsForm, EditNewsForm
from apps.news.models import News, NewsCategory


@staff_member_required(login_url='index')
def index(request):

    return render(request, 'cms/index.html')


@staff_member_required(login_url='index')
def cms_logout(request):
    """
    cms后台用户登出
    :param request:
    :return:
    """
    try:
        logout(request)
        return redirect(reverse('news:index'))
    except:
        return restful.param_error(message='退出失败!')


class NewsListView(View):
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
        category_id = int(request.GET.get('category', 0) or 0)

        newses = News.objects.all()

        if start or end:
            if start:
                start_date = datetime.strptime(start, '%Y/%m/%d')
            else:
                start_date = datetime(year=2019,month=6,day=1)

            if end:
                end_date = datetime.strptime(end, '%Y/%m/%d')
            else:
                end_date = datetime.today()
            newses = newses.filter(pub_time__range=(make_aware(start_date), make_aware(end_date)))

        if title:
            newses = newses.filter(title__icontains=title)

        if category_id:
            newses = newses.filter(category=category_id)

        paginator = Paginator(newses, 2)
        page_obj = paginator.page(page)

        context_data = self.get_paginator_data(paginator, page_obj)

        context = {
            'categories': NewsCategory.objects.all(),
            'newses': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,
            'start': start,
            'end': end,
            'title': title,
            'category_id': category_id,
            'url_query': '&' + parse.urlencode({
                'start': start or '',
                'end': end or '',
                'title': title or '',
                'category': category_id or ''
            })
        }

        print('#'*30)
        print(context['url_query'])
        context.update(context_data)

        return render(request, 'cms/news_list.html', context=context)

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


class EditNewsView(View):
    """
    编辑新闻类视图
    """
    def get(self, request):
        news_id = request.GET.get('news_id')
        news = News.objects.get(pk=news_id)
        context = {
            'news': news,
            'categories': NewsCategory.objects.all()
        }

        return render(request, 'cms/write_news.html', context=context)

    def post(self, request):
        forms = EditNewsForm(request.POST)
        if forms.is_valid():
            title = forms.cleaned_data.get('title')
            desc = forms.cleaned_data.get('desc')
            thumbnail = forms.cleaned_data.get('thumbnail')
            content = forms.cleaned_data.get('content')
            category_id = forms.cleaned_data.get('category')  # 这里的category前端发送过来的是一个数字类型的id
            category = NewsCategory.objects.get(pk=category_id)
            pk = forms.cleaned_data.get('pk') # 某个新闻的主键
            News.objects.filter(pk=pk).update(title=title, content=content, desc=desc, thumbnail=thumbnail, category=category)

            return restful.ok(message='文章编辑成功!')
        else:
            return restful.param_error(message="表单验证失败!")


@require_POST
def delete_news(request):
    """
    删除某篇新闻
    :param request: news_id
    :return:
    """
    news_id = request.POST.get('news_id')
    news = News.objects.filter(pk=news_id)
    news.delete()

    return restful.ok(message='新闻删除成功!')


class WriteNewsView(View):
    """
    编写新闻类视图
    """
    def get(self, request):
        categories = NewsCategory.objects.all()
        context = {
            'categories': categories
        }

        return render(request, 'cms/write_news.html', context=context)

    def post(self, request):
        forms = WriteNewsForm(request.POST)
        if forms.is_valid():
            title = forms.cleaned_data.get('title')
            desc = forms.cleaned_data.get('desc')
            content = forms.cleaned_data.get('content')
            thumbnail = forms.cleaned_data.get('thumbnail')
            category_id = forms.cleaned_data.get('category')
            category = NewsCategory.objects.get(pk=category_id)
            News.objects.create(title=title, desc=desc, content=content,
                                author=request.user, category=category, thumbnail=thumbnail)

            return restful.ok()
        else:
            return restful.param_error(message='请求参数错误!')


@require_GET
def news_category(request):
    categories = NewsCategory.objects.all()
    context = {
        'categories': categories
    }

    return render(request, 'cms/category_news.html', context=context)


@require_POST
def add_news_category(request):
    """
    添加新闻分类
    :param request: name
    :return: ok
    """
    name = request.POST.get('name')
    exists = NewsCategory.objects.filter(name=name).exists()

    if not exists:
        NewsCategory.objects.create(name=name)

        return restful.ok(message='创建新闻分类成功!')
    else:
        return restful.param_error(message='该新闻分类已存在!')


@require_POST
def edit_news_category(request):
    """
    编辑新闻分类
    :param request: pk, name
    :return:
    """
    forms = EditNewsCategoryForm(request.POST)

    if forms.is_valid():
        pk = forms.cleaned_data.get('pk')
        name = forms.cleaned_data.get('name')

        try:
            NewsCategory.objects.filter(pk=pk).update(name=name)
            return restful.ok(message='编辑成功!')
        except:
            return restful.param_error(message='要编辑的分类不存在!')

    else:
        return restful.param_error(message=forms.get_errors())


@require_POST
def delete_news_category(request):
    """
    删除新闻分类
    :param request:pk
    :return:
    """
    pk = request.POST.get('pk')
    try:
        NewsCategory.objects.filter(pk=pk).delete()
        return restful.ok(message='删除成功!')
    except:
        return restful.param_error(message='要删除的新闻不存在!')


@require_POST
def upload_file(request):
    """
    上传缩略图
    :param request: file
    :return: file
    """
    file = request.FILES.get('file')
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT, name), 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)

    url = request.build_absolute_uri(settings.MEDIA_URL+name)
    return restful.result(data={'url': url})


@require_GET
def qn_token(request):
    """
    生成七牛云token
    :param request:
    :return: token
    """
    access_key = settings.QINIU_ACCESS_KEY
    secret_key = settings.QINIU_SECRET_KEY
    bucket = settings.QINIU_BUCKET_NAME

    q = qiniu.Auth(access_key, secret_key)
    token = q.upload_token(bucket)

    return restful.ok(data={'token': token})








