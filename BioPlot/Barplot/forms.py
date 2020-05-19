from django import forms
from captcha.fields import CaptchaField


class PlotForm(forms.Form):
    data = forms.CharField(label="input data",max_length=500,widget=forms.Textarea(attrs={'class': 'form-control'}))
    data_file = forms.FileField(label="")
    x = forms.CharField(label="x", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    y = forms.CharField(label="y", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    hue = forms.CharField(label="hue", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}), initial='')
    orient = forms.ChoiceField(label='orient', choices=(('horizontal','h'), ('vertical','v')))
    ci = forms.CharField(label="ci", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}), initial='')
    title = forms.CharField(label="title", max_length=40, widget=forms.TextInput(attrs={'class': 'form-control'}), initial='')
    ylim = forms.CharField(label="ylim", max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}), initial='', help_text='ymin:ymax')
    figsize = forms.CharField(label="figsize", max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}), initial='12:10', help_text='width:height')

