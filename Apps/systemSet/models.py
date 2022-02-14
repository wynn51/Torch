from django.db import models

# Create your models here.
from django.utils import timezone


class RoleManage(models.Model):
    roleName = models.CharField('角色名称',max_length=11,unique=True)
    A = models.BooleanField('权限设置', default=0)
    B1 = models.BooleanField('基础数据库', default=0)
    B2 = models.BooleanField('火炬数据库', default=0)
    B3 = models.BooleanField('数据处理规则设置', default=0)
    C1 = models.BooleanField('规则设置', default=0)

    C2_1 = models.BooleanField('查询设置（企业审核）', default=0)
    C2_2 = models.BooleanField('审核查看（企业审核）', default=0)
    C2_3 = models.BooleanField('结果导出（企业审核）', default=0)

    C3_1 = models.BooleanField('极值查询（汇总审核）', default=0)
    C3_2 = models.BooleanField('汇总结果（汇总审核）', default=0)
    C3_3 = models.BooleanField('生成报告（汇总审核）', default=0)

    D = models.BooleanField('企业画像', default=0)
    E1 = models.BooleanField('体系配置', default=0)
    E2 = models.BooleanField('综合评价', default=0)
    E3 = models.BooleanField('自定义评价', default=0)
    F1 = models.BooleanField('数据汇总', default=0)
    F2 = models.BooleanField('对标分析', default=0)
    F3 = models.BooleanField('报告生成', default=0)

    is_active = models.BooleanField('是否激活',default=1)
    create_time = models.DateTimeField('创建时间', default=timezone.now)
    update_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '角色管理'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.roleName

class Area(models.Model):
    areaName = models.CharField('所属区域',max_length=11,unique=True)
    areaCode = models.CharField('区划代码', max_length=11,unique=True)
    areaType = models.CharField('类型',max_length=11)
    is_active = models.BooleanField('是否激活',default=1)
    create_time = models.DateTimeField('创建时间',default=timezone.now)
    update_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '区划管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.areaName


