"""flowtracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from flowtracker.views import HomeView #sy
from django.conf import settings #sy
from django.conf.urls.static import static #sy #media 가져오기 위함
from django.conf.urls import url #yolo 모델 실행
from . import views 


#urls 사용자의 요청을 어떤 view가 처리하는지 지정
#from intro import views

urlpatterns = [    
    path('admin/', admin.site.urls),
#    path('intro/', views.index, name='index')
    path('intro/', include('intro.urls')),
    #    path('dashboard/', include('dashboard.urls'))
    path('',HomeView.as_view(), name='home'),
    path('tab1/', include("tab1.urls")),
    path('photo/', include("photo.urls")),
    url(r'^yolo/$', views.startyolo, name='yolo')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
