from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from article.models import ArticlePost


# Create your views here.

class CommentNoticeListView(LoginRequiredMixin,ListView):
    """展示通知列表"""
    # 上下文的名称
    context_object_name ='notices'

    # 模板位置
    template_name = 'notice/list.html'
    # 登录重定向
    # 来自混合功能类LoginRequiredMixin
    login_url = '/userprofile/login'

    def get_queryset(self):
        # 别管pycharm报错，这个能用。
        return self.request.user.notifications.unread()

class CommentNoticeUpdateView(View):
    """更新通知状态"""
    # 处理get请求
    def get(self,request):
        # 获取未读消息
        notice_id=request.GET.get('notice_id')
        # 更新单条通知
        # 页面中，点进去就会消失啦
        if notice_id:
            article = ArticlePost.objects.get(id=request.GET.get('article_id'))
            # print(article_id)
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect(article)
        # 更新全部通知
        else:
            # mark_all_as_read和mark_as_read都是View这个类自带的方法。
            request.user.notifications.mark_all_as_read()
            return redirect('notice:list')