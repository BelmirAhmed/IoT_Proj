from django.shortcuts import render
import datetime 
import csv
from django.utils import timezone
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import timedelta
#import telepot

from .models import Dht11
def test(request):
    return HttpResponse('Iot Project')
# Create your views here.

def table(request): 
    derniere_ligne = Dht11.objects.last()
    derniere_date = Dht11.objects.last().dt
    delta_temps = timezone.now()-derniere_date
    difference_minutes = delta_temps.seconds
    temps_ecoule = ' il y a ' + str(difference_minutes) + ' min'
    if difference_minutes > 60:
        temps_ecoule = 'il y ' + str(difference_minutes // 60) + 'h' + str(difference_minutes % 60) + 'min'
        valeurs = {'date': temps_ecoule, 'id': derniere_ligne.id, 'temp': 
    derniere_ligne.temp, 'hum': derniere_ligne.hum}
    return render(request, 'value.html', {'valeurs': valeurs})

def download_csv(request):
 model_values = Dht11.objects.all()
 response = HttpResponse(content_type='text/csv')
 response['Content-Disposition'] = 'attachment; filename="dht.csv"'
 writer = csv.writer(response)
 writer.writerow(['id', 'temp', 'hum', 'dt'])
 liste = model_values.values_list('id', 'temp', 'hum','dt')
 for row in liste: 
    writer.writerow(row)
 return response 

#pour afficher navbar de template
def index_view(request):
 return render(request, 'index.html')

#pour afficher les graphes
def graphique(request):
    return render(request, 'Chart.html')
# 
#récupérer toutes les valeur de température et humidity sous forme un #fichier json
def chart_data(request):
 dht= Dht11.objects.all()
 data = { 
 'temps': [Dt.dt for Dt in dht],
 'temperature': [Temp.temp for Temp in dht],
 'humidity': [Hum.hum for Hum in dht]
 } 
 return JsonResponse(data)
#

def chart_data_jour(request): 
 dht = Dht11.objects.all() 
 now = timezone.now() 
 # Récupérer l'heure il y a 24 heures 
 last_24_hours = now - timezone.timedelta(hours=24) 
 # Récupérer tous les objets de Module créés au cours des 24 dernières heures 
 dht = Dht11.objects.filter(dt__range=(last_24_hours, now)) 
 data = { 
            'temps': [Dt.dt for Dt in dht], 
            'temperature': [Temp.temp for Temp in dht], 
            'humidity': [Hum.hum for Hum in dht] 
        } 
 return JsonResponse(data) 

#pour récupérer les valeurs de température et humidité de dernier semaine et envoie sous forme JSON 
def chart_data_semaine(request): 
 dht = Dht11.objects.all() 
 # calcul de la date de début de la semaine dernière 
 date_debut_semaine = timezone.now().date() - datetime.timedelta(days=7) 
 print(datetime.timedelta(days=7)) 
 print(date_debut_semaine)

 # filtrer les enregistrements créés depuis le début de la semaine dernière 
 dht = Dht11.objects.filter(dt__gte=date_debut_semaine) 

 data = { 
            'temps': [Dt.dt for Dt in dht], 
            'temperature': [Temp.temp for Temp in dht], 
            'humidity': [Hum.hum for Hum in dht] 
        } 
 return JsonResponse(data) 

#pour récupérer les valeurs de température et humidité de dernier moins  et envoie sous forme JSON 
def chart_data_mois(request): 
 dht = Dht11.objects.all() 
 date_debut_semaine = timezone.now().date() - datetime.timedelta(days=30) 
 print(datetime.timedelta(days=30)) 
 print(date_debut_semaine) 
 # filtrer les enregistrements créés depuis le début de la semaine dernière 
 dht = Dht11.objects.filter(dt__gte=date_debut_semaine) 
 data = { 
            'temps': [Dt.dt for Dt in dht], 
            'temperature': [Temp.temp for Temp in dht], 
            'humidity': [Hum.hum for Hum in dht] 
        } 
 return JsonResponse(data)


def dht_tab(request):
    tab=Dht11.objects.all()
    s={'tab':tab}
    return render(request,'tables.html',s)

def sendtele():
    token = '6377504599:AAFkdgwr9dtYi0WzfJasrl6NZRT92mpJSRQ' #################### 
    rece_id = 6377504599 ########################################################
    bot = telepot.Bot(token)
    bot.sendMessage(rece_id, 'la température depasse la normale')
    print(bot.sendMessage(rece_id, 'OK.'))

