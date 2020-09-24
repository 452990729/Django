from django import forms
from django.forms import ModelForm
from . import models
from patiantinfo.models import PatiantInfo
from WES.models import PatiantWESTable
from Sanger.models import PatiantSangerTable

class ReportPatiantTableForm(ModelForm):
    class Meta:
        model = PatiantInfo
        fields = ['家系编号', '样本编号', '检测类型', '与先证者关系', '姓名', '联系电话','初步诊断']

class ReportWESTableForm(ModelForm):
    class Meta:
        model = PatiantWESTable
        fields = ['项目编号',  '任务状态', '项目信息', '质控结果', '全部结果', '最终结果']

class ReportSangerTableForm(ModelForm):
    class Meta:
        model = PatiantSangerTable
        fields = ['项目编号', '任务状态', '目标基因', '最终结果']

class UploadReportForm(ModelForm):
    class Meta:
        model = models.PatiantReportTable
        fields = ['报告',]
    报告 = forms.FileField(label="上传报告", widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': False}), required=True)
