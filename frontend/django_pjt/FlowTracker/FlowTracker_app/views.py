from django.shortcuts import render
#from django.http import HttpResponse
from .models import inputvideo


# Create your views here.
def index(request):
    text_var="Flow Tracker : 하수관로 결함 탐지 서비스"
    
    """
    Flow Tracker 목록 출력
    """
    InputVideo_list = inputvideo.objects.order_by('-create_date')
    context = {'InputVideo_list' : InputVideo_list}

    return render(request, 'FlowTracker_app/InputVideo_list.html', context)

def detail(request, InputVideo_id):
    """
    Flow Tracker 내용 출력
    """
    location = inputvideo.objects.get(id=InputVideo_id)
#    date = {'촬영 날짜' : date}
    return render(request, 'FlowTracker_app/InputVideo_detail.html', context)
