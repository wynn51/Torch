# Generated by Django 3.2.9 on 2021-11-30 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0010_alter_user_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.CharField(max_length=256, null=True, verbose_name='token'),
        ),
    ]
