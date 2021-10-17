from typing import ContextManager
from django.db import models
from django.db.models.fields.json import DataContains
from django.db.models.fields.related import OneToOneField

# Intro Q & A


"""
class Defect(models.Model):
    InputVideoName = models.CharField(max_length=200)
    FilmDate = models.DateField
    Location = models.TextField
    Owner = models.TextField
    DefectYN = models.TextField

class Details(models.Model):
    VideoTime = models.ForeignKey(Defect.InputVideoName, on_delete = models.CASCADE)
    UploadDate = models.DateTimeField
    DefectNum=models.Foreignkey(Defect.DefectYN, on_delete = models.CASCADE)
"""