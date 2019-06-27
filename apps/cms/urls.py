__author__ = 'LJJ'
__date__ = '2019/6/20 下午10:20'

from django.urls import path
from . import views
from . import course_views

app_name = 'cms'

# 新闻相关的url
urlpatterns = [
    path('', views.index, name='index'),
    path('write_news/', views.WriteNewsView.as_view(), name='write_news'),
    path('edit_news/', views.EditNewsView.as_view(), name='edit_news'),
    path('delete_news/', views.delete_news, name='delete_news'),
    path('news_list/', views.NewsListView.as_view(), name='news_list'),
    path('news_category/', views.news_category, name='news_category'),
    path('add_news_category/', views.add_news_category, name='add_news_category'),
    path('edit_news_category/', views.edit_news_category, name='edit_news_category'),
    path('delete_news_category/', views.delete_news_category, name='delete_news_category'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('qn_token/', views.qn_token, name='qn_token'),
]


# 课程相关的url
urlpatterns += [
    path('pub_course/', course_views.PublicCourseView.as_view(), name='pub_course'),
]