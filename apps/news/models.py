from django.db import models


class NewsCategory(models.Model):
    """
    新闻分类
    """
    name = models.CharField(max_length=100)


class News(models.Model):
    """
    文章
    """
    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=300)
    content = models.TextField()
    thumbnail = models.URLField()
    pub_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('NewsCategory', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey('xfzauth.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-pub_time']

    def __str__(self):
        return '文章标题为: %s' % self.title


class Comment(models.Model):
    """
    评论
    """
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey('News', on_delete=models.CASCADE, related_name='comment')
    author = models.ForeignKey('xfzauth.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_time']

