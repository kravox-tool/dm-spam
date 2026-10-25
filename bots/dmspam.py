#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DM-SPAM :: Rafaga masiva de mensajes directos a una ID.
"""

import asyncio
import os
import sys
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=".", intents=intents)

# Colores esteticos ANSI
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
BOLD = "\033[1m"
RESET = "\033[0m"


def clear_screen():
    os.system('clear')
    print(f"{RED}{BOLD}")
    print("██████╗ ███╗   ███╗      ███████╗██████╗  █████╗ ███╗   ███╗")
    print("██╔══██╗████╗ ████║      ██╔════╝██╔══██╗██╔══██╗████╗ ████║")
    print("██║  ██║██╔████╔██║█████╗███████╗██████╔╝███████║██╔████╔██║")
    print("██║  ██║██║╚██╔╝██║╚════╝╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║")
    print("██████╔╝██║ ╚═╝ ██║      ███████║██║     ██║  ██║██║ ╚═╝ ██║")
    print("╚═════╝ ╚═╝     ╚═╝      ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝")
    print(f"=================================================={RESET}")
    print(f"{CYAN}{BOLD}            DM-SPAM TERMINAL SYSTEM            {RESET}")
    print(f"{RED}=================================================={RESET}")


async def ejecutar_ataque_id(target_id, ctx=None):
    try:
        target_user = await bot.fetch_user(target_id)
    except Exception:
        print(f"\n{RED}{BOLD}[X] ERROR: El bot no encuentra a ese usuario o la ID es invalida.{RESET}")
        if ctx:
            await ctx.send("[X] ID de usuario invalida o el bot no comparte servidores.")
        return

    print(f"\n{RED}{BOLD}==================================================")
    print(f"[>] OBJETIVO: {target_user.name.upper()} ({target_user.id})")
    print(f"=================================================={RESET}")

    if ctx:
        await ctx.send(f"[>] Iniciando protocolo DM-SPAM en {target_user.name}...")
    print(f"{YELLOW}[*] Inyectando rafagas al mensaje privado...{RESET}\n")

    enviados = 0
    for i in range(bot.cantidad_mensajes):
        try:
            await target_user.send(content=bot.mensaje_ataque)
            enviados += 1
            print(f"{GREEN}[+] [{enviados}/{bot.cantidad_mensajes}] Enviado exitosamente.{RESET}")
            await asyncio.sleep(0.7)
        except discord.errors.Forbidden:
            print(f"\n{RED}{BOLD}[X] CANCELADO: El usuario bloqueo al bot o tiene los DMs cerrados.{RESET}")
            break
        except Exception:
            pass

    print(f"\n{GREEN}{BOLD}==================================================")
    print(f"[OK] RAFAGA FINALIZADA. TOTAL ENVIADOS: {enviados}")
    print(f"=================================================={RESET}")

    if ctx:
        await ctx.send(f"[OK] Ataque de spam finalizado. Mensajes enviados: {enviados}")
    await asyncio.sleep(2)
    os.execv(sys.executable, ['python'] + sys.argv)


@bot.event
async def on_ready():
    print(f"\n{GREEN}{BOLD}[OK] CONECTADO COMO: {bot.user.name.upper()} BOT{RESET}")
    print(f"{YELLOW}[*] Procesando la solicitud del panel...{RESET}")

    if bot.target_id_consola:
        asyncio.create_task(ejecutar_ataque_id(bot.target_id_consola))


@bot.command(name="idnuke")
@commands.is_owner()
async def idnuke_command(ctx, target_id: int):
    await ejecutar_ataque_id(target_id, ctx)


def main():
    clear_screen()

    # SECCION 1: Autenticacion
    print(f"{BLUE}{BOLD}[ CONFIGURACION DE CONEXION ]{RESET}")
    token = input(f"{GREEN}-> Coloca el token del bot: {RESET}").strip()
    if not token:
        print(f"\n{RED}{BOLD}[X] Error: El token no puede estar vacio.{RESET}")
        sys.exit()

    # SECCION 2: Objetivo
    print(f"\n{BLUE}{BOLD}[ CONFIGURACION DEL OBJETIVO ]{RESET}")
    id_input = input(f"{GREEN}-> Coloca la ID del usuario a atacar: {RESET}").strip()
    if not id_input:
        print(f"\n{RED}{BOLD}[X] Error: La ID es obligatoria.{RESET}")
        sys.exit()

    try:
        bot.target_id_consola = int(id_input)
    except ValueError:
        print(f"\n{RED}{BOLD}[X] Error: La ID debe ser un numero valido.{RESET}")
        sys.exit()

    # SECCION 3: Mensaje
    print(f"\n{BLUE}{BOLD}[ CONFIGURACION DEL MENSAJE ]{RESET}")
    texto_usuario = input(f"{GREEN}-> Escribe tu mensaje personalizado: {RESET}").strip()
    if not texto_usuario:
        print(f"\n{RED}{BOLD}[X] Error: El mensaje no puede estar vacio.{RESET}")
        sys.exit()
    bot.mensaje_ataque = texto_usuario

    # SECCION 4: Cantidad
    print(f"\n{BLUE}{BOLD}[ CONFIGURACION DE CANTIDAD ]{RESET}")
    cantidad_input = input(f"{GREEN}-> Cuantos mensajes quieres enviar? (Ej: 10, 50, 100): {RESET}").strip()
    if not cantidad_input:
        print(f"\n{YELLOW}[*] No colocaste cantidad. Usando 50 por defecto.{RESET}")
        bot.cantidad_mensajes = 50
    else:
        try:
            bot.cantidad_mensajes = int(cantidad_input)
        except ValueError:
            print(f"\n{YELLOW}[*] Entrada invalida. Usando 50 por defecto.{RESET}")
            bot.cantidad_mensajes = 50

    print(f"\n{YELLOW}{BOLD}==================================================")
    print(f"[*] Validando parametros y estableciendo conexion...")
    print(f"=================================================={RESET}")

    try:
        bot.run(token)
    except discord.errors.LoginFailure:
        print(f"\n{RED}{BOLD}[X] ERROR: El token ingresado es incorrecto o expiro.{RESET}")
    except KeyboardInterrupt:
        print(f"\n{RED}{BOLD}[-] Script cerrado por el usuario.{RESET}")


if __name__ == '__main__':
    main()
