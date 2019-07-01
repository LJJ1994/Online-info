__author__ = 'LJJ'
__date__ = '2019/6/20 下午10:20'

from django.urls import path
from . import views
from . import course_views
from . import staffs_views

app_name = 'cms'

# 新闻相关的url
urlpatterns = [
    path('', views.index, name='index'),
    path('cms_logout/', views.cms_logout, name='cms_logout'),
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
    path('course_category/', course_views.CourseCategoryView.as_view(), name='course_category'),
    path('add_course_category/', course_views.add_course_category, name='add_course_category'),
    path('delete_course_category/', course_views.delete_course_category, name='delete_course_category'),
    path('edit_course_category/', course_views.edit_course_category, name='edit_course_category'),
    path('course_list/', course_views.CourseListView.as_view(), name='course_list'),
    path('edit_course/', course_views.EditCourseView.as_view(), name='edit_course'),
    path('delete_course/', course_views.delete_course, name='delete_course'),
]

# 员工管理相关的url
urlpatterns += [
    path('staffs/', staffs_views.staffs_views, name='staffs'),
    path('staff_center/', staffs_views.staff, name='staff'),
    path('add_staff/', staffs_views.AddStaffView.as_view(), name='add_staff'),
]