from django.db import models


class WES(models.Model):
    user = models.CharField(max_length=256)
    category = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    project = models.CharField(max_length=128,unique=True)
    info = models.CharField(max_length=256)
    platform = models.CharField(max_length=32,choices=(('SGE','SGE'), ('local', 'local')),default='SGE')
    cores = models.CharField(max_length=256)
    c_time = models.DateTimeField(auto_now_add=True)
    outpath = models.CharField(max_length=256)
    status = models.CharField(max_length=256)
    def __str__(self):
        return self.project
    class Meta:
        ordering = ['c_time']
