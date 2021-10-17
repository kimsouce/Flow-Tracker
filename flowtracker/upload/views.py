from django.shortcuts import render
from . import models
# Create your views here.
def uploadFile(request):
    if request.method == "POST":
        # Fetching the form data
        fileTitle = request.POST["fileTitle"]
        uploadedFile = request.FILES["uploadedFile"]

        # Saving the information in the database
        document = models.Document(
            title = fileTitle,
            uploadedFile = uploadedFile
        )
        document.save()

    documents = models.Document.objects.all()

#Core/upload-file.html home.html로?
    return render(request, "templates/home.html", context = {
        "files": documents
    })