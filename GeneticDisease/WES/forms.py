from django import forms
from django.forms import ModelForm
from . import models
from patiantinfo.models import PatiantInfo


class PatiantWESTableForm(ModelForm):
    class Meta:
        model = models.PatiantWESTable
        fields = ['项目编号',  '任务状态', '项目信息', '运行平台', '运行核心数']


class WESForm(ModelForm):
    class Meta:
        model = models.PatiantWESTable
        fields = ['项目编号', '样本编号', '项目信息', '运行平台', '运行核心数']
    config = forms.CharField(label="*输入配置文件",max_length=500,widget=forms.Textarea(attrs={'class': 'form-control'}), help_text='sample\tgroup\tfq1,fq2\n请添加数据绝对路径', initial='#sample\tgroup\tfastq1.gz,fastq2.gz')
    config_file = forms.FileField(label="上传配置文件", widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': True}), required=False)
    项目编号 = forms.CharField(label="*项目编号", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}), help_text='项目编号', initial='NGSWES001', required=True)
    All_wes_sample = PatiantInfo.objects.exclude(检测类型='Sanger测序')
    list_sample_choice = []
#    for sample in All_wes_sample:
#        tup = (sample.样本编号, sample.样本编号)
#        list_sample_choice.append(tup)
    样本编号 = forms.ChoiceField(label='*样本编号', choices=tuple(list_sample_choice), required=True)
    项目信息 = forms.CharField(label="项目信息", max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}), initial='human')
    运行平台 = forms.ChoiceField(label='*运行平台', choices=(('SGE','SGE'), ('local','local')), initial='SGE', required=True)
    运行核心数 = forms.CharField(label="运行核心数", max_length=2, widget=forms.TextInput(attrs={'class': 'form-control'}), initial='4')
