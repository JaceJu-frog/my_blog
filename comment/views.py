from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import ArticleComment
from .forms import ArticleCommentForm


def index(request):
    return HttpResponse("Hello, world. You're at the comment index.")


def create_article_comment(request, article_id):
    # 让用户填表
    if request.method == 'POST':
        print(request.POST)
        comment_form = ArticleCommentForm(data=request.POST)
        if comment_form.is_valid():
            # 通过表单保存一个新评论，并不向数据库提交(若提交了就会出现两个对象)
            # 如果想要在提交前增加更多属性，这是一种常规做法
            comment_form = comment_form.save(commit=False)
            # 如果用户登录则评论作者为登录的用户，否则已经在models.py中默认为匿名。
            if request.user:
                comment_form.author = request.user
            comment_form.save()
            return HttpResponseRedirect(reverse("article:article_detail", kwargs={'id': article_id}))

    elif request.method == 'GET':
        comment_form = ArticleCommentForm()
        return render(request, 'comment/create_article_comment.html',
                      {'comment_form': comment_form, 'article_id': article_id})
    else:
        return HttpResponse('只允许get和post请求')
