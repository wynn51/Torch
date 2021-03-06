# Generated by Django 3.2.9 on 2021-11-24 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RoleManage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roleName', models.CharField(max_length=11, verbose_name='角色名称')),
                ('A', models.BooleanField(default=0, verbose_name='权限设置')),
                ('B1', models.BooleanField(default=0, verbose_name='基础数据库')),
                ('B2', models.BooleanField(default=0, verbose_name='火炬数据库')),
                ('B3', models.BooleanField(default=0, verbose_name='数据处理规则设置')),
                ('C1', models.BooleanField(default=0, verbose_name='规则设置')),
                ('C2_1', models.BooleanField(default=0, verbose_name='查询设置（企业审核）')),
                ('C2_2', models.BooleanField(default=0, verbose_name='审核查看（企业审核）')),
                ('C2_3', models.BooleanField(default=0, verbose_name='结果导出（企业审核）')),
                ('C3_1', models.BooleanField(default=0, verbose_name='极值查询（汇总审核）')),
                ('C3_2', models.BooleanField(default=0, verbose_name='汇总结果（汇总审核）')),
                ('C3_3', models.BooleanField(default=0, verbose_name='生成报告（汇总审核）')),
                ('D', models.BooleanField(default=0, verbose_name='企业画像')),
                ('E1', models.BooleanField(default=0, verbose_name='体系配置')),
                ('E2', models.BooleanField(default=0, verbose_name='综合评价')),
                ('E3', models.BooleanField(default=0, verbose_name='自定义评价')),
                ('F1', models.BooleanField(default=0, verbose_name='数据汇总')),
                ('F2', models.BooleanField(default=0, verbose_name='对标分析')),
                ('F3', models.BooleanField(default=0, verbose_name='报告生成')),
                ('is_active', models.BooleanField(default=1, verbose_name='是否激活')),
            ],
        ),
    ]
