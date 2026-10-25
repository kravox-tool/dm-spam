import asyncio
import json
import os
import sys
import textwrap
import urllib.request

import discord
import discord.errors
from discord.ext import commands

from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.formatted_text import ANSI, FormattedText
from prompt_toolkit.patch_stdout import patch_stdout

# ------------------------------------------------------------------
#   PALETA NEON
# ------------------------------------------------------------------
RED     = "\033[1;91m"
GREEN   = "\033[1;92m"
YELLOW  = "\033[1;93m"
BLUE    = "\033[1;94m"
MAGENTA = "\033[1;95m"
CYAN    = "\033[1;96m"
WHITE   = "\033[1;97m"
GRAY    = "\033[0;90m"
BOLD    = "\033[1m"
RESET   = "\033[0m"

ANCHO = 60

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORIAL_FILE = os.path.join(BASE_DIR, "historial_chats.json")

BANNER = (
    "██████╗ ███╗   ███╗      ███████╗██████╗  █████╗ ███╗   ███╗",
    "██╔══██╗████╗ ████║      ██╔════╝██╔══██╗██╔══██╗████╗ ████║",
    "██║  ██║██╔████╔██║█████╗███████╗██████╔╝███████║██╔████╔██║",
    "██║  ██║██║╚██╔╝██║╚════╝╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║",
    "██████╔╝██║ ╚═╝ ██║      ███████║██║     ██║  ██║██║ ╚═╝ ██║",
    "╚═════╝ ╚═╝     ╚═╝      ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝",
)

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.dm_messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)

bot.target_user_id = None
bot.target_user_obj = None


# ------------------------------------------------------------------
#   UTILIDADES DE DIBUJO
# ------------------------------------------------------------------
def clear_screen():
    os.system("clear")


def barra(color=RED):
    print_formatted_text(ANSI(f"{color}{'=' * ANCHO}{RESET}"))


def banner_rojo():
    print_formatted_text(ANSI(f"{RED}{BOLD}"))
    for linea in BANNER:
        print_formatted_text(ANSI(f"{RED}{BOLD}{linea}{RESET}"))
    barra(RED)
    print_formatted_text(ANSI(f"{WHITE}{BOLD}{'kvx :: LIVE CHAT'.center(ANCHO)}{RESET}"))
    barra(RED)


def _arriba(color=RED):
    print_formatted_text(ANSI(f"{color}╔{'═' * ANCHO}╗{RESET}"))


def _abajo(color=RED):
    print_formatted_text(ANSI(f"{color}╚{'═' * ANCHO}╝{RESET}"))


def _separador(color=RED):
    print_formatted_text(ANSI(f"{color}╠{'═' * ANCHO}╣{RESET}"))


def _fila(etiqueta="", valor="", color=RED, color_valor=WHITE):
    seg_izq = f" {etiqueta:<13}"
    seg_der = str(valor)
    disponible = ANCHO - len(seg_izq) - 1
    if len(seg_der) > disponible:
        seg_der = seg_der[:disponible]
    relleno = ANCHO - len(seg_izq) - len(seg_der)
    print_formatted_text(ANSI(
        f"{color}║{RESET}{color}{seg_izq}{RESET}"
        f"{color_valor}{seg_der}{RESET}{' ' * relleno}{color}║{RESET}"
    ))


def _envolver(texto, ancho):
    salida = []
    for parrafo in str(texto).splitlines() or [""]:
        trozos = textwrap.wrap(parrafo, ancho) or [""]
        salida.extend(trozos)
    return salida


def _carpeta_media():
    destino = "/sdcard/Download/Chat_Media/"
    if not os.path.isdir("/sdcard/Download"):
        destino = os.path.join(BASE_DIR, "Hexvox_Media")
    os.makedirs(destino, exist_ok=True)
    return destino


# ------------------------------------------------------------------
#   PANTALLAS
# ------------------------------------------------------------------
def enter_chat_layout():
    clear_screen()
    banner_rojo()
    print()
    _arriba(RED)
    _fila("", "SESION ABIERTA", RED, WHITE)
    _separador(RED)
    _fila("OBJETIVO", bot.target_user_obj.name.upper(), RED, GREEN)
    _fila("ID", str(bot.target_user_obj.id), RED, YELLOW)
    _fila("SALIR", "/salir", RED, GRAY)
    _abajo(RED)
    print()


