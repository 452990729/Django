from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.PatiantInfo)
admin.site.register(models.PatiantPhoto)
admin.site.register(models.PatiantPathology)
admin.site.register(models.PatiantInformation)
