from django.contrib import admin
from django.urls import path, include
#from FlowTracker_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('FlowTracker_app/', include('FlowTracker_app.urls')),
]
