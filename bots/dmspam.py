#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DM-SPAM :: Rafaga masiva de mensajes directos a una ID.
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

bot.cantidad_mensajes = 0
bot.mensaje_ataque = ""
bot.target_id_consola = None
bot._salida_instalada = False
bot._lanzado = False


async def ejecutar_ataque_id(target_id, ctx=None):
    try:
        target_user = await bot.fetch_user(target_id)
    except Exception:
        print(f"\n{core.RED}{core.BOLD}[X] ERROR: El bot no encuentra a ese usuario o la ID es invalida.{core.RESET}")
        if ctx:
            await ctx.send("[X] ID de usuario invalida o el bot no comparte servidores.")
        await asyncio.sleep(3)
        await core.salir(bot)
        return

    print(f"\n{core.RED}{core.BOLD}{core.SEP}")
    print(f"[>] OBJETIVO: {target_user.name.upper()} ({target_user.id})")
    print(f"{core.SEP}{core.RESET}")

    if ctx:
        await ctx.send(f"[>] Iniciando protocolo DM-SPAM en {target_user.name}...")
    print(f"{core.YELLOW}[*] Inyectando rafagas al mensaje privado...{core.RESET}\n")

    enviados = 0
    for i in range(bot.cantidad_mensajes):
        try:
            await target_user.send(content=bot.mensaje_ataque)
            enviados += 1
            print(f"{core.GREEN}[+] [{enviados}/{bot.cantidad_mensajes}] Enviado exitosamente.{core.RESET}")
            await asyncio.sleep(0.0)
        except discord.errors.Forbidden:
            print(f"\n{core.RED}{core.BOLD}[X] CANCELADO: bloqueo al bot o DMs cerrados.{core.RESET}")
            break
        except Exception:
            pass

    print(f"\n{core.GREEN}{core.BOLD}{core.SEP}")
    print(f"[OK] RAFAGA FINALIZADA. TOTAL ENVIADOS: {enviados}")
    print(f"{core.SEP}{core.RESET}")

    if ctx:
        await ctx.send(f"[OK] Ataque finalizado. Mensajes enviados: {enviados}")

    await asyncio.sleep(3)
    await core.salir(bot)


@bot.event
async def on_ready():
    core.instalar_salida(bot)
    print(f"\n{core.GREEN}{core.BOLD}[OK] CONECTADO COMO: {bot.user.name.upper()}{core.RESET}")
    print(f"{core.GRAY}[*] Escribe 'salir' para volver al panel.{core.RESET}")

    if not bot._lanzado:
        bot._lanzado = True
        if bot.target_id_consola:
            asyncio.create_task(ejecutar_ataque_id(bot.target_id_consola))


@bot.command(name="idnuke")
@commands.is_owner()
async def idnuke_command(ctx, target_id: int):
    await ejecutar_ataque_id(target_id, ctx)


def main():
    core.pantalla("DM-SPAM :: RAFAGA A UNA ID")

    print(f"{core.BLUE}{core.BOLD}[ CONFIGURACION DE CONEXION ]{core.RESET}")
    token = core.pedir("Coloca el token del bot")

    print(f"\n{core.BLUE}{core.BOLD}[ CONFIGURACION DEL OBJETIVO ]{core.RESET}")
    bot.target_id_consola = core.pedir_int("Coloca la ID del usuario a atacar")

    print(f"\n{core.BLUE}{core.BOLD}[ CONFIGURACION DEL MENSAJE ]{core.RESET}")
    bot.mensaje_ataque = core.pedir("Escribe tu mensaje personalizado", permitir_salir=False)

    print(f"\n{core.BLUE}{core.BOLD}[ CONFIGURACION DE CANTIDAD ]{core.RESET}")
    bot.cantidad_mensajes = core.pedir_int("Cuantos mensajes enviar? (ENTER = 50)", defecto=50)

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
