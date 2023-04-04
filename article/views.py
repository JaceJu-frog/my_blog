# @login提示登录，用在修改文章
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# 通过render函数，从模板生成网页;redirect重定向
from django.shortcuts import render
from django.urls import reverse

# 导入数据模型ArticlePost
from .models import ArticlePost, ArticleColumn
# 导入markdown2html的库
import markdown

from django.http import HttpResponse, HttpResponseRedirect

from .forms import ArticlePostForm

# 引入分页
from django.core.paginator import Paginator

from comment.forms import ArticleCommentForm

#类视图
from django.views import View


def index(request):
    return HttpResponse("Hello, world. You're at the article index.")


def article_list(request):
    # 如果search 不存在会设置为None
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    print(column)
    tag = request.GET.get('tag')

    # 初始化查询集
    article_listing = ArticlePost.objects.all()
    # 按搜索
    if search:
        # 引入 Q 对象完成联合搜索
        from django.db.models import Q
        # 注意Q对象，Q(title__icontains=search)
        # 意思是在模型的title字段查询，icontains是不区分大小写的包含，中间用两个下划线隔开。
        # contains 区分大小写
        article_listing = article_listing.filter(Q(content__icontains=search) |
                                                 Q(title__icontains=search))

    else:
        # 将 search 参数重置为空
        search = ''

    # 栏目查询集
    if column is not None and column.isdigit(): # isdigit()表示非负整数，因为这里是外键
        print("开始按栏目排序")
        article_listing = article_listing.filter(column=column)
    else:
        column = ''

    # 标签查询集
    # Django-taggit中标签过滤的写法：
    # filter(tags__name__in=[tag])，
    # 赋值的字符串tag用方括号包起来。
    # 因为django-taggit多标签联合查询时，代码为
    # Model.objects.filter(tags__name__in=["tag1", "tag2"])
    if tag and tag != 'None':
        article_listing = article_listing.filter(tags__name__in=[tag])

    # 查询集最后的排序，如果要求“最热”，则取出的文章按浏览量排列
    if order == 'hot':
        # - 表示倒序
        article_listing = article_listing.order_by("-total_views")

    # 引入paginator，每页1篇
    article_paginator = Paginator(article_listing, 3)
    # 网页展示为.../?page=1,get是用于获取页码的

    page_number = request.GET.get('page')
    # 将导航对象相应的页码内容返回，获取articles
    # 一些针对page_number的纠错paginator自己就有，不必多此一举。
    articles = article_paginator.get_page(page_number)

    # 在视图中通过Paginator类，给传递给模板的内容做了手脚：
    # 返回的不再是所有文章的集合，而是对应页码的部分文章的对象，并且这个对象还包含了分页的方法。
    return render(request, 'article/article_list.html',
                  context={"articles": articles,
                           'order': order,
                           'search': search,
                           'column': column})


def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)
    # 每次访问增加1的浏览量
    article.total_views += 1
    article.save(update_fields=['total_views'])
    # 将content中markdown语法渲染成html样式
    md = markdown.Markdown(extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        # 目录扩展
        'markdown.extensions.toc',
    ])
    article.content = md.convert(article.content)

    article_comments = article.article_comment.all()
    # 需要传递给模板的对象，虽然上面的语句改变了article.content，但是context中依然传入article就好。
    # 此外md.toc 算是个html对象，传入markdown的标题结构。
    # 第三，为了在评论中使用富文本，将评论的表单传到文章详情页面中

    article_comment_form = ArticleCommentForm()
    # print(article_comment_form)
    # print(article_comment_form.author)
    # 传入文章，大纲，评论，新建评论所用表单
    context = {'article': article, 'toc': md.toc, 'article_comments': article_comments,
               'article_comment_form':article_comment_form}
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)


@login_required(login_url='/accounts/login/')  # 需要登录
def article_create(request):
    # 判断用户是否提交数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        # 包括标题图，所以给了个file
        article_post_form = ArticlePostForm(data=request.POST, files=request.FILES)
        print(article_post_form.is_valid())  # False
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中。
            new_article_post = article_post_form.save(commit=False)

            # 指定目前登录的用户为作者
            new_article_post.author = request.user
            # 将新文章保存到数据库中
            print(new_article_post.author)
            new_article_post.save()

            # 保存 tags 的多对多关系
            article_post_form.save_m2m()
            # 完成后返回到文章列表
            return HttpResponseRedirect(reverse("article:article_list"))
        # 如果数据不合法，返回错误信息

    # 如果用户是get方法请求数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文,提交的表单和栏目
        columns = ArticleColumn.objects.all()
        context = {'article_post_form': article_post_form, 'columns': columns}
        return render(request, 'article/article_create.html', context=context)


@login_required(login_url='/accounts/login/')
def article_delete(request, id):
    # 以POST形式，否则别人用get可以直接删除
    if request.method == 'POST':
        # 取出相应的文章
        article = ArticlePost.objects.get(id=id)
        if request.user == article.author:
            # 将文章从数据库中删除
            article.delete()
            # 完成后返回到文章列表
            return HttpResponseRedirect(reverse("article:article_list"))
        else:
            return HttpResponse("只有作者才能删除")
    else:
        return HttpResponse("仅允许post请求")


@login_required(login_url='/accounts/login/')
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新title、content字段
    GET方法进入初始表单页面
    id:文章的id
    """

    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)

    # 判断用户是否为POST提交表单数据
    if request.method == 'POST':
        # 创建表单来修改现有的article,data是POST方法传入的参数，用于更新表单。
        # instance让表单基于这篇文章操作，没有instance=article,就会新建一个对象！！我的五六篇文章就是这么得来的。
        article_post_form = ArticlePostForm(data=request.POST, files=request.FILES, instance=article)
        print(request.FILES)
        # 判断提交的数据是否符合表单的要求
        if article_post_form.is_valid():

            # 指定目前登录的用户为作者
            article_post_form.author = request.user

            # 指定标题图，如果有的话
            if request.FILES.get('avatar'):
                article_post_form.avatar = request.FILES.get('avatar')
                print(article_post_form.avatar)
            # 通过表单保存一篇新文章，并不向数据库提交(若提交了就会出现两个对象)
            # 如果想要在提交前增加更多属性，这是一种常规做法
            article_post_form = article_post_form.save(commit=False)
            # 指定标签，如果有的话
            if request.POST.get('tags'):
                article_post_form.tags.set(request.POST.get('tags').split(','), clear=True)
            else:
                article_post_form.tags.clear()
            article_post_form.save()
            # 完成后返回到这篇文章
            return HttpResponseRedirect(reverse("article:article_detail", kwargs={'id': id}))
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse(article_post_form.errors)

    # 如果用户是get方法请求数据，也就是通过"修改文章"按钮访问此页面
    else:
        # 只有作者本人才能修改
        if article.author == request.user:
            # 赋值上下文,提交的表单和栏目
            columns = ArticleColumn.objects.all()
            # 调用官方接口将文章的tags放进页面
            context = {'article': article, 'columns': columns,
                       'tags': ','.join([x for x in article.tags.names()]) or ""}
            # 将响应返回到模板中
            return render(request, 'article/article_update.html', context=context)
        # 将get模块也设计得有些复杂，是防止坏用户直接猜到链接输入。
        else:
            return HttpResponse("只有作者才能修改")

# 类视图的点赞
# 点赞数 +1
class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = ArticlePost.objects.get(id=kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('success')
        