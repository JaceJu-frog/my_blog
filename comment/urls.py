# 博文id + 评论id
from django.urls import path
from . import views

app_name = 'comment'

urlpatterns=[
    path('',views.index,name='index'),
    path('article/<int:article_id>',views.create_article_comment,name='create_article_comment'),
]