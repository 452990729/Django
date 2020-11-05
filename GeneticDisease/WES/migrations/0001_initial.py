# Generated by Django 2.2 on 2020-11-05 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patiantinfo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatiantWESTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('任务状态', models.CharField(choices=[('运行中', '运行中'), ('运行完成', '运行完成'), ('运行错误', '运行错误')], default='运行中', max_length=32)),
                ('任务开始时间', models.DateTimeField(auto_now_add=True)),
                ('质控结果', models.CharField(max_length=256)),
                ('全部结果', models.CharField(max_length=256)),
                ('最终结果', models.CharField(max_length=256)),
                ('执行人员', models.CharField(default='', max_length=256)),
                ('项目编号', models.CharField(default='', max_length=128)),
                ('项目信息', models.CharField(default='', max_length=256)),
                ('运行平台', models.CharField(choices=[('SGE', 'SGE'), ('local', 'local')], default='SGE', max_length=32)),
                ('运行核心数', models.CharField(default='', max_length=256)),
                ('项目路径', models.CharField(default='', max_length=256)),
                ('Patiant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patiantinfo.PatiantInfo')),
            ],
        ),
    ]
