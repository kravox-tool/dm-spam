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
            with open(HISTOR
