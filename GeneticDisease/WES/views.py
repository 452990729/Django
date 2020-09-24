import os
import re
from glob import glob
from django.shortcuts import render
from django.http import HttpResponse,FileResponse
from django.utils.decorators import method_decorator
from django.utils import timezone
from . import models
from .forms import WESForm,PatiantWESTableForm
from patiantinfo.models import PatiantInfo
from login.models import LoginUser

# Create your views here.

def Pemmision(request):
    obj = LoginUser.objects.get(username=request.session['user_name'])
    if obj.wes_right == 'no':
        return 0
    return 1


def Index(request):
    isactive = 'WES'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    data_list = []
    for ob in models.PatiantWESTable.objects.exclude(任务状态='运行完成'):
        UpdateStatus(ob)
    for data_info in models.PatiantWESTable.objects.all():
        data_list.append({
            '项目编号': data_info.项目编号,
            '家系编号': data_info.Patiant.家系编号,
            '样本编号': data_info.Patiant.样本编号,
            '姓名': data_info.Patiant.姓名,
            '初步诊断': data_info.Patiant.初步诊断,
            '任务状态': data_info.任务状态,
            '任务开始时间': data_info.任务开始时间.strftime('%Y-%m-%d %H:%M:%S'),
            '质控结果': data_info.质控结果,
            '全部结果': data_info.全部结果,
            '最终结果': data_info.最终结果,
        })
    data_dic = {}
    data_dic['patiantable'] = data_list
    return render(request, 'Wes/index.html', data_dic)

def CreateNew(request):
    isactive = 'WES'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    if not Pemmision(request):
        return render(request, 'RightWarning.html', locals())
    if request.method == "POST":
        wes_form = WESForm(request.POST, request.FILES)
        message = "please check in the content!"
        if wes_form.is_valid():
            config = wes_form.cleaned_data['config']
            config_file = request.FILES.getlist('config_file')
            项目编号 = wes_form.cleaned_data['项目编号']
            样本编号 = wes_form.cleaned_data['样本编号']
            样本信息 = wes_form.cleaned_data['样本信息']
            运行平台 = wes_form.cleaned_data['运行平台']
            运行核心数 = wes_form.cleaned_data['运行核心数']
            same_name_project = models.PatiantWESTable.objects.filter(项目编号=项目编号)
            if same_name_project:
                message = '项目名称已经存在，请选择其他'
                return render(request, 'Wes/new.html', locals())
            ProjectPath = HandleWES(config, config_file, 项目编号, 样本信息, 运行平台, 运行核心数, )
            RawPatiant = PatiantInfo.objects.get(样本编号=样本编号)
            new_project = models.PatiantWESTable.objects.create(Patiant=RawPatiant)
            new_project.执行人员 = request.user.username
            new_project.项目编号 = 项目编号
            new_project.样本编号 = 样本编号
            new_project.样本信息 = 样本信息
            new_project.运行平台 = 运行平台
            new_project.运行核心数 = 运行核心数
            new_project.项目路径 = ProjectPath
            new_project.任务状态 = '运行中'
            new_project.save()
            return render(request, 'JobLoad.html', locals())
        return render(request, 'Wes/new.html', locals())
    wes_form = WESForm()
    return render(request, 'Wes/new.html', locals())

def HandleWES(config, config_file, project, info, platform, cores, ):
    OUTPATH = '/mnt/dfc_data1/project/lixuefei/WES'
    Pipeline = '/mnt/dfc_data1/home/lixuefei/Pipeline/Exon/Bin/ExonPipeline.py'
    ProjectPath = os.path.join(OUTPATH, project)
    if not os.path.exists(ProjectPath):
        os.mkdir(ProjectPath)
    RawDataPath = os.path.join(ProjectPath, 'RawData')
    if not os.path.exists(RawDataPath):
        os.mkdir(RawDataPath)
    RunPath = os.path.join(ProjectPath, 'Run')
    if not os.path.exists(RunPath):
        os.mkdir(RunPath)
    print(config_file)
    if len(config_file) > 0:
        UploadFile(config_file, RawDataPath)
        ReadConfig(glob(RawDataPath+'/*')[0], ProjectPath)
    else:
        ReadConfig(config, ProjectPath)
#    print(fastq_file)
#    if len(fastq_file) > 0:
#        UploadFile(fastq_file, RawDataPath)
    shell = open(os.path.join(RunPath, 'run.sh'), 'w')
    shell.write('{} -c {} -o {} -p {} -j {} -r'.format(Pipeline, os.path.join(RunPath, 'config.lst'),\
                                                      RunPath, platform, cores))
    shell.close()
    os.system('sh {}'.format(os.path.join(RunPath, 'run.sh')))
    return ProjectPath

def UploadFile(list_in, outpath):
    for f in list_in:
        destination = open(os.path.join(outpath, f.name),'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()

def ReadConfig(config, outpath):
    out = open(os.path.join(outpath, 'Run/config.lst'), 'w')
    if os.path.isfile(config):
        with open(config, 'r') as f:
            content = f.read()
    else:
        content = config
    for line in re.split('\n', content.strip()):
        if line and not line.startswith('#'):
            list_split = re.split('\s+', line.strip())
            if '/' in list_split[2]:
                for i in re.split(',', list_split[2]):
                    os.system('ln -s {} {}'.format(i, outpath+'/RawData'))
            list_fq = [re.split('\/', i)[-1] for i in re.split(',', list_split[2])]
            out.write(list_split[0]+'\t'+list_split[1]+'\t'+outpath+'/RawData/'+list_fq[0]+','+outpath+'/RawData/'+list_fq[1]+'\n')
    out.close()

def WESDetail(request, project):
    isactive = 'WES'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    Project_model = models.PatiantWESTable.objects.get(项目编号=project)
    form = PatiantWESTableForm()
    Project_form = PatiantWESTableForm(instance=Project_model)
    list_file = {}
    if Project_model.任务状态 == '运行完成':
        QC = {'qc_result': Project_model.质控结果, 'label': '下载'}
        all_als = {'all_result': Project_model.全部结果, 'label': '下载'}
        final_als = {'final_result': Project_model.最终结果, 'label': '下载'}
    else:
        QC = {'qc_result': '', 'label': ''}
        all_als = {'all_result': '', 'label': ''}
        final_als = {'final_result': '', 'label': ''}
    return render(request, 'Wes/detail.html', locals())

def DelPatiant(request, project):
    isactive = 'WES'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    if not Pemmision(request):
        return render(request, 'RightWarning.html', locals())
    Project_model = models.PatiantWESTable.objects.get(项目编号=project)
    Project_model.delete()
    return Index(request)

def UpdateStatus(project):
     AllFile = project.项目路径+'/Run/6.Final/AllIntergrateMutation.xlsx'
     FinalFile = project.项目路径+'/Run/6.Final/FinalIntergrateMutation.xlsx'
     QCfile = project.项目路径+'/Run/6.Final/QCStat.xls'
     if os.path.isfile(FinalFile):
         project.任务状态 = '运行完成'
         project.质控结果 = QCfile
         project.全部结果 = AllFile
         project.最终结果 = FinalFile
         project.save()

def DownloadFile(request, file_path):
    files = open(file_path, 'rb')
    label = re.split('/', file_path)[-1]
    response = FileResponse(files)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(label)
    return response
