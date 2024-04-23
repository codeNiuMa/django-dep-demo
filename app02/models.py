from django.db import models

# Create your models here.

class Department(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='部门id')
    title = models.CharField(max_length=32, verbose_name='部门名称')

class UserInfo(models.Model):
    # 创建字段
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    age = models.IntegerField()
    account = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField()

    # 级联删除
    depart = models.ForeignKey(to='Department', to_field='id', on_delete=models.CASCADE)
    # 置空
    # depart = models.ForeignKey(to='Department', to_field='id', null=True, blank=True, on_delete=models.SET_NULL)

    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.SmallIntegerField(choices=gender_choices)
