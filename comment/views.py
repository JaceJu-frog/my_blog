from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from article.models import ArticlePost

from .models import ArticleComment
from .forms import ArticleCommentForm

from notifications.signals import notify
from django.contrib.auth.models import User


def index(request):
    return HttpResponse("Hello, world. You're at the comment index.")


@login_required(login_url='/userprofile/login/')
# 新增参数 parent_comment_id，用于区分多级评论
# 对一级评论，缺省值None.
def create_article_comment(request, article_id, parent_comment_id=None):
    article = ArticlePost.objects.get(id=article_id)

    # 让用户填表
    if request.method == 'POST':
        comment_form = ArticleCommentForm(data=request.POST)
        if comment_form.is_valid():
            # 通过表单保存一个新评论，并不向数据库提交(若提交了就会出现两个对象)
            # 如果想要在提交前增加更多属性，这是一种常规做法
            comment_form = comment_form.save(commit=False)
            comment_form.article_related = article
            # 评论作者为登录的用户。
            comment_form.author = request.user
            # 二级回复
            if parent_comment_id:
                parent_comment = ArticleComment.objects.get(id=parent_comment_id)
                # 若回复层级超过二级，则转换为二级
                comment_form.parent_id = parent_comment.get_root().id
                # 被回复人
                comment_form.reply_to = parent_comment.author
                comment_form.save()

                # 给父评论的对象发送通知，实际上这段判断用户是否管理员的代码
                # 我不理解为何需要。
                if request.user != parent_comment.author:
                    notify.send(
                        request.user,
                        recipient=parent_comment.author,
                        verb="回复了你",
                        target=article,
                        action_object=comment_form,
                    )
                return JsonResponse({"code": "200 OK", "new_comment_id": comment_form.id})

            comment_form.save()

            if not request.user.is_superuser:
                # "User.objects.filter(is_superuser=1)" 的作用是
                # 从数据库中提取所有是superuser的对象。
                # 这段代码意为用户发表一级评论时给所有管理员发送通知。
                notify.send(
                    request.user,
                    recipient=User.objects.filter(is_superuser=1),
                    target=article,
                    verb='发表了评论',
                    action_object = comment_form,
                )
            # 拼接锚点，这样发表一级评论后，刷新页面，自动跳至刚发的评论。
            redirect_url=article.get_absolute_url()+ "#comment_elem_"+str(comment_form.id)
            return HttpResponseRedirect(redirect_url)
        else:
            return HttpResponse("提交的表单不合法")
    # 通过get方法获取一个评论界面，用在项目中的二级评论
    elif request.method == 'GET':
        comment_form = ArticleCommentForm()
        return render(request, 'comment/reply.html',
                      {'comment_form': comment_form,
                       'article_id': article_id,
                       'parent_comment_id': parent_comment_id})
    # 只允许get和post请求
    else:
        return HttpResponse('只允许get和post请求')
