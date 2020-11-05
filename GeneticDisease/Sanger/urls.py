from django.urls import path,re_path
from . import views

urlpatterns = [
    path('index/', views.Index, name="index"),
    path('new/', views.CreateNew, name="CreateNew"),
    path('<str:project>/del/', views.DelPatiant, name='DelPatiant'),
    path('<str:project>/', views.SangerDetail, name='SangerDetail'),
    re_path('.*?(/mnt.*?/\w*.xlsx?)', views.DownloadFile, name='DownloadFile'),
    re_path('.*?(/mnt.*?/ALL.html)', views.DownloadFile, name='DownloadFile')
]
