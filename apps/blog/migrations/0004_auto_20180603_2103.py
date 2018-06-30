# Generated by Django 2.0.3 on 2018-06-03 21:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180603_2100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlecategory',
            name='article',
        ),
        migrations.AlterField(
            model_name='pagedetail',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.ArticleCategory', verbose_name='分类'),
        ),
    ]
