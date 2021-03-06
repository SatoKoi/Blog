# Generated by Django 2.0.3 on 2018-06-03 20:36

import DjangoUeditor.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=20)),
                ('nums', models.IntegerField(default=0, verbose_name='引用个数')),
            ],
            options={
                'verbose_name': '分类集',
                'verbose_name_plural': '分类集',
            },
        ),
        migrations.CreateModel(
            name='PageDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='标题')),
                ('category', models.CharField(max_length=20, verbose_name='分类')),
                ('comments', models.IntegerField(default=0, verbose_name='评论数')),
                ('views', models.IntegerField(default=0, verbose_name='访问数')),
                ('detail', DjangoUeditor.models.UEditorField(default='', verbose_name='文章详情')),
                ('image', models.ImageField(upload_to='posts/%Y/%m', verbose_name='封面图')),
                ('tags', models.CharField(default='', max_length=12, verbose_name='标签')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='发布日期')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='文章作者')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.CreateModel(
            name='SiteInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=20, verbose_name='网站名称')),
                ('category_nums', models.IntegerField(default=0, verbose_name='分类个数')),
                ('lasting_time', models.IntegerField(default=0, verbose_name='运行时间')),
                ('article_nums', models.IntegerField(default=0, verbose_name='文章个数')),
                ('comments_nums', models.IntegerField(default=0, verbose_name='评论条数')),
                ('total_views', models.IntegerField(default=0, verbose_name='总访问量')),
                ('tag_nums', models.IntegerField(default=0, verbose_name='标签个数')),
            ],
            options={
                'verbose_name': '网站详情',
                'verbose_name_plural': '网站详情',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=12, verbose_name='标签')),
                ('nums', models.IntegerField(default=0, verbose_name='引用个数')),
            ],
            options={
                'verbose_name': '标签集',
                'verbose_name_plural': '标签集',
            },
        ),
        migrations.CreateModel(
            name='TagsMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.PageDetail', verbose_name='文章')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Tags', verbose_name='标签')),
            ],
            options={
                'verbose_name': '标签映射集',
                'verbose_name_plural': '标签映射集',
            },
        ),
        migrations.AddField(
            model_name='articlecategory',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.PageDetail', verbose_name='文章'),
        ),
    ]
