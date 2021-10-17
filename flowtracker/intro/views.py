from django.shortcuts import render

# HttpResponse : 웹 요청에 결과를 http 형식으로 return
from django.http import HttpResponse


#Create your views here.
# def index(request):
#    text_var = "Welcome to 하수관로 결함탐지 서비스 'Flow Tracker'!!"
#    return HttpResponse(text_var)


def index(request):
	return render(request, 'intro/index.html')

# intro 에 대한 요청이 오면 text_var의 내용을 httpResponse 형식으로 출력