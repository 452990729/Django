import os
import re
from glob import glob
from django.shortcuts import render
from django.http import HttpResponse,FileResponse
from django.utils import timezone
from django.conf import settings
from . import models
from . import forms
from patiantinfo.models import PatiantInfo,PatiantPhoto,PatiantInformation,PatiantPathology
from WES.models import PatiantWESTable
from Sanger.models import PatiantSangerTable
from login.models import LoginUser

# Create your views here.

def Pemmision(request):
    obj = LoginUser.objects.get(username=request.session['user_name'])
    if str(obj.report_right) == 'no':
        return 0
    return 1

def QueryData(model_in, Patiant):
    project = model_in.objects.filter(Patiant=Patiant)
    if Patiant.检测类型 == 'Sanger测序':
        barc = 'None'
    else:
        barc = '未进行'
    list_out = []
    if len(project)>0:
        for ob in project:
            list_out.append(ob.项目编号)
    else:
#        if Patiant.检测类型 == 'Sanger测序':
#            list_out = ['None',]
#        else:
#            list_out = ['未进行',]
        pass
    return list_out

def Index(request):
    isactive = 'Report'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    for Patiant in PatiantInfo.objects.all():
        same_name_project = models.PatiantReportTable.objects.filter(Patiant=Patiant)
        if not same_name_project:
            new_project = models.PatiantReportTable.objects.create(Patiant=Patiant)
            new_project.save()
    data_list = []
    for data_info in models.PatiantReportTable.objects.all():
        if data_info.报告:
            rps = data_info.报告.url
        else:
            rps = ''
        data_list.append({
            '项目编号': 'FPR000'+str(data_info.项目编号),
            '家系编号': data_info.Patiant.家系编号,
            '样本编号': data_info.Patiant.样本编号,
            '姓名': data_info.Patiant.姓名,
            '初步诊断': data_info.Patiant.初步诊断,
            'WES结果': QueryData(PatiantWESTable, data_info.Patiant),
            'Sanger结果': QueryData(PatiantSangerTable, data_info.Patiant),
            '报告': rps
        })
    data_dic = {}
    data_dic['patiantable'] = data_list
    return render(request, 'Report/index.html', data_dic)

def ProjectDetail(request, project):
    isactive = 'Report'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    Report_Patiant = models.PatiantReportTable.objects.get(项目编号=int(project.lstrip('FPR000')))
    Patiant = Report_Patiant.Patiant
    list_PatiantPhoto = []
    list_PatiantInformation = []
    list_PatiantPathology = []
    for ml in PatiantPhoto.objects.filter(Patiant=Patiant):
        lb = re.split('\/', str(ml.照片))[-1]
        list_PatiantPhoto.append({'label': lb,
                                  'path': ml.照片})
    for ml in PatiantInformation.objects.filter(Patiant=Patiant):
        lb = re.split('\/', str(ml.送检单))[-1]
        list_PatiantInformation.append({'label': lb,
                                        'path': ml.送检单})
    for ml in PatiantPathology.objects.filter(Patiant=Patiant):
        lb = re.split('\/', str(ml.病理))[-1]
        list_PatiantPathology.append({'label': lb,
                                      'path': ml.病理})
    form = forms.ReportPatiantTableForm()
    patiant_form = forms.ReportPatiantTableForm(instance=Patiant)
    list_wes = []
    for ob in PatiantWESTable.objects.filter(Patiant=Patiant):
        form = forms.ReportWESTableForm()
        list_wes.append(forms.ReportWESTableForm(instance=ob))
    list_sanger = []
    for ob in PatiantSangerTable.objects.filter(Patiant=Patiant):
        form = forms.ReportSangerTableForm()
        list_sanger.append(forms.ReportSangerTableForm(instance=ob))
    report_form = forms.UploadReportForm()
    if request.method == "POST":
        if not Pemmision(request):
            return render(request, 'RightWarning.html', locals())
        report_form = forms.UploadReportForm(request.POST, request.FILES)
        if report_form.is_valid():
            报告 = request.FILES.getlist('报告')[0]
            Report_Patiant.报告 = 报告
            Report_Patiant.save()
            return render(request, 'Report/detail.html', locals())
    return render(request, 'Report/detail.html', locals())

def DelPatiant(request, project):
    isactive = 'WES'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    if not Pemmision(request):
        return render(request, 'RightWarning.html', locals())
    Project_model = models.PatiantReportTable.objects.get(项目编号=project)
    Project_model.delete()
    return Index(request)

def DownloadFile(request, file_path):
    if file_path.startswith('/images'):
        fl_path = settings.BASE_DIR+file_path
    if file_path.startswith('/Reports'):
        fl_path = settings.BASE_DIR+file_path
    else:
        fl_path = file_path
    files = open(fl_path, 'rb')
    label = re.split('/', file_path)[-1]
    response = FileResponse(files)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(label)
    return response
