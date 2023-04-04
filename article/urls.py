from django.contrib import admin
from django.urls import include,path
from . import views
from my_blog import urls
from .views import article_list


app_name = 'article'

urlpatterns = [
    path('',views.index,name='index'),
    path('article_list/',views.article_list,name='article_list'),
    path('article_detail/<int:id>/',views.article_detail,name='article_detail'),
    path('article_create/',views.article_create,name='article_create'),
    path('article_delete/<int:id>/',views.article_delete,name='article_delete'),
    path('article_update/<int:id>/',views.article_update,name='article_update'),
    path('increase-likes/<int:id>/',views.IncreaseLikesView.as_view(), name='increase_likes'),
]