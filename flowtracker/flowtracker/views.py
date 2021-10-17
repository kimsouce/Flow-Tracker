from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import AccessMixin
from django.views.defaults import permission_denied

# 하은추가 0917
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

#--TemplateView
class HomeView(TemplateView):
    template_name='home.html'

#믹스인 클래스 #object 편집 기능용
class OwnerOnlyMixin(AccessMixin):
    raise_exception = True
    permission_denied_message = "Owner only can update/delete the object"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.owner:
            self.handle_no_permission()
        return super().get(request, *args, **kwargs)

#yolo 모델 실행
import subprocess

def startyolo(request):
    if request.POST:
        # give the absolute path to your `text4midiAllMilisecs.py`
        # and for `tiger.mid`
        # subprocess.call(['python', '/path/to/text4midiALLMilisecs.py', '/path/to/tiger.mid'])
        subprocess.call('/home/blushy/flowtracker/analyze.sh')
        #subprocess.call('/home/blushy/yolov5/yolov5-master/detect.sh')

    return render(request,'home.html',{})
