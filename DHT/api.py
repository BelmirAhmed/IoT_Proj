import genericpath
from typing import Generic
from .models import Dht11 
from .serializers import DHT11serialize
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status, generics
@api_view(["GET","POST"]) 
def dhtser (request): 
    if request.method=="GET":
        all=Dht11.objects.all()
        dataSer=DHT11serialize(all,many=True) # les donnée se form fichier JSON
        return Response(dataSer.data)
    elif request.method=="POST":
        serial=DHT11serialize(data=request.data)
        if serial.is_valid():
            serial.save()
            derniere_temperature = Dht11.objects.last().temp 
            print(derniere_temperature)
            if (derniere_temperature > 10): 
                subject = 'Alerte'
                message = 'Il y a une alerte importante sur votre Capteur la température dépasse le seuil' 
                email_from = settings.EMAIL_HOST_USER 
                recipient_list = ['med88mir@gmail.com'] 
                send_mail(subject, message, email_from, recipient_list)
                # Alertwhatsapp 
                
            return Response(serial.data, status=status.HTTP_201_CREATED)
        else: 
            return Response(serial.id, status=status.HTTP_400_CREATED)

####
@api_view(['GET'])
def Dlist(request):
    all_data = Dht11.objects.all()
    data = DHT11serialize(all_data, many=True).data
    return Response({'data': data})

class Dhtviews(generics.CreateAPIView):
    queryset = Dht11.objects.all()
    serializer_class = DHT11serialize
