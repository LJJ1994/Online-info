from django.shortcuts import render
from django.conf import settings
from django.views.decorators.http import require_GET, require_POST

from .models import News, NewsCategory, Comment
from .forms import CommentForm
from .serializers import NewsSerializers, CommentSerializers
from utils import restful
from apps.xfzauth.decorators import xxz_login_required


def index(request):
    """
    当加载首页时获取的新闻数据
    :param request:
    :return: index.html
    """
    count = settings.ONE_PAGE_NEWS
    news = News.objects.select_related('category', 'author').order_by('-pub_time')[0:count]
    categories = NewsCategory.objects.all()
    context = {
        'newses': news,
        'categories': categories
    }

    return render(request, 'news/index.html', context=context)


def news_list(request):
    """
    通过page和category_id参数获取每一页的数据,默认获取所有分类的数据的1页
    :param request: ?p=xxx&&category_id=xx
    :return: news list
    """
    p = int(request.GET.get('p', 1))
    category_id = int(request.GET.get('category_id', 0))
    start = (p - 1) * settings.ONE_PAGE_NEWS
    end = start + settings.ONE_PAGE_NEWS

    if category_id == 0:
        news = News.objects.select_related('category', 'author').all()[start:end]
    else:
        news = News.objects.select_related('author', 'category').filter(category__id=category_id)[start:end]

    serializer = NewsSerializers(news, many=True)
    serializer_data = serializer.data

    return restful.ok(data=serializer_data)


def news_detail(request, news_id):
    """
    通过news_id获取某个文章
    :param request: news_id
    :return: news
    """
    news = News.objects.select_related('author', 'category').prefetch_related('comment__author').get(pk=news_id)
    context = {
        'news': news
    }

    return render(request, 'news/news_detail.html', context=context)


@xxz_login_required
def news_comment(request):
    """
    获取某条新闻的评论
    :param request:news_id, comment
    :return: comment
    """
    forms = CommentForm(request.POST)
    if forms.is_valid():
        news_id = forms.cleaned_data.get('news_id')
        content = forms.cleaned_data.get('content')
        news = News.objects.get(pk=news_id)

        comment = Comment.objects.create(content=content, author=request.user, news=news)
        serializer = CommentSerializers(comment)
        data = serializer.data

        return restful.result(data=data)
    else:
        return restful.param_error(message="请填写评论信息!")


def search(request):

    return render(request, 'search/search.html')
