# Generated by Django 4.1.5 on 2023-03-05 08:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("article", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("comment", "0002_rename_article_articlecomment_article_related"),
    ]

    operations = [
        migrations.AlterField(
            model_name="articlecomment",
            name="article_related",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="article_comment",
                to="article.articlepost",
            ),
        ),
        migrations.AlterField(
            model_name="articlecomment",
            name="author",
            field=models.ForeignKey(
                blank=True,
                default="AnonymousUser",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="article_comment",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
