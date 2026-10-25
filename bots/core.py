#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nucleo compartido del panel DM-SPAM.
Colores ANSI, banner, salida limpia al panel y utilidades comunes.
"""

import asyncio
import os
import sys

RED     = "\033[1;31m"
GREEN   = "\033[1;32m"
YELLOW  = "\033[1;33m"
BLUE    = "\033[1;34m"
MAGENTA = "\033[1;35m"
CYAN    = "\033[1;36m"
WHITE   = "\033[1;37m"
GRAY    = "\033[0;90m"
BOLD    = "\033[1m"
RESET   = "\033[0m"

ANCHO = 66
SEP = "=" * ANCHO

BANNER_LINES = [
    "██████╗ ███╗   ███╗      ███████╗██████╗  █████╗ ███╗   ███╗",
    "██╔══██╗████╗ ████║      ██╔════╝██╔══██╗██╔══██╗████╗ ████║",
    "██║  ██║██╔████╔██║█████╗███████╗██████╔╝███████║██╔████╔██║",
    "██║  ██║██║╚██╔╝██║╚════╝╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║",
    "██████╔╝██║ ╚═╝ ██║      ███████║██║     ██║  ██║██║ ╚═╝ ██║",
    "╚═════╝ ╚═╝     ╚═╝      ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝",
]

# Palabras que devuelven al panel
SALIR_TOKENS = {"salir", "exit", "quit", "0", "/salir", "q", "volver"}
SALIR_PEDIR = {"salir", "exit", "volver"}


def clear_screen():
    os.system("clear")


def banner(subtitulo=""):
    print(f"{RED}{BOLD}")
    for linea in BANNER_LINES:
        print(linea)
    print(f"{SEP}{RESET}")
    if subtitulo:
        print(f"{CYAN}{BOLD}{subtitulo.center(ANCHO)}{RESET}")
        print(f"{RED}{BOLD}{SEP}{RESET}")
    print()


def pantalla(subtitulo=""):
    clear_screen()
    banner(subtitulo)


def pedir(texto, obligatorio=True, defecto=None, permitir_salir=True):
    while True:
        valor = input(f"{GREEN}-> {texto}: {RESET}").strip()
        if permitir_salir and valor.lower() in SALIR_PEDIR:
            print(f"{RED}[-] Volviendo al panel...{RESET}")
            sys.exit(0)
        if valor:
            return valor
        if not obligatorio:
            return defecto
        print(f"{RED}[X] Este campo es obligatorio.{RESET}")


def pedir_int(texto, defecto=None, permitir_salir=True):
    while True:
        valor = input(f"{GREEN}-> {texto}: {RESET}").strip()
        if permitir_salir and valor.lower() in SALIR_PEDIR:
            print(f"{RED}[-] Volviendo al panel...{RESET}")
            sys.exit(0)
        if not valor:
            if defecto is not None:
                return defecto
            print(f"{YELLOW}[!] Campo obligatorio.{RESET}")
            continue
        try:
            return int(valor)
        except ValueError:
            print(f"{YELLOW}[!] Debe ser un numero entero.{RESET}")


async def salir(bot):
    """Cierra el bot y devuelve el control al panel."""
    print(f"\n{RED}{BOLD}[-] Volviendo al panel...{RESET}")
    try:
        await bot.close()
    except Exception:
        pass
    await asyncio.sleep(0.2)
    os._exit(0)


async def escuchar_salida(bot):
    """Escucha la consola: escribe 'salir' para volver al panel."""
    while True:
        try:
            linea = await asyncio.to_thread(input)
        except (EOFError, KeyboardInterrupt):
            await salir(bot)
            return
        if linea.strip().lower() in SALIR_TOKENS:
            await salir(bot)
            return


def instalar_salida(bot):
    """
    Registra los comandos .salir / .exit y arranca el escucha de consola.
    Se llama una sola vez desde on_ready.
    """
    from discord.ext import commands

    if getattr(bot, "_salida_instalada", False):
        return

    @bot.command(name="salir")
    @commands.is_owner()
    async def _salir_cmd(ctx):
        await salir(bot)

    @bot.command(name="exit")
    @commands.is_owner()
    async def _exit_cmd(ctx):
        await salir(bot)

    bot._salida_instalada = True
    asyncio.create_task(escuchar_salida(bot))
