# Importar las librerías necesarias
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import SteamSearchForm
import os
import validators
import urllib.request, json
from datetime import datetime
from steamid_converter import Converter
import pandas as pd

# Diccionario con las respuestas de texto
texto_respuestas = {
    'nombre_no_disponible': 'Nombre no disponible',
    'avatar_vacio': '',  # Puedes establecer aquí el enlace a una imagen predeterminada
    'url_no_disponible': '',  # Puedes establecer aquí un mensaje o un enlace alternativo
    'pais_no_disponible': 'No está disponible',
    'error_steamid_invalido': 'Error: El dato que ingreso no es valido',
    'error_steamid_no_encontrado': 'El SteamID no existe o no se pudo obtener información',
    'busqueda_exitosa': 'Se buscó la información de {nombre}',
}

# Función para detectar el tipo de dato ingresado y convertirlo a SteamID64
def detectardato(dato):
    dato = dato.strip()
    if dato.startswith("STEAM_") or dato.startswith("[U"):
        try:
            steamid64 = Converter.to_steamID64(dato, as_int=False)
            return steamid64
        except ValueError:
            return texto_respuestas['error_steamid_invalido']
    elif validators.url(dato):
        if dato.endswith("/"):
            dato = dato.rstrip(dato[-1])
        subdirname = os.path.basename(os.path.dirname(dato))
        if subdirname == "id":
            custom = os.path.basename(dato)
            url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=9D6D8348D31393D6E89D49F1C933F0E7&vanityurl={custom}"
            data = urllib.request.urlopen(url).read()
            output = json.loads(data)
            if 'response' in output and 'steamid' in output['response']:
                return output['response']['steamid']
        else:
            steamid64 = os.path.basename(dato)
            if steamid64.isdigit() and len(steamid64) == 17 and steamid64.isnumeric():
                return steamid64
    elif dato.isdigit() and len(dato) == 17 and dato.isnumeric():
        return dato

    # Si no se pudo convertir el SteamID, devolvemos un mensaje de error.
    return texto_respuestas['error_steamid_invalido']

# Función para obtener los datos de un SteamID64
def traer_datos(steamid64):
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=9D6D8348D31393D6E89D49F1C933F0E7&steamids={steamid64}"
    data = urllib.request.urlopen(url).read()
    output = json.loads(data)
    if 'players' in output['response'] and output['response']['players']:
        return output['response']['players'][0]
    return None

# Vista principal
def index(request):
    if request.method == 'POST':
        form = SteamSearchForm(request.POST)
        if form.is_valid():
            busqueda = form.cleaned_data['buscador']
            steamid64 = detectardato(busqueda)
            if steamid64.startswith("Error"):
                context = {'form': form}
                messages.error(request, texto_respuestas['error_steamid_invalido'])
                return render(request, 'index.html', context)

            steamid3 = Converter.to_steamID3(steamid64)
            steamid = Converter.to_steamID(steamid64)
            datos = traer_datos(steamid64)

            if not datos:
                context = {'form': form}
                messages.error(request, texto_respuestas['error_steamid_no_encontrado'])
                return render(request, 'index.html', context)

            nombre = datos.get('personaname', texto_respuestas['nombre_no_disponible'])
            avatar = datos.get('avatarfull', texto_respuestas['avatar_vacio'])
            url = datos.get('profileurl', texto_respuestas['url_no_disponible'])
            realname = datos.get('realname', nombre)
            time = pd.to_datetime(datos.get('timecreated', 0), unit='s')
            pais = datos.get('loccountrycode', texto_respuestas['pais_no_disponible'])

            context = {
                'form': form,
                'steamid64': steamid64,
                'steamid': steamid,
                'steamid3': steamid3,
                'nombre': nombre,
                'avatar': avatar,
                'url': url,
                'realname': realname,
                'time': time,
                'pais': pais,
            }
            mensaje_exito = texto_respuestas['busqueda_exitosa'].format(nombre=nombre)
            messages.success(request, mensaje_exito)
            return render(request, 'index.html', context)
    else:
        form = SteamSearchForm()
    context = {'form': form}
    return render(request, 'index.html', context)
