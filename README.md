# DM-SPAM

Terminal de control para Discord en Termux.

```
██████╗ ███╗   ███╗      ███████╗██████╗  █████╗ ███╗   ███╗
██╔══██╗████╗ ████║      ██╔════╝██╔══██╗██╔══██╗████╗ ████║
██║  ██║██╔████╔██║█████╗███████╗██████╔╝███████║██╔████╔██║
██║  ██║██║╚██╔╝██║╚════╝╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║
██████╔╝██║ ╚═╝ ██║      ███████║██║     ██║  ██║██║ ╚═╝ ██║
╚═════╝ ╚═╝     ╚═╝      ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝
```

## Modulos

| # | Modulo | Descripcion |
|---|--------|-------------|
| 1 | DM-SPAM | Rafaga masiva de mensajes directos a una ID |
| 2 | CHAT | Chat en vivo por consola + historial + descarga de adjuntos |

## Instalacion en Termux

```bash
pkg update -y && pkg install -y git python
git clone https://github.com/dm-spam.git
cd dm-spam
bash install.sh
```

## Uso

```bash
python dm-spam.py
# o
bash run.sh
```

## Requisitos en el Discord Developer Portal

Activa estos intents en tu aplicacion:

- MESSAGE CONTENT INTENT
- SERVER MEMBERS INTENT
- PRESENCE INTENT (opcional)

## Modulo 1 - DM-SPAM

Pide por consola: token, ID objetivo, mensaje y cantidad. Al conectar dispara la rafaga automaticamente.

Comando extra dentro de Discord (solo el owner del bot):

```
.idnuke <ID>
```

## Modulo 2 - CHAT

Abre un chat en vivo por consola con el usuario indicado.

- `/salir` cierra la sesion limpiamente
- Guarda historial en `historial_chats.json`
- Descarga imagenes, audios y documentos en `/sdcard/Download/Hexvox_Media/`

## Notas

- En `spam_bot.py` existe la constante `REINICIAR_AL_TERMINAR`. Con `True` el script se reinicia al acabar la rafaga; con `False` el bot queda vivo y puedes reusar `.idnuke`.
- La interfaz no usa emojis para evitar desalineaciones de ancho en Termux.
- Ejecuta `termux-setup-storage` la primera vez para permitir la carpeta de descargas.

## Licencia

MIT
