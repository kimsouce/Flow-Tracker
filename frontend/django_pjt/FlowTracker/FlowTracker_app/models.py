from typing import ContextManager
from django.db import models

# Create your models here.

###################################
#  영상 InputVideo속성            #
#  1. Location (영상 촬영 지역)   #
#  2. Date (영상 촬영 날짜)       #
#  3. Owner (담당자)              #
###################################

class inputvideo(models.Model):
    location = models.CharField(max_length=100)
    date= models.DateTimeField()
    owner = models.CharField(max_length=20)

    def __str__(self):
        return self.owner

    