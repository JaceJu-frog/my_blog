from django.db import models
# 导入内建的User模型
from django.contrib.auth.models import User
from article.models import ArticlePost


class ArticleComment(models.Model):
    """评论"""
    # 评论由外键连接唯一的作者
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="article_comment", blank=True,null=True,default="AnonymousUser")
    # 评论由外键连接唯一的文章
    article_related = models.ForeignKey(ArticlePost,
                                        on_delete=models.CASCADE,
                                        blank=True,null=True,related_name="article_comment")
    # 保存评论的大量文本使用TextField
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('created',)
    def __str__(self):
        return self.comment[:20]