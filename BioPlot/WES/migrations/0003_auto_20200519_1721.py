# Generated by Django 2.2 on 2020-05-19 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WES', '0002_wes_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='wes',
            name='category',
            field=models.CharField(default='Pipeline', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wes',
            name='name',
            field=models.CharField(default='WES', max_length=256),
            preserve_default=False,
        ),
    ]
