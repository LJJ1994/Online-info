__author__ = 'LJJ'
__date__ = '2019/6/25 上午9:30'

from django.urls import path
from django.conf import settings
from . import views

app_name = 'ueditor'

urlpatterns = [
    path('upload/', views.UploadView.as_view(), name='upload'),
]

if hasattr(settings, 'UEDITOR_UPLOAD_PATH'):
    urlpatterns += [
        path('f/<filename>', views.send_file, name='send_file'),
    ]
