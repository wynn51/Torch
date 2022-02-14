from django.db import models
from django.utils import timezone


# Create your models here.

class DataRules(models.Model):
    indicator_name = models.CharField('新指标名称', max_length=64)
    indicator_unit = models.CharField('单位', max_length=16, null=True)
    indicator_code = models.CharField('指标代码', max_length=16, unique=True)
    indicator_address = models.CharField('操作表', max_length=16)
    # lookTable = models.CharField('匹配表', max_length=16, blank=True,null=True)
    indicator_type = models.CharField('公式类型', max_length=8)
    dynamicFormula = models.TextField('计算公式', max_length=1024)

    create_time = models.DateTimeField('创建时间', default=timezone.now)
    update_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '数据处理指标设置'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.indicator_code
