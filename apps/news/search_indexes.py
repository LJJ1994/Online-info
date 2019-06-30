__author__ = 'LJJ'
__date__ = '2019/6/30 上午5:38'

from haystack import indexes
from .models import News


class SearchIndexes(indexes.SearchIndex, indexes.Indexable):
    """创建whoosh搜索索引表"""
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return News

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
