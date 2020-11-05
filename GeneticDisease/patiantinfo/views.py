import re
import json
from django.shortcuts import render
from django.http import HttpResponse,FileResponse
from django.forms import model_to_dict
from . import models
from . import forms
from login.models import LoginUser

# Create your views here.

def Pemmision(request):
    obj = LoginUser.objects.get(username=request.session['user_name'])
    if str(obj.info_right) == 'no':
        return 0
    return 1

def index(request):
    isactive = 'patiantinfo'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    data_list = []
    for data_info in models.PatiantInfo.objects.all():
        data_list.append({
            '家系编号': data_info.家系编号,
            '样本编号': data_info.样本编号,
            '检测类型': data_info.检测类型,
            '与先证者关系': data_info.与先证者关系,
            '姓名': data_info.姓名,
            '性别': data_info.性别,
            '年龄': data_info.年龄,
            '初步诊断': data_info.初步诊断,
            '联系电话': data_info.联系电话,
            '调查日期': data_info.调查日期.strftime('%Y-%m-%d %H:%M:%S'),
            '调查员': data_info.调查员,
            '诊断医生': data_info.诊断医生,
        })
    data_dic = {}
    data_dic['patiantable'] = data_list
    return render(request, 'patiantinfo/index.html', data_dic)

def CreatePatiant(request):
    isactive = 'patiantinfo'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    if not Pemmision(request):
        return render(request, 'RightWarning.html', locals())
    infoForm = forms.FullInfoForm()
    if request.method == "POST":
        infoForm = forms.FullInfoForm(request.POST, request.FILES)
        message = "please check in the content!"
        if infoForm.is_valid():
            print(1)
            家系编号 = infoForm.cleaned_data['家系编号']
            样本编号 = infoForm.cleaned_data['样本编号']
            检测类型 = infoForm.cleaned_data['检测类型']
            与先证者关系 = infoForm.cleaned_data['与先证者关系']
            姓名 = infoForm.cleaned_data['姓名']
            性别 = infoForm.cleaned_data['性别']
            年龄 = infoForm.cleaned_data['年龄']
            籍贯 = infoForm.cleaned_data['籍贯']
            民族 = infoForm.cleaned_data['民族']
            联系电话 = infoForm.cleaned_data['联系电话']
            样本类型 = infoForm.cleaned_data['样本类型']
            初步诊断 = infoForm.cleaned_data['初步诊断']
            受检者类型 = infoForm.cleaned_data['受检者类型']
            调查员 = infoForm.cleaned_data['调查员']
            诊断医生 = infoForm.cleaned_data['诊断医生']
            发病年龄 = infoForm.cleaned_data['发病年龄']
            病程进展 = infoForm.cleaned_data['病程进展']
            临床治疗手段及效果 = infoForm.cleaned_data['临床治疗手段及效果']
            主要和伴随症状 = infoForm.cleaned_data['主要和伴随症状']
            既往史 = infoForm.cleaned_data['既往史']
            家族史 = infoForm.cleaned_data['家族史']
            生活史 = infoForm.cleaned_data['生活史']
            既往基因检测情况 = infoForm.cleaned_data['既往基因检测情况']
            皮肤表型 = infoForm.cleaned_data['皮肤表型']
            if '照片' in request.FILES:
                照片 = request.FILES.getlist('照片')
            else:
                照片 = ''
            if '病理' in request.FILES:
                病理 = request.FILES.getlist('病理')
            else:
                病理 = ''
            送检单 = request.FILES.getlist('送检单')
            same_name_project = models.PatiantInfo.objects.filter(样本编号=样本编号)
            if same_name_project:
                message = '样本编号已经存在，请检查！'
                return render(request, 'patiantinfo/new.html', locals())
            new_project = models.PatiantInfo()
            new_project.家系编号 = 家系编号
            new_project.样本编号 = 样本编号
            new_project.检测类型 = 检测类型
            new_project.与先证者关系 = 与先证者关系
            new_project.姓名 = 姓名
            new_project.性别 = 性别
            new_project.年龄 = 年龄
            new_project.籍贯 = 籍贯
            new_project.民族 = 民族
            new_project.联系电话 = 联系电话
            new_project.样本类型 = 样本类型
            new_project.初步诊断 = 初步诊断
            new_project.受检者类型 = 受检者类型
            new_project.调查员 = 调查员
            new_project.诊断医生 = 诊断医生
            new_project.发病年龄 = 发病年龄
            new_project.病程进展 = 病程进展
            new_project.临床治疗手段及效果 = 临床治疗手段及效果
            new_project.主要和伴随症状 = 主要和伴随症状
            new_project.既往史 = 既往史
            new_project.家族史 = 家族史
            new_project.生活史 = 生活史
            new_project.既往基因检测情况 = 既往基因检测情况
            new_project.皮肤表型 = 皮肤表型
            new_project.save()
            new_project = models.PatiantInfo.objects.get(样本编号=样本编号)
            for f in 照片:
                models.PatiantPhoto.objects.create(Patiant=new_project,照片=f)
            for f in 病理:
                models.PatiantPathology.objects.create(Patiant=new_project,病理=f)
            for f in 送检单:
                models.PatiantInformation.objects.create(Patiant=new_project,送检单=f)
#            new_project.save()
#            return HttpResponse('新增成功')
            return render(request, 'patiantinfo/works.html', locals())
        return render(request, 'patiantinfo/new.html', locals())
    return render(request, 'patiantinfo/new.html', locals())

