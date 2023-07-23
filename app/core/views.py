from django.shortcuts import render
from .forms import *
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
import requests
from django.views import View
from .forms import *
from django.views.decorators.csrf import csrf_exempt
import os
import validators
import urllib.request, json
from datetime import datetime
import requests
from steamid_converter import Converter
import pandas as pd


def detectardato(dato):
    dato = dato.strip()
    if dato.startswith("STEAM_") or dato.startswith("[U"):
        steamid64 = Converter.to_steamID64(dato, as_int=False)
        return steamid64
    elif validators.url(dato):
        if dato.endswith("/"):
            dato = dato.rstrip(dato[-1])
        subdirname = os.path.basename(os.path.dirname(dato))
        if subdirname=="id":
            custom = os.path.basename(dato)
            url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=9D6D8348D31393D6E89D49F1C933F0E7&vanityurl={custom}"
            data = urllib.request.urlopen(url).read()
            output = json.loads(data)
            return output['response']['steamid']
        else:
            steamid64 = os.path.basename(dato)
            return steamid64
    elif len(dato)==17:
        return dato
    else:
        return "No"

def traer_datos(id):
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=9D6D8348D31393D6E89D49F1C933F0E7&steamids={id}"
    data = urllib.request.urlopen(url).read()
    output = json.loads(data)
    array = output['response']['players'][0]
    return array


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = steamsearch(request.POST)
        if form.is_valid():
            busqueda = form.cleaned_data['buscador']
            steamid64 = detectardato(busqueda)
            if steamid64=="No":
                context = {'form' : form}
                messages.success(request, f'El dato que ingreso no es correcto')
                return render(request, 'index.html', context)
            steamid3 = Converter.to_steamID3(steamid64)
            steamid = Converter.to_steamID(steamid64)
            datos = traer_datos(steamid64)
            nombre = datos['personaname']
            avatar = datos['avatarfull']
            url = datos['profileurl']
            try:
                realname = datos['realname']
            except:
                realname = nombre
            time = datos['timecreated']
            time = pd.to_datetime(time, unit='s')
            try:
                pais = datos['loccountrycode']
            except:
                pais = "No Esta disponible"
            context = {'form' : form, 'steamid64' : steamid64, 'steamid' : steamid, 'steamid3' : steamid3
            , 'nombre' : nombre,'avatar' : avatar,'url' : url,
            'realname' : realname, 'time' : time,'pais' : pais}
            messages.success(request, f'Se Busco la info de {nombre}')
            return render(request, 'index.html', context)
    else:
        form = steamsearch()
        context = {'form' : form}
    return render(request, 'index.html', context)