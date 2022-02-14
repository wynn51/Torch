from django.db import models
from django.utils import timezone

from ..systemSet.models import RoleManage,Area
# Create your models here.
class User(models.Model):
    username = models.CharField('用户名',max_length=20,unique=True,null=False)
    password = models.CharField('密码',max_length=32,null=False)

    area = models.ForeignKey(Area,on_delete=models.CASCADE,null=False)
    role = models.ForeignKey(RoleManage,on_delete=models.CASCADE,null=False)

    is_active = models.CharField('状态',max_length=2,default="启用",null=False)
    create_time = models.DateTimeField('创建时间',default=timezone.now)
    update_time = models.DateTimeField('修改时间',auto_now=True)

    token = models.CharField('token',max_length=256,null=True)

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    # def get_is_active(self):


