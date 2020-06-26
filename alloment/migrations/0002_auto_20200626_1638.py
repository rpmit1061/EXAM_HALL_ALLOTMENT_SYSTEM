# Generated by Django 3.0.7 on 2020-06-26 11:08

import alloment.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alloment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadfile',
            name='ttfile',
            field=models.FileField(default='0000000', upload_to=alloment.models.time_file_name),
        ),
        migrations.AlterField(
            model_name='uploadfile',
            name='file',
            field=models.FileField(upload_to=alloment.models.content_file_name),
        ),
        migrations.AlterField(
            model_name='uploadfile',
            name='sessionmonth',
            field=models.CharField(choices=[('May-June', 'MAY-JUNE'), ('Dec-Jan', 'DEC-JAN')], default='May-June', max_length=11),
        ),
        migrations.AlterField(
            model_name='uploadfile',
            name='year',
            field=models.CharField(choices=[('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023')], default='2020', max_length=11),
        ),
    ]
