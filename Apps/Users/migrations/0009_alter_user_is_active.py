# Generated by Django 3.2.9 on 2021-11-25 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0008_alter_user_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.CharField(choices=[(1, '启用'), (0, '禁用')], default=1, max_length=2, verbose_name='状态'),
        ),
    ]
