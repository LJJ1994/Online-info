import os
import qiniu
from django.conf import settings

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_POST, require_GET

from apps.news.models import NewsCategory
from utils import restful
from .forms import EditNewsCategoryForm, WriteNewsForm
from apps.news.models import News, NewsCategory


@staff_member_required(login_url='index')
def index(request):

    return render(request, 'cms/index.html')


class WriteNewsView(View):
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








