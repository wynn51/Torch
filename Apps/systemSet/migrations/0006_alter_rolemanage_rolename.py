# Generated by Django 3.2.9 on 2021-11-25 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systemSet', '0005_alter_area_areaname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rolemanage',
            name='roleName',
            field=models.CharField(max_length=11, unique=True, verbose_name='角色名称'),
        ),
    ]
