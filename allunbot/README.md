<h1 align="center"><img src="https://raw.githubusercontent.com/Deipzza/ppi_02/main/icon_large.png" width="300"></h1>

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://github.com/Deipzza/ppi_02/blob/main/LICENSE.md)

## Usar AllUNBot

Para poner utilizar los servicios de **AllUNBot** debes:

1. Buscar en telegram [@allun_dev_bot](https://telegram.me/allun_dev_bot)

2. Inicia el chat con el comando /start

---

## Usarlo localmente

1. Ejecuta el archivo build.sh en consola.

2. Descargue [ngrok](https://ngrok.com/download)

3. Descomprimir el archivo y pongan el .exe en la carpeta allunbot.

4. Ejecute el comado
```cmd
ngrok http 10000
```

5. Cree un archivo .env que contenga:
    
    "BOT_TOKEN": es el token generado por botfather.
    
    "URL": ingrese el valor del *Forwarding* generado por paso anterior.

6. Inicia el bot ejecutando el archivo bot.py

7. Envie un mensaje a su bot


