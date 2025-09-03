from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SatelliteImageSerializer
from .models import SatelliteImage
from kafka import KafkaProducer
import json

# Create your views here.
class UploadSatelliteImage(APIView):

    def get(self, request):
        return render (request, 'upload.html')

    def post (self, request):
        serializer = SatelliteImageSerializer(data = request.data)
        print("=================================================================")
        print("FILES:", request.FILES)
        print("DATA:", request.data)
        if serializer.is_valid():
            obj = serializer.save()

            #kafka producer
            producer = KafkaProducer(
                bootstrap_servers = 'localhost:9092',
                value_serializer = lambda v: json.dumps(v).encode('utf-8')
            )
            message = {'file_path':obj.file.path}
            producer.send('satellite_topic',message)
            
            return render(request, 'upload.html', {'uploaded_url': obj.file.url, 'message': '업로드 완료!'})
        return render(request, 'upload.html', {'errors': serializer.errors})


def index_page(request):
    return render(request, 'index.html')