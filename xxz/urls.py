"""xxz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


from apps.news import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('search/', include('haystack.urls')), # 全文搜索引擎whoosh
    path('search/', views.search, name='search'), # 普通搜索
    path('cms/', include('apps.cms.urls')),
    path('news/', include('apps.news.urls')),
    path('account/', include('apps.xfzauth.urls')),
    path('course/', include('apps.course.urls')),
    path('payinfo/', include('apps.payinfo.urls')),
    path('ueditor/', include('apps.ueditor.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
