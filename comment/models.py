from django.db import models
# 导入内建的User模型
from django.contrib.auth.models import User
from article.models import ArticlePost
from ckeditor.fields import RichTextField


class ArticleComment(models.Model):
    """评论"""
    # 评论由外键连接唯一的作者
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="article_comment", blank=True,null=True)
    # 评论由外键连接唯一的文章
    article_related = models.ForeignKey(ArticlePost,
                                        on_delete=models.CASCADE,
                                        blank=True,null=True,related_name="article_comment")
    # 保存评论的大量文本使用TextField
    # 但是此处引入富文本插件ckeditor,改成RichTextField
    comment = RichTextField(blank=True,config_name='default')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('created',)
    def __str__(self):
        return self.comment[:20]