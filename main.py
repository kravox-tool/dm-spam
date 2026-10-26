#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DM-SPAM :: Termux Panel
Lanzador principal con interfaz fuego (rojo/naranja neon).
"""

import os
import sys
import time
import subprocess

# ---------- Paleta ANSI ----------
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

# ---------- Paleta FUEGO ----------
FUEGO = [
    "\033[1;38;5;196m",
    "\033[1;38;5;202m",
    "\033[1;38;5;208m",
    "\033[1;38;5;214m",
]
ROJO    = FUEGO[0]
NARANJA = FUEGO[2]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOTS_DIR = os.path.join(BASE_DIR, "bots")
ANCHO = 66

BANNER_LINES = [
    "██████╗ ███╗   ███╗      ███████╗██████╗  █████╗ ███╗   ███╗",
    "██╔══██╗████╗ ████║      ██╔════╝██╔══██╗██╔══██╗████╗ ████║",
    "██║  ██║██╔████╔██║█████╗███████╗██████╔╝███████║██╔████╔██║",
    "██║  ██║██║╚██╔╝██║╚════╝╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║",
    "██████╔╝██║ ╚═╝ ██║      ███████║██║     ██║  ██║██║ ╚═╝ ██║",
    "╚═════╝ ╚═╝     ╚═╝      ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝",
]


def neon(texto):
    """Pinta el texto caracter por caracter con la paleta fuego."""
    if not texto:
        return ""
    piezas = []
    for i, ch in enumerate(texto):
        piezas.append(FUEGO[i % len(FUEGO)])
        piezas.append(ch)
    piezas.append(RESET)
    return "".join(piezas)


def limpiar():
    os.system("clear")


def banner():
    print(BOLD)
    for i, linea in enumerate(BANNER_LINES):
        print(f"{FUEGO[i % len(FUEGO)]}{linea}")
    print(RESET)


def barra(texto=""):
    print(f"{ROJO}{BOLD}" + "=" * ANCHO + f"{RESET}")
    if texto:
        print(neon(texto.center(ANCHO)))
        print(f"{ROJO}{BOLD}" + "=" * ANCHO + f"{RESET}")


def encabezado():
    limpiar()
    banner()
    barra("TERMUX PANEL")
    print()


def pausa():
    input(f"\n{GRAY}Presiona ENTER para volver al panel...{RESET}")


def menu():
    print(f" {ROJO}{BOLD}[1]{RESET}  {WHITE}{BOLD}DM-SPAM{RESET}   {GRAY}rafaga de mensajes directos a una ID{RESET}")
    print(f" {ROJO}{BOLD}[2]{RESET}  {WHITE}{BOLD}CHAT{RESET}      {GRAY}chat en vivo por consola con una ID{RESET}")
    print(f" {ROJO}{BOLD}[3]{RESET}  {WHITE}{BOLD}MASIVO{RESET}    {GRAY}mensaje x veces a todos los usuarios del servidor{RESET}")
    print(f" {ROJO}{BOLD}[4]{RESET}  {WHITE}{BOLD}FLASH{RESET}     {GRAY}enviar a usuario o servidor y borrar rapido{RESET}")
    print(f" {ROJO}{BOLD}[5]{RESET}  {WHITE}{BOLD}INFO{RESET}      {GRAY}requisitos, token e intents necesarios{RESET}")
    print(f" {ROJO}{BOLD}[0]{RESET}  {WHITE}{BOLD}SALIR{RESET}     {GRAY}cerrar el lanzador{RESET}")
    print()


def lanzar_script(nombre):
    ruta = os.path.join(BOTS_DIR, nombre)
    if not os.path.isfile(ruta):
        print(f"\n{ROJO}[X] Script no encontrado: {ruta}{RESET}")
        pausa()
        return
    try:
        subprocess.run([sys.executable, ruta], cwd=BASE_DIR)
    except KeyboardInterrupt:
        pass
    pausa()


def pantalla_info():
    limpiar()
    banner()
    barra("INFORMACION / REQUISITOS")
    print(f"""
 {WHITE}{BOLD}FUNCIONES DEL PANEL{RESET}
   {GRAY}-{RESET} DM-SPAM  rafaga de DMs a una ID
   {GRAY}-{RESET} CHAT     chat en vivo por consola con una ID
   {GRAY}-{RESET} MASIVO   mensaje x veces a todos los usuarios de un servidor
   {GRAY}-{RESET} FLASH    enviar a un usuario o servidor y borrar rapido

 {WHITE}{BOLD}REQUISITOS{RESET}
   {GRAY}-{RESET} Termux actualizado
   {GRAY}-{RESET} Python 3.10 o superior
   {GRAY}-{RESET} discord.py >= 2.3.2
   {GRAY}-{RESET} prompt_toolkit >= 3.0.43

 {WHITE}{BOLD}INSTALACION{RESET}
   {NARANJA}bash setup.sh{RESET}

 {WHITE}{BOLD}COMO OBTENER EL TOKEN{RESET}
   {GRAY}-{RESET} Entra a https://discord.com/developers/applications
   {GRAY}-{RESET} New Application > Bot > Reset Token > Copia el token

 {WHITE}{BOLD}INTENTS NECESARIOS (activalos en el portal){RESET}
   {GRAY}-{RESET} Presence Intent
   {GRAY}-{RESET} Server Members Intent
   {GRAY}-{RESET} Message Content Intent

 {WHITE}{BOLD}COMO OBTENER UNA ID{RESET}
   {GRAY}-{RESET} Ajustes de Discord > Avanzado > Modo desarrollador
   {GRAY}-{RESET} Clic derecho sobre el usuario > Copiar ID

 {WHITE}{BOLD}SALIR DESDE ADENTRO DE UNA FUNCION{RESET}
   {GRAY}-{RESET} Escribe 'salir' en la consola para volver al panel
   {GRAY}-{RESET} En Discord usa .salir o .exit (solo el dueno)
""")
    pausa()


def main():
    while True:
        encabezado()
        menu()
        opcion = input(f"{neon('-> ')}{neon('Elige una opcion')}{neon(': ')}").strip()

        if opcion == "1":
            lanzar_script("dmspam.py")
        elif opcion == "2":
            lanzar_script("chat.py")
        elif opcion == "3":
            lanzar_script("masivo.py")
        elif opcion == "4":
            lanzar_script("flash.py")
        elif opcion == "5":
            pantalla_info()
        elif opcion == "0":
            limpiar()
            banner()
            barra()
            print(f"\n{NARANJA}[-] Saliendo del panel...{RESET}\n")
            break
        else:
            print(f"\n{NARANJA}[!] Opcion invalida. Usa 1, 2, 3, 4, 5 o 0.{RESET}")
            time.sleep(1.2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{ROJO}[-] Panel cerrado por el usuario.{RESET}")
