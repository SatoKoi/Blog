# Generated by Django 2.0.3 on 2018-06-07 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_emailvarifyrecord_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='default/user.png', upload_to='user/%Y/%m', verbose_name='用户头像'),
        ),
    ]
