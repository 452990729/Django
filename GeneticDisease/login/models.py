from django.db import models
from django.contrib.auth.models import User


class LoginUser(User):
    info_right = models.CharField(max_length=32,choices=(('yes', 'yes'), ('no', 'no')),default='no')
    sanger_right = models.CharField(max_length=32,choices=(('yes', 'yes'), ('no', 'no')),default='no')
    wes_right = models.CharField(max_length=32,choices=(('yes', 'yes'), ('no', 'no')),default='no')
    report_right = models.CharField(max_length=32,choices=(('yes', 'yes'), ('no', 'no')),default='no')
