#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MASIVO :: Envia un mensaje personalizado N veces a todos los usuarios de un servidor.
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import discord
from discord.ext import commands
import core

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=".", intents=intents)

bot.guild_id = None
bot.mensaje_ataque = ""
bot.veces = 1
bot.incluir_bots = False
bot._salida_instalada = False
bot._lanzado = False


async def lanzar_masivo():
    try:
        guild = bot.get_guild(bot.guild_id) or await bot.fetch_guild(bot.guild_id)
    except Exception:
        print(f"\n{core.RED}{core.BOLD}[X] No se encontro el servidor con esa ID.{core.RESET}")
        await asyncio.sleep(3)
        await core.salir(bot)
        return

    try:
        await guild.chunk()
    except Exception:
        pass

    miembros = [m for m in guild.members if (bot.incluir_bots or not m.bot) and m.id != bot.user.id]

    print(f"\n{core.RED}{core.BOLD}{core.SEP}")
    print(f"[>] SERVIDOR: {guild.name.upper()} ({guild.id})")
    print(f"[>] MIEMBROS OBJETIVO: {len(miembros)}")
    print(f"[>] MENSAJES POR USUARIO: {bot.veces}")
    print(f"{core.SEP}{core.RESET}\n")

    ok, fallidos, enviados = 0, 0, 0

    for i, miembro in enumerate(miembros, 1):
        entrego = True
        for _ in range(bot.veces):
            try:
                await miembro.send(bot.mensaje_ataque)
                enviados += 1
            except discord.errors.Forbidden:
                entrego = False
                break
            except Exception:
                pass

        if entrego:
            ok += 1
            estado = f"{core.GREEN}OK{core.RESET}"
        else:
            fallidos += 1
            estado = f"{core.YELLOW}DMs cerrados{core.RESET}"

        print(f"{core.GREEN}[+] [{i}/{len(miembros)}] {miembro.name} -> {estado}")
        await asyncio.sleep(0.5)

    print(f"\n{core.GREEN}{core.BOLD}{core.SEP}")
    print(f"[OK] FINALIZADO | Alcanzados: {ok} | Fallidos: {fallidos} | Mensajes: {enviados}")
    print(f"{core.SEP}{core.RESET}")

    await asyncio.sleep(3)
    await core.salir(bot)


@bot.event
async def on_ready():
    core.instalar_salida(bot)
    print(f"\n{core.GREEN}{core.BOLD}[OK] CONECTADO COMO: {bot.user.name.upper()}{core.RESET}")
    print(f"{core.GRAY}[*] Escribe 'salir' para volver al panel.{core.RESET}")

    if not bot._lanzado:
        bot._lanzado = True
        asyncio.create_task(lanzar_masivo())


def main():
    core.pantalla("MASIVO :: TODO EL SERVIDOR")

    print(f"{core.BLUE}{core.BOLD}[ CONFIGURACION DE CONEXION ]{core.RESET}")
    token = core.pedir("Coloca el token del bot")

    print(f"\n{core.BLUE}{core.BOLD}[ CONFIGURACION DEL SERVIDOR ]{core.RESET}")
    bot.guild_id = core.pedir_int("Coloca la ID del servidor")

    print(f"\n{core.BLUE}{core.BOLD}[ CONFIGURACION DEL MENSAJE ]{core.RESET}")
    bot.mensaje_ataque = core.pedir("Escribe tu mensaje personalizado", permitir_salir=False)

    print(f"\n{core.BLUE}{core.BOLD}[ CONFIGURACION DE CANTIDAD ]{core.RESET}")
    bot.veces = core.pedir_int("Cuantos mensajes por usuario? (ENTER = 1)", defecto=1)

    print(f"\n{core.BLUE}{core.BOLD}[ OPCIONES ]{core.RESET}")
    inc = input(f"{core.GREEN}-> Incluir bots tambien? (s/N): {core.RESET}").strip().lower()
    bot.incluir_bots = inc == "s"

    print(f"\n{core.YELLOW}{core.BOLD}{core.SEP}")
    print("[*] Validando parametros y estableciendo conexion...")
    print(f"{core.SEP}{core.RESET}")
    print(f"{core.GRAY}[*] Escribe 'salir' en cualquier momento para volver al panel.{core.RESET}")

    try:
        bot.run(token)
    except discord.errors.LoginFailure:
        print(f"\n{core.RED}{core.BOLD}[X] ERROR: El token ingresado es incorrecto o expiro.{core.RESET}")
        input(f"{core.GRAY}ENTER para volver al panel...{core.RESET}")
    except KeyboardInterrupt:
        print(f"\n{core.RED}{core.BOLD}[-] Script cerrado por el usuario.{core.RESET}")


if __name__ == '__main__':
    main()
