# Generated by Django 3.2.10 on 2024-05-06 02:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app02', '0005_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oid', models.CharField(max_length=64, verbose_name='订单号')),
                ('title', models.CharField(max_length=32, verbose_name='标题')),
                ('price', models.IntegerField(verbose_name='价格')),
                ('status', models.SmallIntegerField(choices=[(1, '待支付'), (2, '已支付')], default=1, verbose_name='状态')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app02.userinfo')),
            ],
        ),
    ]
