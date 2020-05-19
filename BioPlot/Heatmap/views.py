from django.shortcuts import render

# Create your views here.

def index(request):
    isactive = 'Heatmap'
    return render(request, 'Heatmap/plot.html')
