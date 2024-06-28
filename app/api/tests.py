from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class SteamIDConverterAPITests(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.url = '/steam-user/'  # Asegúrate de usar la URL correcta de tu aplicación
    
    def test_convert_steamID_to_steamID64(self):
        # Prueba con formato STEAM_0
        data_steam_0 = {"steamID": "STEAM_0:1:62006755"}
        response_steam_0 = self.client.post(self.url, data_steam_0, format='json')
        self.assertEqual(response_steam_0.status_code, status.HTTP_200_OK)
        self.assertIn('steamID', response_steam_0.data)
        self.assertIn('steamID3', response_steam_0.data)
        self.assertIn('steamID64', response_steam_0.data)
        self.assertIn('player_data', response_steam_0.data)
    
        # Prueba con formato [U:1:124013511]
        data_u_format = {"steamID": "[U:1:124013511]"}
        response_u_format = self.client.post(self.url, data_u_format, format='json')
        self.assertEqual(response_u_format.status_code, status.HTTP_200_OK)
        self.assertIn('steamID', response_u_format.data)
        self.assertIn('steamID3', response_u_format.data)
        self.assertIn('steamID64', response_u_format.data)
        self.assertIn('player_data', response_u_format.data)
    
        # Prueba con formato [76561198084279239]
        data_numeric_format = {"steamID": "76561198084279239"}
        response_numeric_format = self.client.post(self.url, data_numeric_format, format='json')
        self.assertEqual(response_numeric_format.status_code, status.HTTP_200_OK)
        self.assertIn('steamID', response_numeric_format.data)
        self.assertIn('steamID3', response_numeric_format.data)
        self.assertIn('steamID64', response_numeric_format.data)
        self.assertIn('player_data', response_numeric_format.data)
        
    def test_resolve_vanity_url(self):
        # Prueba con URL usando HTTP
        data_http = {"steamID": "http://steamcommunity.com/id/gladoslel/"}
        response_http = self.client.post(self.url, data_http, format='json')
        self.assertEqual(response_http.status_code, status.HTTP_200_OK)
        self.assertIn('steamID64', response_http.data)
        self.assertIn('player_data', response_http.data)
    
        # Prueba con URL usando HTTPS
        data_https = {"steamID": "https://steamcommunity.com/id/gladoslel/"}
        response_https = self.client.post(self.url, data_https, format='json')
        self.assertEqual(response_https.status_code, status.HTTP_200_OK)
        self.assertIn('steamID64', response_https.data)
        self.assertIn('player_data', response_https.data)
        
    def test_resolve_url(self):
        data = {"steamID": "https://steamcommunity.com/profiles/76561198084279239/"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('steamID64', response.data)
        self.assertIn('player_data', response.data)

    def test_resolve_name(self):
        data = {"steamID": "gladoslel"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('steamID64', response.data)
        self.assertIn('player_data', response.data)
        
    def test_no_data(self):
        data = {"steamID": "gladosleldadada"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)  # Verificar si hay un campo 'error' en la respuesta
        
    def test_empty_data(self):
        data = {}  # No proporcionar ningún dato
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)  # Verificar si hay un campo 'error' en la respuesta
