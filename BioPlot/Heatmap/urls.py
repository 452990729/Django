from django.conf.urls import url,include
from Heatmap import views as Heatmap_views

urlpatterns = [
    url(r'^$', Heatmap_views.index, name="index"),
]
