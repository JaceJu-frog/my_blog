from django.db import models
#导入内建的User模型
from django.contrib.auth.models import User

#timezone用于处理时间相关事务
from django.utils import timezone

# 博客文章的数据模型


class ArticlePost(models.Model):
    # 文章作者。参数 on_delete用于指定数据删除的方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Django具有一个简单的账号系统（User），满足一般网站的用户相关的基本功能。

    # 设置文章浏览量，初始值为0.
    total_views = models.PositiveIntegerField(default=0)

    # 文章标题.models.CharField为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=200)

    # 文章正文。保存大量文本使用TextField
    content = models.TextField()

    # 文章的创建时间。参数 default=timezone.now()指定创建文章时将默认写入当前的时间
    created_time = models.DateTimeField(default=timezone.now)

    # 文章更新时间。 参数 auto_now=True指定每次更新数据时自动写入当前时间
    updated_time = models.DateTimeField(auto_now=True)

    class Meta: # class Meta提供元数据，也就是内部数据，这些信息不是某篇文章私有，而是整张表的共同行为。
        # ordering 指定模型返回的数据的排列顺序
        # "-created_time"表示返回数据应以创建时间倒序排列
        ordering = ('-created_time',)
        # 注意ordering是元组，括号中只含一个元素时不要忘记末尾的逗号。

    def __str__(self):
        # __str__方法定义了需要表示数据时应该显示的名称。
        # return self.title 将文章标题返回
        return self.title
