"""my_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path,re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
import notifications.urls
from article.views import article_list

urlpatterns = [
    path("",article_list,name="home"),
    path("admin/", admin.site.urls),
    path("article/", include("article.urls",namespace="article")),
    path('userprofile/', include('userprofile.urls',namespace='userprofile')),
    path('comment/', include('comment.urls',namespace='comment')),
    # 这里的notifications.urls没有像之前一样用字符串，是为了确保模块安装到正确的命名空间中。
    path('inbox/notifications',include(notifications.urls,namespace='notifications')),
    # notice
    path('notice/',include('notice.urls',namespace='notice')),
    # allauth的登录，也是一个单独的APP
    path('accounts/', include('allauth.urls')),

    # 部署时使用，让gunicorn知道static和media文件在哪
    re_path(r'^static/(?P<path>.*)$', serve, {"document_root": settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
]

#添加这行为以后上传的图片配置URL路径
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)