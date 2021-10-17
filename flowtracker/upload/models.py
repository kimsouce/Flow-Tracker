from django.db import models

# Create your models here.
from django.db import models

class Document(models.Model):
    title = models.CharField(max_length = 200)
    #uploadedFile = models.FileField(upload_to = "Uploaded Files/")
    uploadedFile = models.FileField(upload_to = "media/")
    dateTimeOfUpload = models.DateTimeField(auto_now = True)