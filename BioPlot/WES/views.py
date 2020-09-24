import os
import re
from glob import glob
from django.shortcuts import render
from . import models
from .forms import WESForm

# Create your views here.

def index(request):
    isactive = 'WES'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    if request.method == "POST":
        wes_form = WESForm(request.POST, request.FILES)
        message = "please check in the content!"
        if wes_form.is_valid():
            config = wes_form.cleaned_data['config']
            config_file = request.FILES.getlist('config_file')
            fastq_file = request.FILES.getlist('fastq_file')
            project = wes_form.cleaned_data['project']
            info = wes_form.cleaned_data['info']
            platform = wes_form.cleaned_data['platform']
            cores = wes_form.cleaned_data['cores']
            same_name_project = models.WES.objects.filter(project = 'WES_'+project)
            if same_name_project:
                message = 'project already exists, please re-select project'
                return render(request, 'Wes/index.html', locals())
            ProjectPath = HandleWES(config, config_file, fastq_file, project, info, platform, cores, )
            new_project = models.WES.objects.create()
            new_project.user = request.user.username
            new_project.category  = 'Pipeline'
            new_project.name = 'WES'
            new_project.project = 'WES_'+project
            new_project.info = info
            new_project.platform = platform
            new_project.cores = cores
            new_project.outpath = ProjectPath
            new_project.status = 'Submitted'
            new_project.save()
            return render(request, 'JobLoad.html', locals())
        return render(request, 'Wes/index.html', locals())
    wes_form = WESForm()
    return render(request, 'Wes/index.html', locals())

def HandleWES(config, config_file, fastq_file, project, info, platform, cores, ):
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
    print(fastq_file)
    if len(fastq_file) > 0:
        UploadFile(fastq_file, RawDataPath)
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
