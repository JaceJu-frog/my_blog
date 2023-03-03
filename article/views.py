# 通过render函数，从模板生成网页;redirect重定向
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse

# 导入数据模型ArticlePost
from .models import ArticlePost
# 导入markdown2html的库
import markdown

from django.http import HttpResponse, HttpResponseRedirect

from .forms import ArticlePostForm


def index(request):
    return HttpResponse("Hello, world. You're at the article index.")


def article_list(request):
    # 取出博客所有文章
    articles = ArticlePost.objects.all()
    # render函数：载入模板，并返回context对象
    return render(request, 'article/article_list.html', context={"articles": articles})


def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)

    # 将content中markdown语法渲染成html样式
    article.content = markdown.markdown(article.content,
                                     extensions=[
                                         # 包含 缩写、表格等常用扩展
                                         'markdown.extensions.extra',
                                         # 语法高亮扩展
                                         'markdown.extensions.codehilite',
                                     ])
    # 需要传递给模板的对象，虽然上面的语句改变了article.content，但是context依然传入article就好。
    context = {'article': article}
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)

def article_create(request):
    # 判断用户是否提交数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        print(article_post_form.is_valid()) #False
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中。
            new_article_post = article_post_form.save(commit=False)

            # 暂时先指定数据库中id=1的用户为作者
            new_article_post.author = User.objects.get(id=1)
            # 将新文章保存到数据库中
            print(new_article_post.author)
            new_article_post.save()
            # 完成后返回到文章列表
            return HttpResponseRedirect(reverse("article:article_list"))
        # 如果数据不合法，返回错误信息

    #如果用户是get方法请求数据
    else:
        # 创建表单类实例
        article_post_form= ArticlePostForm()
        # 赋值上下文
        context = {'article_post_form':article_post_form}
        return render(request, 'article/article_create.html',context=context)

def article_delete(request, id):
    # 以POST形式，否则别人用get可以直接删除
    if request.method == 'POST':
        # 取出相应的文章
        article = ArticlePost.objects.get(id=id)
        # 将文章从数据库中删除
        article.delete()
        # 完成后返回到文章列表
        return HttpResponseRedirect(reverse("article:article_list"))
    else:
        return HttpResponse("仅允许post请求")

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
        article_post_form = ArticlePostForm(data=request.POST,instance=article)

        # 判断提交的数据是否符合表单的要求
        if article_post_form.is_valid():
            # 通过表单保存一篇新文章，并不向数据库提交(若提交了就会出现两个对象)
            # 如果想要在提交前增加更多属性，这是一种常规做法
            article_post_form = article_post_form.save(commit=False)

            # 暂时先指定数据库中id=1的用户为作者，并调用save()方法保存
            article_post_form.author = User.objects.get(id=1)
            article_post_form.save()
            # 完成后返回到这篇文章
            return HttpResponseRedirect(reverse("article:article_detail",kwargs={'id': id}))
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse(article_post_form.errors)

    #如果用户是get方法请求数据，也就是通过"修改文章"按钮访问此页面
    else:
        # 赋值上下文
        context = {'article':article}
        # 将响应返回到模板中
        return render(request, 'article/article_update.html',context=context)
