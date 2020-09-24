from django.db import models
from patiantinfo.models import PatiantInfo
from django.utils import timezone

class PatiantSangerTable(models.Model):
    Patiant = models.ForeignKey(PatiantInfo,on_delete=models.CASCADE)
    任务状态 = models.CharField(max_length=32,choices=(('运行中','运行中'), ('运行完成', '运行完成'), ('运行错误', '运行错误')), default='运行中')
    任务开始时间 = models.DateTimeField(auto_now_add=True)
#    质控结果 = models.CharField(max_length=256)
#    全部结果 = models.CharField(max_length=256)
    最终结果 = models.CharField(max_length=256)
    执行人员 = models.CharField(max_length=256, default='')
    项目编号 = models.CharField(max_length=128, default='')
#    样本编号 = models.CharField(max_length=128)
    目标基因 = models.CharField(max_length=256, default='')
#    运行平台 = models.CharField(max_length=32,choices=(('SGE','SGE'), ('local', 'local')),default='SGE')
#    运行核心数 = models.CharField(max_length=256, default='')
    项目路径 = models.CharField(max_length=256, default='')
