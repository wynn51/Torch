# Generated by Django 3.2.9 on 2021-11-24 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '用户管理', 'verbose_name_plural': '用户管理'},
        ),
    ]
