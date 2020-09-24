from django import forms
from django.forms import ModelForm
from . import models


class infoForm(ModelForm):
    class Meta:
        model = models.PatiantInfo
        fields = ['家系编号', '样本编号', '检测类型', '与先证者关系', '姓名', '性别', '年龄', '籍贯', '民族', '联系电话',\
                  '样本类型', '初步诊断', '受检者类型', '调查员', '诊断医生', '发病年龄', '病程进展', '临床治疗手段及效果',\
                  '主要和伴随症状', '既往史', '家族史', '生活史', '既往基因检测情况', '皮肤表型']

    家系编号 = forms.CharField(label="*家系编号",max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    样本编号 = forms.CharField(label="*样本编号",max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    检测类型 = forms.ChoiceField(choices=(('外显子-单人', '外显子-单人'), ('外显子-家系', '外显子-家系'), ('Sanger测序', 'Sanger测序')), label="*检测类型")
    与先证者关系 = forms.CharField(label='*与先证者关系', max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    姓名 = forms.CharField(label="*姓名",max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    性别 = forms.ChoiceField(label='*性别', choices=(('男', '男'), ('女', '女')))
    年龄 = forms.CharField(label="*年龄",max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    籍贯 = forms.CharField(label="籍贯",max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    民族 = forms.CharField(label="民族",max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    联系电话 = forms.CharField(label="*联系电话",max_length=11, widget=forms.TextInput(attrs={'class': 'form-control'}))
    样本类型 = forms.ChoiceField(choices=(('外周血', '外周血'), ('DNA', 'DNA'), ('肌肉组织', '肌肉组织'), ('流产组织', '流产组织'), ('唾液', '唾液')), label="*样本类型")
    初步诊断 = forms.CharField(label="*初步诊断",max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    受检者类型 = forms.ChoiceField(choices=(('确诊患者', '确诊患者'), ('疑似患者', '疑似患者'), ('表型正常人群', '表型正常人群'), ('其他表型', '其他表型')), label="*受检者类型")
    调查员 = forms.CharField(label="*调查员",max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    诊断医生 = forms.CharField(label="*诊断医生",max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    发病年龄 = forms.CharField(label="*发病年龄",max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    病程进展 = forms.CharField(label="*病程进展",max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    临床治疗手段及效果 = forms.CharField(label="临床治疗手段及效果",max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    主要和伴随症状 = forms.CharField(label="主要/伴随症状",max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    既往史 = forms.CharField(label="既往史",max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    家族史 = forms.CharField(label="家族史",max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    生活史 = forms.CharField(label="生活史",max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    既往基因检测情况 = forms.CharField(label="*既往基因检测情况",max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    皮肤表型 = forms.CharField(label="皮肤表型",max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
#    照片 = forms.ImageField(label='照片', widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': True}), required=False)
#    病理 = forms.ImageField(label='病理', widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': True}), required=False)
#    送检单 = forms.ImageField(label='*送检单', widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': True}))


class FullInfoForm(infoForm):
    class Meta(infoForm.Meta):
        fields = infoForm.Meta.fields + ['照片', '病理', '送检单']

    照片 = forms.FileField(label='照片', widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': True}), required=False)
    病理 = forms.FileField(label='病理', widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': True}), required=False)
    送检单 = forms.FileField(label='*送检单', widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': True}), required=False)


#class PatiantDetailForm(ModelForm):
#    class Meta:
#        model = models.PatiantInfo
#        fields = ['家系编号', '样本编号', '检测类型', '与先证者关系', '姓名', '性别', '年龄', '籍贯', '民族', '联系电话',\
#                 '样本类型', '初步诊断', '受检者类型', '调查员', '诊断医生', '发病年龄', '病程进展', '临床治疗手段及效果',\
#                 '主要和伴随症状', '既往史', '家族史', '生活史', '既往基因检测情况', '皮肤表型', '照片', '病理', '送检单']
