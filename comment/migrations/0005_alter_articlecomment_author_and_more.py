# Generated by Django 4.1.5 on 2023-03-11 05:34

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("comment", "0004_alter_articlecomment_options_articlecomment_created"),
    ]

    operations = [
        migrations.AlterField(
            model_name="articlecomment",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="article_comment",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="articlecomment",
            name="comment",
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]