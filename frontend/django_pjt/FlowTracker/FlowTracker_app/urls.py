from django.urls import path

from . import views

app_name = 'FlowTracker_app'

urlpatterns = [
    path('', views.index),
    path('<int:Inputvideo_id>/', views.detail)
]