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
    isactive = 'Project'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    return render(request, 'Unfinish.html', locals())

def DownloadFile(request, file_path):
    if file_path.startswith('/images'):
        fl_path = settings.BASE_DIR+file_path
    if file_path.startswith('Reports'):
        fl_path = settings.BASE_DIR+file_path
    files = open(fl_path, 'rb')
    label = re.split('/', file_path)[-1]
    response = FileResponse(files)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(label)
    return response
