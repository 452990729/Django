from django.urls import path
from . import views

urlpatterns = [
    path('new', views.CreatePatiant, name="new"),
    path('<str:patiant>/', views.PatiantDetail, name='PatiantDetail'),
    path('<str:patiant>/mod/', views.ModPatiant, name='ModPatiant'),
    path('<str:patiant>/del/', views.DelPatiant, name='DelPatiant'),
    path('<str:patiant>/images/<str:cls>/<str:year>/<str:month>/<str:date>/<str:pic>', views.GetImage, name="GetImage"),
    path('', views.index, name="index"),
#    url('PrevData/', views.PrevData, name="PrevData"),
]
