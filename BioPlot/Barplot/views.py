from django.shortcuts import render
from . import models
from .forms import PlotForm

# Create your views here.

def index(request):
    isactive = 'Barplot'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    if request.method == "POST":
        plot_form = PlotForm(request.POST)
        message = "please check in the content!"
        if plot_form.is_valid():
            x = plot_form.cleaned_data['x']
            y = plot_form.cleaned_data['y']
            hue = plot_form.cleaned_data['hue']
            orient = plot_form.cleaned_data['orient']
            ci = plot_form.cleaned_data['ci']
            title = plot_form.cleaned_data['title']
            ylim = plot_form.cleaned_data['ylim']
            figsize = plot_form.cleaned_data['figsize']
        return render(request, 'Barplot/plot.html', locals())
    plot_form = PlotForm()
    return render(request, 'Barplot/plot.html', locals())