def PatiantDetail(request, patiant):
    isactive = 'patiantinfo'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    patiant_model = models.PatiantInfo.objects.get(样本编号=patiant)
    list_PatiantPhoto = []
    list_PatiantInformation = []
    list_PatiantPathology = []
    for ml in models.PatiantPhoto.objects.filter(Patiant=patiant_model):
        lb = re.split('\/', str(ml.照片))[-1]
        list_PatiantPhoto.append({'label': lb,
                                  'path': ml.照片})
    for ml in models.PatiantInformation.objects.filter(Patiant=patiant_model):
        lb = re.split('\/', str(ml.送检单))[-1]
        list_PatiantInformation.append({'label': lb,
                                  'path': ml.送检单})
    for ml in models.PatiantPathology.objects.filter(Patiant=patiant_model):
        lb = re.split('\/', str(ml.病理))[-1]
        list_PatiantPathology.append({'label': lb,
                                  'path': ml.病理})
#    dict_data = {}
#    for key in patiant_model:
#        dict_data[key] = patiant_model[key]
    form = forms.infoForm()
    patiant_form = forms.infoForm(instance=patiant_model)
    return render(request, 'patiantinfo/patiant.html', locals())

def GetImage(request, patiant, cls, date, pic):
    url_image = 'images/'+cls+'/'+date+'/'+pic
    files = open(url_image, 'rb')
    response = FileResponse(files)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(pic)
    return response

def ModPatiant(request, patiant):
    isactive = 'patiantinfo'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    if not Pemmision(request):
        return render(request, 'RightWarning.html', locals())
    patiant_model = models.PatiantInfo.objects.get(样本编号=patiant)
#    form = forms.infoForm()
    if request.method == "POST":
        infoForm = forms.FullInfoForm(request.POST, request.FILES, instance=patiant_model)
        message = "please check in the content!"
        if infoForm.is_valid():
            家系编号 = infoForm.cleaned_data['家系编号']
            样本编号 = infoForm.cleaned_data['样本编号']
            检测类型 = infoForm.cleaned_data['检测类型']
            与先证者关系 = infoForm.cleaned_data['与先证者关系']
            姓名 = infoForm.cleaned_data['姓名']
            性别 = infoForm.cleaned_data['性别']
            年龄 = infoForm.cleaned_data['年龄']
            籍贯 = infoForm.cleaned_data['籍贯']
            民族 = infoForm.cleaned_data['民族']
            联系电话 = infoForm.cleaned_data['联系电话']
            样本类型 = infoForm.cleaned_data['样本类型']
            初步诊断 = infoForm.cleaned_data['初步诊断']
            受检者类型 = infoForm.cleaned_data['受检者类型']
            调查员 = infoForm.cleaned_data['调查员']
            诊断医生 = infoForm.cleaned_data['诊断医生']
            发病年龄 = infoForm.cleaned_data['发病年龄']
            病程进展 = infoForm.cleaned_data['病程进展']
            临床治疗手段及效果 = infoForm.cleaned_data['临床治疗手段及效果']
            主要和伴随症状 = infoForm.cleaned_data['主要和伴随症状']
            既往史 = infoForm.cleaned_data['既往史']
            家族史 = infoForm.cleaned_data['家族史']
            生活史 = infoForm.cleaned_data['生活史']
            既往基因检测情况 = infoForm.cleaned_data['既往基因检测情况']
            皮肤表型 = infoForm.cleaned_data['皮肤表型']
            if '照片' in request.FILES:
                照片 = request.FILES.getlist('照片')
            else:
                照片 = ''
            if '病理' in request.FILES:
                病理 = request.FILES.getlist('病理')
            else:
                病理 = ''
            if '送检单' in request.FILES:
                送检单 = request.FILES.getlist('送检单')
            else:
                送检单 = ''
            patiant_model.家系编号 = 家系编号
            patiant_model.样本编号 = 样本编号
            patiant_model.检测类型 = 检测类型
            patiant_model.与先证者关系 = 与先证者关系
            patiant_model.姓名 = 姓名
            patiant_model.性别 = 性别
            patiant_model.年龄 = 年龄
            patiant_model.籍贯 = 籍贯
            patiant_model.民族 = 民族
            patiant_model.联系电话 = 联系电话
            patiant_model.样本类型 = 样本类型
            patiant_model.初步诊断 = 初步诊断
            patiant_model.受检者类型 = 受检者类型
            patiant_model.调查员 = 调查员
            patiant_model.诊断医生 = 诊断医生
            patiant_model.发病年龄 = 发病年龄
            patiant_model.病程进展 = 病程进展
            patiant_model.临床治疗手段及效果 = 临床治疗手段及效果
            patiant_model.主要和伴随症状 = 主要和伴随症状
            patiant_model.既往史 = 既往史
            patiant_model.家族史 = 家族史
            patiant_model.生活史 = 生活史
            patiant_model.既往基因检测情况 = 既往基因检测情况
            patiant_model.皮肤表型 = 皮肤表型
            for f in 照片:
                models.PatiantPhoto.objects.create(Patiant=patiant_model,照片=f)
            for f in 病理:
                models.PatiantPathology.objects.create(Patiant=patiant_model,病理=f)
            for f in 送检单:
                models.PatiantInformation.objects.create(Patiant=patiant_model,送检单=f)
            patiant_model.save()
            return PatiantDetail(request, patiant)
        return render(request, 'patiantinfo/modpatiant.html', locals())
    else:
        infoForm = forms.FullInfoForm(instance=patiant_model)
    return render(request, 'patiantinfo/modpatiant.html', locals())

def DelPatiant(request, patiant):
    isactive = 'patiantinfo'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    if not Pemmision(request):
        return render(request, 'RightWarning.html', locals())
    patiant_model = models.PatiantInfo.objects.get(样本编号=patiant)
    patiant_model.delete()
    return index(request)
