from django.db import models
# 导入内建的User模型
from django.contrib.auth.models import User
from django.urls import reverse

# timezone用于处理时间相关事务
from django.utils import timezone
# 一个处理多对多关系的管理器：
from taggit.managers import TaggableManager
# 导入pillow库处理标题图
from PIL import Image


# 博客文章分栏
class ArticleColumn(models.Model):
    title = models.CharField(max_length=200)
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # __str__方法定义了需要表示数据时应该显示的名称。
        # return self.title 将文章标题返回
        return self.title


# 博客文章的数据模型
class ArticlePost(models.Model):
    # 文章作者。参数 on_delete用于指定数据删除的方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Django具有一个简单的账号系统（User），满足一般网站的用户相关的基本功能。

    # 文章所属栏目
    column = models.ForeignKey(ArticleColumn, on_delete=models.CASCADE, null=True, blank=True, related_name="articles")
    # 文章标签
    tags = TaggableManager(blank=True)

    # 设置文章浏览量，初始值为0.
    total_views = models.PositiveIntegerField(default=0)

    # 文章标题.models.CharField为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=200)

    # 文章标题图
    avatar = models.ImageField(upload_to='article/%Y%m%d', blank=True, null=True)

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])

    # 重载save()函数
    def save(self, *args, **kwargs):
        # 调用父类(models.Model)的save()功能
        # 即将model中的字段数据保存到数据库中，这里如果有图片也会保存，之后的修改基于已经保存过的图片。
        article = super(ArticlePost, self).save(*args, **kwargs)

        # 上方代码刚刚保存图片进数据库，现在基于它修改，
        # 固定宽度缩放图片大小
        if self.avatar and not kwargs.get('update_fields'):
            img = Image.open(self.avatar.path)
            (x, y) = img.size
            new_x = 400
            new_y = int(new_x * (y / x))
            # Image.ANTIALIAS表示缩放采用平滑滤波。
            img = img.resize((new_x, new_y), Image.ANTIALIAS)
            img.save(self.avatar.path)
        # 最后一步，将父类save()
        # 返回的结果原封不动的返回去。
        return article

    # 文章正文。保存大量文本使用TextField
    content = models.TextField()

    # 文章的创建时间。参数 default=timezone.now()指定创建文章时将默认写入当前的时间
    created_time = models.DateTimeField(default=timezone.now)

    # 文章更新时间。 参数 auto_now=True指定每次更新数据时自动写入当前时间
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:  # class Meta提供元数据，也就是内部数据，这些信息不是某篇文章私有，而是整张表的共同行为。
        # ordering 指定模型返回的数据的排列顺序
        # "-created_time"表示返回数据应以创建时间倒序排列
        ordering = ('-created_time',)
        # 注意ordering是元组，括号中只含一个元素时不要忘记末尾的逗号。

    def __str__(self):
        # __str__方法定义了需要表示数据时应该显示的名称。
        # return self.title 将文章标题返回
        return self.title
