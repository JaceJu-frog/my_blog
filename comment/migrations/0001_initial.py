# Generated by Django 4.1.5 on 2023-03-05 07:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("article", "__first__"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ArticleComment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("comment", models.TextField()),
                (
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="article_comment",
                        to="article.articlepost",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        default="AnonymousUser",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="article_comment",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
