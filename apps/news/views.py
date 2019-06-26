from django.shortcuts import render
from django.conf import settings

from .models import News, NewsCategory
from .serializers import NewsSerializers
from utils import restful

def index(request):
    """
    获取首页数据
    :param request:
    :return: index.html
    """
    count = settings.ONE_PAGE_NEWS
    news = News.objects.order_by('-pub_time')[0:count]
    categories = NewsCategory.objects.all()
    context = {
        'news': news,
        'categories': categories
    }
    return render(request, 'news/index.html', context=context)


def news_list(request):
    """
    通过page参数获取每一页的数据
    :param request: ?p=xxx
    :return: data
    """
    p = int(request.GET.get('p', 1))
    start = (p - 1) * settings.ONE_PAGE_NEWS
    end = start + settings.ONE_PAGE_NEWS
    news = News.objects.order_by('-pub_time')[start:end]
    serializer = NewsSerializers(news, many=True)
    serializer_data = serializer.data

    return restful.ok(data=serializer_data)


def news_detail(request, news_id):
    return render(request, 'news/news_detail.html')


def search(request):
    return render(request, 'search/search.html')
