from django.db import models
from patiantinfo.models import PatiantInfo
from WES.models import PatiantWESTable
from Sanger.models import PatiantSangerTable

# Create your models here.

class PatiantReportTable(models.Model):
    Patiant = models.ForeignKey(PatiantInfo,on_delete=models.CASCADE)
    项目编号 = models.AutoField(primary_key=True)
    报告 = models.FileField(upload_to='Reports/Company/%Y-%m-%d', null=True, blank=True, verbose_name='报告')

