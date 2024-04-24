from django.db import models

# Create your models here.

class Department(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='部门id')
    title = models.CharField(max_length=32, verbose_name='部门名称')

    def __str__(self):
        return self.title

class UserInfo(models.Model):
    # 创建字段
    name = models.CharField(max_length=32, verbose_name='姓名')
    password = models.CharField(max_length=64, verbose_name='密码')
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='账户余额')
    create_time = models.DateField(verbose_name='入职时间')

    # 级联删除
    depart = models.ForeignKey(to='Department', to_field='id', on_delete=models.CASCADE, verbose_name='部门')
    # 置空
    # depart = models.ForeignKey(to='Department', to_field='id', null=True, blank=True, on_delete=models.SET_NULL)

    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.SmallIntegerField(choices=gender_choices, verbose_name='性别')