def ver_historial_consola(user_id):
    clear_screen()
    _arriba(BLUE)
    _fila("", "REGISTRO DE CONVERSACION GUARDADA", BLUE, WHITE)
    _abajo(BLUE)

    if not os.path.exists(HISTORIAL_FILE):
        print(f"\n{YELLOW}[!] No hay historial registrado aun.{RESET}\n")
        return False

    try:
        with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        print(f"\n{RED}[X] El archivo de historial esta corrupto.{RESET}\n")
        return False

    str_id = str(user_id)
    if str_id not in data or not data[str_id].get("logs"):
        print(f"\n{YELLOW}[!] No hay registros con la ID {user_id}.{RESET}\n")
        return False

    print()
    for log in data[str_id]["logs"]:
        if "[Tu (Bot)]" in log:
            print_formatted_text(ANSI(f"  {GREEN}{log}{RESET}"))
        else:
            print_formatted_text(ANSI(f"  {YELLOW}{log}{RESET}"))
    print()
    return True


# ------------------------------------------------------------------
#   PERSISTENCIA Y DESCARGAS
# ------------------------------------------------------------------
def guardar_en_historial(user_name, user_id, remitente, mensaje):
    data = {}
    if os.path.exists(HISTORIAL_FILE):
        try:
            with open(HISTORIAL
                      def guardar_en_historial(user_name, user_id, remitente, mensaje):
    data = {}
    if os.path.exists(HISTORIAL_FILE):
        try:
            with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}

    str_id = str(user_id)
    if str_id not in data:
        data[str_id] = {"name": user_name, "logs": []}

    data[str_id]["logs"].append(f"[{remitente}]: {mensaje}")

    try:
        with open(HISTORIAL_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception:
        pass


def descargar_archivo_multimedia(url, nombre_archivo):
    try:
        carpeta = _carpeta_media()
        ruta_completa = os.path.join(carpeta, nombre_archivo)
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Linux; Android 10)"}
        )
        with urllib.request.urlopen(req) as response, open(ruta_completa, "wb") as out_file:
            out_file.write(response.read())
        return ruta_completa
    except Exception:
        return None


# ------------------------------------------------------------------
#   ENTRADA POR CONSOLA
# ------------------------------------------------------------------
async def terminal_input_loop():
    session = PromptSession()
    prompt_texto = FormattedText([("ansigreen bold", " -> Tu (Bot): ")])

    with patch_stdout():
        while True:
            try:
                user_input = await session.prompt_async(prompt_texto)
                user_input = user_input.strip()

                if not user_input:
                    continue

                if user_input == "/salir":
                    print_formatted_text(ANSI(f"\n{RED}[-] Cerrando la terminal limpiamente...{RESET}"))
                    await bot.close()
                    os._exit(0)

                if bot.target_user_obj:
                    try:
                        await bot.target_user_obj.send(content=user_input)
                        guardar_en_historial(
                            bot.target_user_obj.name,
                            bot.target_user_id,
                            "Tu (Bot)",
                            user_input
                        )
                        print("")
                    except discord.errors.Forbidden:
                        print_formatted_text(ANSI(f"\n{RED}[X] El usuario te bloqueo o cerro sus DMs.{RESET}\n"))
                    except Exception as e:
                        print_formatted_text(ANSI(f"\n{RED}[X] ERROR: {e}{RESET}\n"))

            except (KeyboardInterrupt, EOFError):
                await bot.close()
                os._exit(0)


# ------------------------------------------------------------------
#   EVENTOS
# ------------------------------------------------------------------
@bot.event
async def on_ready():
    try:
        bot.target_user_obj = await bot.fetch_user(bot.target_user_id)
        enter_chat_layout()
    except Exception:
        print_formatted_text(ANSI(f"\n{RED}[X] Error fatal: la ID provista no existe en Discord.{RESET}"))
        await bot.close()
        os._exit(0)

    asyncio.create_task(terminal_input_loop())


