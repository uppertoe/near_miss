# Generated by Django 4.1.7 on 2023-04-05 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name='issue',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='comments',
            field=models.ManyToManyField(related_name='issues', through='issues.Tag', to='issues.comment'),
        ),
    ]