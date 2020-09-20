from django.db import models
import os

# Create your models here.
Session_CHOICES = (
   ('May-June', 'MAY-JUNE'),
   ('Dec-Jan', 'DEC-JAN')
)
year_select = (
    ('2020', '2020'),
    ('2021', '2021'),
    ('2022', '2022'),
    ('2023', '2023'),
)


def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.sessionmonth, instance.year, ext)
    return os.path.join('datafile/', filename)


def time_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.sessionmonth, instance.year, ext)
    return os.path.join('timefile/', filename)


class UploadFile(models.Model):
    sessionmonth = models.CharField(max_length=11, choices=Session_CHOICES, default='May-June')
    year = models.CharField(max_length=11, choices=year_select, default='2020')
    file = models.FileField(upload_to=content_file_name)
    ttfile = models.FileField(upload_to=time_file_name, default='0000000')


class RoomCreate(models.Model):
    room_no = models.IntegerField()
    no_col = models.IntegerField()
    no_row = models.IntegerField()
    total_capacity = models.IntegerField()