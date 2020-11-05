import os
import re
from glob import glob
from django.shortcuts import render
from django.http import HttpResponse,FileResponse
from django.utils import timezone
from . import models
from .forms import SangerForm,PatiantSangerTableForm
from patiantinfo.models import PatiantInfo
from login.models import LoginUser

# Create your views here.

def Pemmision(request):
    obj = LoginUser.objects.get(username=request.session['user_name'])
    if str(obj.sanger_right) == 'no':
        return 0
    return 1

def Index(request):
    isactive = 'Sanger'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    data_list = []
    for ob in models.PatiantSangerTable.objects.exclude(任务状态='运行完成'):
        UpdateStatus(ob)
    for data_info in models.PatiantSangerTable.objects.all():
        data_list.append({
            '项目编号': data_info.项目编号,
            '家系编号': data_info.Patiant.家系编号,
            '样本编号': data_info.Patiant.样本编号,
            '姓名': data_info.Patiant.姓名,
            '初步诊断': data_info.Patiant.初步诊断,
            '任务状态': data_info.任务状态,
            '任务开始时间': data_info.任务开始时间.strftime('%Y-%m-%d %H:%M:%S'),
            '最终结果': data_info.最终结果,
        })
    data_dic = {}
    data_dic['patiantable'] = data_list
    return render(request, 'Sanger/index.html', data_dic)

def CreateNew(request):
    isactive = 'Sanger'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    if not Pemmision(request):
        return render(request, 'RightWarning.html', locals())
    if request.method == "POST":
        sanger_form = SangerForm(request.POST)
        message = "please check in the content!"
        if sanger_form.is_valid():
            config = sanger_form.cleaned_data['config']
            项目编号 = sanger_form.cleaned_data['项目编号']
            样本编号 = sanger_form.cleaned_data['样本编号']
            目标基因 = sanger_form.cleaned_data['目标基因']
            same_name_project = models.PatiantSangerTable.objects.filter(项目编号=项目编号)
            if same_name_project:
                message = '项目名称已经存在，请选择其他'
                return render(request, 'Sanger/new.html', locals())
            ProjectPath = HandleSanger(config, 项目编号, 目标基因)
            RawPatiant = PatiantInfo.objects.get(样本编号=样本编号)
            new_project = models.PatiantSangerTable.objects.create(Patiant=RawPatiant)
            new_project.执行人员 = request.user.username
            new_project.项目编号 = 项目编号
            new_project.样本编号 = 样本编号
            new_project.目标基因 = 目标基因
            new_project.项目路径 = ProjectPath
            new_project.任务状态 = '运行中'
            new_project.save()
            return render(request, 'JobLoad.html', locals())
        return render(request, 'Sanger/new.html', locals())
    sanger_form = SangerForm()
    return render(request, 'Sanger/new.html', locals())

def HandleSanger(config,  project, gene, ):
    OUTPATH = '/mnt/dfc_data1/project/lixuefei/Sanger'
    Pipeline = '/mnt/dfc_data1/home/zhangyongjun/database/gtc/ODS/run_ods.pl'
    ProjectPath = os.path.join(OUTPATH, project)
    if not os.path.exists(ProjectPath):
        os.mkdir(ProjectPath)
#    print(fastq_file)
#    if len(fastq_file) > 0:
#        UploadFile(fastq_file, RawDataPath)
    shell = open(os.path.join(ProjectPath, 'run.sh'), 'w')
    os.chdir(ProjectPath)
    shell.write('cp -rf {} {}/chromat_dir\n'.format(config.strip(), ProjectPath))
    shell.write('{} {} {}\n'.format(Pipeline, project, gene))
    shell.close()
    os.system('nohup sh run.sh&')
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

def SangerDetail(request, project):
    isactive = 'Sanger'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    Project_model = models.PatiantSangerTable.objects.get(项目编号=project)
    form = PatiantSangerTableForm()
    Project_form = PatiantSangerTableForm(instance=Project_model)
    list_file = {}
    if Project_model.任务状态 == '运行完成':
        final_als = {'final_result': Project_model.最终结果, 'label': '下载'}
    else:
        final_als = {'final_result': '', 'label': ''}
    return render(request, 'Sanger/detail.html', locals())

def DelPatiant(request, project):
    isactive = 'Sanger'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    if not Pemmision(request):
        return render(request, 'RightWarning.html', locals())
    Project_model = models.PatiantSangerTable.objects.get(项目编号=project)
    Project_model.delete()
    return Index(request)

def UpdateStatus(project):
     FinalFile = project.项目路径+'/ALL.html'
     if os.path.isfile(FinalFile):
         project.任务状态 = '运行完成'
         project.最终结果 = FinalFile
         project.save()

def DownloadFile(request, file_path):
    files = open(file_path, 'rb')
    label = re.split('/', file_path)[-1]
    response = FileResponse(files)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(label)
    return response
