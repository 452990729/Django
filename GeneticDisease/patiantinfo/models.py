from django.db import models
from django.conf import settings

class PatiantInfo(models.Model):
#    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    家系编号 = models.CharField(max_length=24)
#    样本编号 = models.CharField(max_length=256)
    样本编号 = models.CharField(max_length=24,  primary_key=True)
    检测类型 = models.CharField(choices=(('外显子-单人', '外显子-单人'), ('外显子-家系', '外显子-家系'), ('Sanger测序', 'Sanger测序')), max_length=10)
    与先证者关系 = models.CharField(max_length=10)
    姓名 = models.CharField(max_length=10)
    性别 = models.CharField(choices=(('男', '男'), ('女', '女')), max_length=10)
    年龄 = models.CharField(max_length=256)
    籍贯 = models.CharField(max_length=256)
    民族 = models.CharField(max_length=10)
    联系电话 = models.CharField(max_length=11)
    样本类型 = models.CharField(choices=(('外周血', '外周血'), ('DNA', 'DNA'), ('肌肉组织', '肌肉组织'), ('流产组织', '流产组织'), ('唾液', '唾液')), max_length=10)
    初步诊断 = models.CharField(max_length=10)
    受检者类型 = models.CharField(choices=(('确诊患者', '确诊患者'), ('疑似患者', '疑似患者'), ('表型正常人群', '表型正常人群'), ('其他表型', '其他表型')), max_length=10)
    调查员 = models.CharField(max_length=10)
    诊断医生 = models.CharField(max_length=10)
    调查日期 = models.DateTimeField(auto_now_add=True)
    发病年龄 = models.CharField(max_length=10)
    病程进展 = models.CharField(max_length=10)
    临床治疗手段及效果 = models.CharField(max_length=10)
    主要和伴随症状 = models.CharField(max_length=10)
    既往史 = models.CharField(max_length=256)
    家族史 = models.CharField(max_length=256)
    生活史 = models.CharField(max_length=256)
    既往基因检测情况 = models.CharField(max_length=256)
    皮肤表型 = models.CharField(max_length=256)
#    照片 = models.ImageField(upload_to='images/照片/%Y/%m/%d/',verbose_name='照片')
#    病理 = models.ImageField(upload_to='images/病理/%Y/%m/%d/',verbose_name='病理')
#    送检单 = models.ImageField(upload_to='images/送检单/%Y/%m/%d/',verbose_name='送检单')

class PatiantPhoto(models.Model):
    Patiant = models.ForeignKey(PatiantInfo,on_delete=models.CASCADE)
    照片 = models.FileField(upload_to='照片/%Y-%m-%d/', null=True, blank=True, verbose_name='照片')

class PatiantPathology(models.Model):
    Patiant = models.ForeignKey(PatiantInfo,on_delete=models.CASCADE)
    病理  = models.FileField(upload_to='病理/%Y-%m-%d/', null=True, blank=True, verbose_name='病理')

class PatiantInformation(models.Model):
    Patiant = models.ForeignKey(PatiantInfo,on_delete=models.CASCADE)
    送检单 = models.FileField(upload_to='送检单/%Y-%m-%d/', null=True, blank=True, verbose_name='送检单')
