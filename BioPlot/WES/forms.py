from django import forms
from captcha.fields import CaptchaField


class WESForm(forms.Form):
    config = forms.CharField(label="input file config",max_length=500,widget=forms.Textarea(attrs={'class': 'form-control'}), help_text='sample\tgroup\tfq1,fq2\nif you have upload th fastq file ,please write the absulte path of fq, else upload fastq below and only write the fasrq file names', initial='#sample\tgroup\tfastq1.gz,fastq2.gz')
    config_file = forms.FileField(label="upload config file", allow_empty_file=True, required=False, initial='')
    fastq_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label="upload fastq file", allow_empty_file=True,required=False, initial='')
    project = forms.CharField(label="project name", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}), help_text='project name', initial='prj1')
    info = forms.CharField(label="project information", max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}), initial='human')
    platform = forms.ChoiceField(label='platform', choices=(('SGE','SGE'), ('local','local')), initial='SGE')
    cores = forms.CharField(label="parallel cores", max_length=2, widget=forms.TextInput(attrs={'class': 'form-control'}), initial='4')
