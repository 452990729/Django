from django.conf.urls import url,include
from Barplot import views as Barplot_views

urlpatterns = [
    url(r'^$', Barplot_views.index, name="index"),
]
