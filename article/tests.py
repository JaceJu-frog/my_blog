from time import sleep

from django.test import TestCase
# 想来还是有意思的,timezone.now()来自django，datetime来自python自带
import datetime

from django.urls import reverse
from django.utils import timezone
from article.models import ArticlePost
from django.contrib.auth.models import User

# Create your tests here.

class ArticlePostModelTests(TestCase):
    def test_was_created_recently_with_future_article(self):
        # 若文章创建时间为未来，返回False
        # 用户给到用户名和密码就行。
        author = User(username='user', password='test_password')
        author.save()

        future_article = ArticlePost(
            author=author,
            title='test',
            content='test',
            created_time=timezone.now() + datetime.timedelta(days=30)
        )

        self.assertIs(future_article.was_created_recently(), False)

    def test_was_created_recently_with_seconds_before_article(self):
        # 若文章创建时间为 1 分钟内，返回 True
        author = User(username='user1', password='test_password')
        author.save()
        seconds_before_article = ArticlePost(
            author=author,
            title='test1',
            content='test1',
            created_time=timezone.now() - datetime.timedelta(seconds=45)
        )
        self.assertIs(seconds_before_article.was_created_recently(), True)

    def test_was_created_recently_with_hours_before_article(self):
        # 若文章创建时间为几小时前，返回 False
        author = User(username='user2', password='test_password')
        author.save()
        hours_before_article = ArticlePost(
            author=author,
            title='test2',
            content='test2',
            created_time=timezone.now() - datetime.timedelta(hours=3)
        )
        self.assertIs(hours_before_article.was_created_recently(), False)

    def test_was_created_recently_with_days_before_article(self):
        # 若文章创建时间为几天前，返回 False
        author = User(username='user3', password='test_password')
        author.save()
        months_before_article = ArticlePost(
            author=author,
            title='test3',
            content='test3',
            created_time=timezone.now() - datetime.timedelta(days=5)
        )
        self.assertIs(months_before_article.was_created_recently(), False)

class ArticlePostViewTests(TestCase):
    def test_increase_view(self):
        # 请求文章详情时，阅读量+1
        author = User(username="user4",password="test_password")
        author.save()
        article = ArticlePost(
            author=author,
            title='test4',
            content='test4',
        )
        article.save()
        self.assertEqual(article.total_views,0)

        url = reverse('article:article_detail',args=(article.id,))
        response=self.client.get(url)
        viewed_article = ArticlePost.objects.get(id=article.id)
        self.assertEqual(viewed_article.total_views,1)

    def test_increase_views_but_not_change_updated_field(self):
        # 请求文章详情时，不改变updated_time.
        # 思路:让程序睡0.5s后请求，如果改变了updated_time字段，是肯定通不过下方
        # updated_time -created_time<0.1的测试的
        author = User(username='user5', password='test_password')
        author.save()
        article = ArticlePost(
            author=author,
            title='test5',
            content='test5',
            )
        article.save()

        sleep(0.5)
        url = reverse('article:article_detail', args=(article.id,))
        response = self.client.get(url)
        viewed_article = ArticlePost.objects.get(id=article.id)
        self.assertIs(viewed_article.updated_time - viewed_article.created_time < timezone.timedelta(seconds=0.1), True)

