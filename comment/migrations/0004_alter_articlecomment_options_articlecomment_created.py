# Generated by Django 4.1.5 on 2023-03-06 13:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("comment", "0003_alter_articlecomment_article_related_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="articlecomment",
            options={"ordering": ("created",)},
        ),
        migrations.AddField(
            model_name="articlecomment",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]