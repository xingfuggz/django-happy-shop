# Generated by Django 3.2.7 on 2021-10-10 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='desc',
            field=models.TextField(blank=True, default='', max_length=200, verbose_name='个人简介'),
        ),
    ]