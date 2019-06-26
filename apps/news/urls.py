from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('<int:news_id>/', views.news_detail, name='news_detail'),
    path('news_list/', views.news_list, name='news_list'),
    path('news_comment/', views.news_comment, name='news_comment'),
]