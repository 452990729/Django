from django import forms
from django.forms import ModelForm
from . import models
from patiantinfo.models import PatiantInfo


class PatiantSangerTableForm(ModelForm):
    class Meta:
        model = models.PatiantSangerTable
        fields = ['项目编号',  '任务状态', '目标基因']


class SangerForm(ModelForm):
    class Meta:
        model = models.PatiantSangerTable
        fields = ['项目编号', '样本编号', '目标基因']
    config = forms.CharField(label="*输入数据绝对路径",max_length=100,widget=forms.Textarea(attrs={'class': 'form-control'}), help_text='请添加数据绝对路径')
    项目编号 = forms.CharField(label="*项目编号", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}), help_text='项目编号', initial='NGSWES001', required=True)
    All_wes_sample = PatiantInfo.objects.all()
    list_sample_choice = []
#    for sample in All_wes_sample:
#        tup = (sample.样本编号, sample.样本编号)
#        list_sample_choice.append(tup)
    样本编号 = forms.ChoiceField(label='*样本编号', choices=tuple(list_sample_choice), required=True)
    目标基因 = forms.CharField(label="目标基因", max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
