#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nucleo compartido del panel DM-SPAM.
Colores ANSI, banner, salida limpia al panel, prompts neon y utilidades.
"""

import asyncio
import os
import sys

import discord

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

# Paleta neon para textos de pregunta (multicolor)
NEON = [RED, MAGENTA, YELLOW, GREEN, CYAN, BLUE]

# Palabras que devuelven al panel
SALIR_TOKENS = {"salir", "exit", "quit", "0", "/salir", "q", "volver"}
SALIR_PEDIR = {"salir", "exit", "volver"}


def neon(texto):
    """Pinta el texto caracter por caracter con la paleta neon."""
    if not texto:
        return ""
    piezas = []
    for i, ch in enumerate(texto):
        piezas.append(NEON[i % len(NEON)])
        piezas.append(ch)
    piezas.append(RESET)
    return "".join(piezas)


def titulo(texto):
    """Imprime un titulo de seccion en neon."""
    print(f"\n{neon(texto)}{RESET}")


def clear_screen():
    os.system("clear")


def banner(subtitulo=""):
    print(f"{RED}{BOLD}")
    for linea in BANNER_LINES:
        print(linea)
    print(f"{SEP}{RESET}")
    if subtitulo:
        print(f"{neon(subtitulo.center(ANCHO))}")
        print(f"{RED}{BOLD}{SEP}{RESET}")
    print()


def pantalla(subtitulo=""):
    clear_screen()
    banner(subtitulo)


def pedir(texto, obligatorio=True, defecto=None, permitir_salir=True):
    while True:
        prompt = f"{neon('-> ')}{neon(texto)}{neon(': ')}"
        valor = input(prompt).strip()
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
        prompt = f"{neon('-> ')}{neon(texto)}{neon(': ')}"
        valor = input(prompt).strip()
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
    """Registra .salir / .exit y arranca el escucha de consola (una sola vez)."""
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


# ---------------------------------------------------------------------------
#  UTILIDADES DE ENVIO
# ---------------------------------------------------------------------------

async def enviar_dm(destino, texto, reintentos=3):
    """
    Envia un DM con reintentos ante rate limit.
    Devuelve True si se entrego, False si el usuario tiene los DMs cerrados
    o hubo un error definitivo.
    """
    for intento in range(reintentos):
        try:
            await destino.send(texto)
            return True
        except discord.errors.Forbidden:
            return False
        except discord.errors.HTTPException as e:
            if e.status == 429:
                espera = float(getattr(e, "retry_after", 2)) + 0.5
                await asyncio.sleep(espera)
                continue
            return False
        except Exception:
            await asyncio.sleep(1)
    return False


async def obtener_miembros(guild, incluir_bots=False):
    """
    Devuelve la lista de miembros del servidor.
    Primero por HTTP (fetch_members), y si falla, desde la cache tras chunk().
    """
    miembros = []

    # 1) Via HTTP: la forma confiable, no depende de la cache
    try:
        async for m in guild.fetch_members(limit=None):
            if incluir_bots or not m.bot:
                miembros.append(m)
        if miembros:
            return miembros
    except Exception:
        pass

    # 2) Fallback: cache local
    try:
        await guild.chunk()
    except Exception:
        pass

    return [m for m in guild.members if incluir_bots or not m.bot]
