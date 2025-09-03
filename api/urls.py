from django.urls import path
from .views import UploadSatelliteImage
from .views import index_page

urlpatterns = [
    path('upload/', UploadSatelliteImage.as_view(), name= 'upload-satellite'),
    path('',index_page, name = 'index_page'),
]


