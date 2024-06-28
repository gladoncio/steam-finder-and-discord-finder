import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import re
import arrow

class Converter:
    @staticmethod
    def to_steamID(steamID):
        if isinstance(steamID, int):
            steamID64 = steamID
        elif isinstance(steamID, str) and steamID.isdigit() and len(steamID) == 17:
            steamID64 = int(steamID)
        else:
            raise ValueError("Invalid SteamID format")
        
        y = steamID64 % 2
        z = (steamID64 - 76561197960265728) // 2
        return f'STEAM_0:{y}:{z}'

    @staticmethod
    def to_steamID3(steamID):
        if isinstance(steamID, int):
            steamID64 = steamID
        elif isinstance(steamID, str) and steamID.isdigit() and len(steamID) == 17:
            steamID64 = int(steamID)
        else:
            raise ValueError("Invalid SteamID format")
        
        z = steamID64 - 76561197960265728
        return f'[U:1:{z}]'

    @staticmethod
    def to_steamID64(steamID, as_int=False):
        if isinstance(steamID, int):
            steamID64 = steamID
        elif isinstance(steamID, str):
            if steamID.isdigit() and len(steamID) == 17:
                steamID64 = int(steamID)
            elif re.match(r'^STEAM_0:[01]:\d+$', steamID):
                parts = steamID.split(':')
                steamID64 = int(parts[2]) * 2 + 76561197960265728 + int(parts[1])
            elif re.match(r'^\[U:1:\d+\]$', steamID):
                steamID64 = int(steamID[5:-1]) + 76561197960265728
            elif re.match(r'^https?://steamcommunity\.com/profiles/\d+/?$', steamID):
                steamID64 = int(re.findall(r'\d+', steamID)[0])
            elif re.match(r'^https?://steamcommunity\.com/id/[^/]+/?$', steamID):
                vanity_url = re.findall(r'https?://steamcommunity\.com/id/([^/]+)/?$', steamID)[0]
                steamID64 = Converter.resolve_vanity_url(vanity_url)
            else:
                # Assume the input is a Vanity URL identifier
                steamID64 = Converter.resolve_vanity_url(steamID)
        else:
            raise ValueError("Invalid SteamID format")
        
        return steamID64 if as_int else str(steamID64)

    @staticmethod
    def resolve_vanity_url(vanity_url):
        steam_token = settings.STEAM_TOKEN
        url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={steam_token}&vanityurl={vanity_url}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['response']['success'] == 1:
            return data['response']['steamid']
        else:
            raise ValueError("Invalid Vanity URL")

class SteamIDConverter(APIView):
    def post(self, request):
        steamID = request.data.get('steamID')
        steam_token = settings.STEAM_TOKEN
        
        try:
            if not steamID:
                raise ValueError("No steamID provided")

            steamID64 = None

            # Determinar el tipo de steamID y convertirlo a steamID64
            if re.match(r'^STEAM_0:[01]:\d+$', steamID):
                parts = steamID.split(':')
                steamID64 = int(parts[2]) * 2 + 76561197960265728 + int(parts[1])
            elif re.match(r'^\[U:1:\d+\]$', steamID):
                steamID64 = int(steamID[5:-1]) + 76561197960265728
            elif steamID.isdigit() and len(steamID) == 17:
                steamID64 = int(steamID)
            elif re.match(r'^https?://steamcommunity\.com/profiles/\d+/?$', steamID):
                steamID64 = int(re.findall(r'\d+', steamID)[0])
            elif re.match(r'^https?://steamcommunity\.com/id/[^/]+/?$', steamID):
                vanity_url = re.findall(r'https?://steamcommunity\.com/id/([^/]+)/?$', steamID)[0]
                steamID64 = Converter.resolve_vanity_url(vanity_url)
            elif re.match(r'^gladoslel$', steamID):  # Ejemplo específico, adaptar según tus necesidades
                vanity_url = steamID  # Suponiendo que 'gladoslel' es un ejemplo de vanity URL
                steamID64 = Converter.resolve_vanity_url(vanity_url)
            else:
                raise ValueError("Invalid SteamID format")

            if steamID64 is None:
                raise ValueError("Invalid SteamID format")

            # Obtener datos del usuario desde la API de Steam
            url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steam_token}&steamids={steamID64}"
            response = requests.get(url)
            response.raise_for_status()  # Lanzará una excepción si la respuesta no tiene éxito
            data = response.json()

            if 'response' in data and 'players' in data['response'] and data['response']['players']:
                player_data = data['response']['players'][0]

                # Convertir SteamID a diferentes formatos
                steamID_converted = Converter.to_steamID(steamID64)
                steamID3_converted = Converter.to_steamID3(steamID64)

                result = {
                    "steamID": steamID_converted,
                    "steamID3": steamID3_converted,
                    "steamID64": steamID64,
                    "player_data": player_data
                }

                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No player data found"}, status=status.HTTP_404_NOT_FOUND)
        
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Request Exception: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ve:
            return Response({"error": f"ValueError: {str(ve)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({"error": f"Internal Server Error: {str(ex)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def convert_id_to_unix(id):
    id = int(id) >> 22  # Shift y ajuste para obtener los primeros 42 bits
    unix_time = id + 1420070400000  # Fecha base en milisegundos (1420070400000)
    return unix_time

class DiscordUserView(APIView):
    def get(self, request):
        discord_id = request.query_params.get('discord_id')
        if not discord_id:
            return Response({"error": "Discord ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        discord_token = settings.DISCORD_TOKEN
        headers = {
            'Authorization': f'Bot {discord_token}',
        }
        url = f'https://discord.com/api/v10/users/{discord_id}'
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            if 'avatar' in data and data['avatar'] is not None:
                data['avatar_url'] = f'https://cdn.discordapp.com/avatars/{discord_id}/{data["avatar"]}.png?size=1024'

            if 'banner' in data and data['banner'] is not None:
                data['banner_url'] = f'https://cdn.discordapp.com/banners/{discord_id}/{data["banner"]}.gif?size=1024'

            if 'premium_type' in data:
                if data['premium_type'] == 1:
                    data['nitro'] = 'Nitro Classic'
                elif data['premium_type'] == 2:
                    data['nitro'] = 'Nitro'
                else:
                    data['nitro'] = 'None'

            # Convertir el ID de Discord a fecha usando la función convert_id_to_unix
            if 'id' in data:
                discord_id_unix = convert_id_to_unix(data['id'])
                timestamp = arrow.get(discord_id_unix / 1000)  # Convertir a segundos para Arrow

                # Agregar las fechas formateadas al diccionario de salida
                data['discord_id_unix'] = discord_id_unix
                data['discord_id_date24'] = timestamp.format('YYYY-MM-DD, HH:mm:ss')
                data['discord_id_date12'] = timestamp.format('YYYY-MM-DD, h:mm:ss A')
                data['discord_id_timezone'] = timestamp.format('ZZ')
                data['discord_id_timeago'] = timestamp.humanize()

            return Response(data, status=status.HTTP_200_OK)
        
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)