@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return

    if message.guild is None and message.author.id == bot.target_user_id:

        if message.content:
            _arriba(YELLOW)
            _fila("ENTRANTE", message.author.name, YELLOW, WHITE)
            _separador(YELLOW)
            for trozo in _envolver(message.content, ANCHO - 2):
                _fila("", trozo, YELLOW, WHITE)
            _abajo(YELLOW)
            print()
            guardar_en_historial(
                message.author.name,
                bot.target_user_id,
                message.author.name,
                message.content
            )

        if message.attachments:
            for adjunto in message.attachments:
                url = adjunto.url
                filename = adjunto.filename
                filename_lower = filename.lower()
                ruta_guardado = descargar_archivo_multimedia(url, filename)

                estado = f"{GREEN}descargado localmente{RESET}" if ruta_guardado else f"{RED}error al descargar{RESET}"

                if any(ext in filename_lower for ext in [".png", ".jpg", ".jpeg", ".gif", ".webp"]):
                    tipo = "IMAGEN"
                elif any(ext in filename_lower for ext in [".mp3", ".ogg", ".wav", ".m4a", ".oga"]):
                    tipo = "AUDIO / NOTA DE VOZ"
                else:
                    tipo = "ARCHIVO / DOCUMENTO"

                _arriba(MAGENTA)
                _fila(tipo, message.author.name, MAGENTA, WHITE)
                _separador(MAGENTA)
                _fila("archivo", filename, MAGENTA, CYAN)
                _fila("estado", estado, MAGENTA, WHITE)
                _fila("enlace", url, MAGENTA, GRAY)
                _abajo(MAGENTA)
                print()

                guardar_en_historial(
                    message.author.name,
                    bot.target_user_id,
                    message.author.name,
                    f"[{tipo}: {filename}]"
                )


# ------------------------------------------------------------------
#   ARRANQUE
# ------------------------------------------------------------------
def main():
    clear_screen()
    banner_rojo()
    print()

    _arriba(GREEN)
    _fila("PASO 1", "TOKEN DEL BOT", GREEN, WHITE)
    _abajo(GREEN)
    token = input(f"{GREEN} -> token: {RESET}").strip()
    if not token:
        sys.exit(1)

    _arriba(BLUE)
    _fila("PASO 2", "ID DEL USUARIO OBJETIVO", BLUE, WHITE)
    _abajo(BLUE)
    id_input = input(f"{BLUE} -> id: {RESET}").strip()
    if not id_input:
        sys.exit(1)

    try:
        bot.target_user_id = int(id_input)
    except ValueError:
        print_formatted_text(ANSI(f"\n{RED}[X] La ID debe ser un valor numerico.{RESET}"))
        sys.exit(1)

    _arriba(MAGENTA)
    _fila("PASO 3", "MODO DE SESION", MAGENTA, WHITE)
    _separador(MAGENTA)
    _fila("1", "entrar al chat en vivo", MAGENTA, WHITE)
    _fila("2", "ver historial guardado", MAGENTA, WHITE)
    _abajo(MAGENTA)

    opcion = input(f"{MAGENTA} -> Elige opcion (1 o 2): {RESET}").strip()

    if opcion == "2":
        if ver_historial_consola(bot.target_user_id):
            input(f"\n{GREEN} -> ENTER para conectar el chat en vivo...{RESET}")
        else:
            input(f"\n{GREEN} -> ENTER para continuar...{RESET}")
        clear_screen()

    print_formatted_text(ANSI(f"\n{YELLOW}[*] Conectando con los servidores de Discord...{RESET}"))

    try:
        bot.run(token)
    except discord.errors.LoginFailure:
        print_formatted_text(ANSI(f"\n{RED}[X] ERROR: token de Discord invalido o vencido.{RESET}"))
    except KeyboardInterrupt:
        print_formatted_text(ANSI(f"\n{RED}[-] Script detenido por el usuario.{RESET}"))


if __name__ == "__main__":
    main()
