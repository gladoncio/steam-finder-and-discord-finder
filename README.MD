# Proyecto API para Discord y Steam

Este proyecto está dividido en dos partes: una API que permite buscar datos públicos de usuarios mediante sus IDs de Discord y Steam. A continuación se detallan los pasos para configurarlo y ejecutarlo utilizando Docker Compose.

## Configuración del Proyecto

### Clonar el Repositorio

Clona el repositorio desde la URL correspondiente y navega al directorio del proyecto.

### Cambiar Nombre del Archivo de Configuración

Renombra el archivo `docker-compose-example.yml` a `docker-compose.yml`.

### Obtener Tokens de API

Antes de continuar, asegúrate de obtener los siguientes tokens de API desde las respectivas plataformas:

- **Discord**: Necesitas un token de la aplicación creada en Discord Developer Portal.
```
https://discord.com/developers/applications
```
- **Steam**: Requiere un token obtenido en Steam Community API Key.
```
https://steamcommunity.com/dev/apikey
```

### Configurar Variables de Entorno

Abre el archivo `docker-compose.yml` y añade los tokens obtenidos como variables de entorno.

### Construir y Levantar el Contenedor Docker

Ejecuta los siguientes comandos para construir y levantar el proyecto utilizando Docker Compose:
```bash
docker-compose build
docker-compose up
```

## Uso de la API

Una vez que el contenedor esté en funcionamiento, puedes acceder a las siguientes URLs para obtener datos de usuarios:


- **Buscar usuario de Discord por ID**:
```
GET /discord-user/?discord_id=<discord_id>
```

- **Buscar usuario de Steam**:
```
POST /steam-user/
```
- **Formato Post**
```
{
     "steamID": "STEAM_0:1:62006755"
}
or
{
     "steamID": "https://steamcommunity.com/profiles/76561198084279239/"
}
or
etc...
```


## Notas Adicionales

- Asegúrate de tener Docker y Docker Compose instalados en tu sistema antes de ejecutar los comandos anteriores.
- Asegúrate de que los servicios de Discord y Steam estén accesibles desde tu red.
