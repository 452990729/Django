from django.urls import path,re_path
from . import views

urlpatterns = [
    path('new', views.CreatePatiant, name="new"),
    path('<str:patiant>/', views.PatiantDetail, name='PatiantDetail'),
    path('<str:patiant>/mod/', views.ModPatiant, name='ModPatiant'),
    path('<str:patiant>/del/', views.DelPatiant, name='DelPatiant'),
    path('', views.index, name="index"),
]
