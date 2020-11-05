from django.urls import path,re_path
from . import views

urlpatterns = [
    path('<str:project>/', views.ProjectDetail, name='ProjectDetail'),
    re_path('.*?(/mnt.*?/\w*.xlsx?)', views.DownloadFile, name='DownloadFile'),
    re_path('.*?(/mnt.*?/ALL.html)', views.DownloadFile, name='DownloadFile'),
    re_path('.*?(/images.*?/\w*.*)', views.DownloadFile, name='DownloadFile'),
    re_path('.*?(Reports.*?/\w*.*)', views.DownloadFile, name='DownloadFile'),
    path('', views.Index, name="index"),
]
