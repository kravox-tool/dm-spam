#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==================================================================
#   D M - S P A M   ::   LANZADOR PRINCIPAL
#   Termux  -  interfaz roja neon  -  sin emojis
# ------------------------------------------------------------------
#   Uso:  python dm-spam.py
# ==================================================================

import os
import sys

RED     = "\033[1;91m"
GREEN   = "\033[1;92m"
YELLOW  = "\033[1;93m"
CYAN    = "\033[1;96m"
WHITE   = "\033[1;97m"
GRAY    = "\033[0;90m"
BOLD    = "\033[1m"
RESET   = "\033[0m"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ANCHO = 62

BANNER = (
    "██████╗ ███╗   ███╗      ███████╗██████╗  █████╗ ███╗   ███╗",
    "██╔══██╗████╗ ████║      ██╔════╝██╔══██╗██╔══██╗████╗ ████║",
    "██║  ██║██╔████╔██║█████╗███████╗██████╔╝███████║██╔████╔██║",
    "██║  ██║██║╚██╔╝██║╚════╝╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║",
    "██████╔╝██║ ╚═╝ ██║      ███████║██║     ██║  ██║██║ ╚═╝ ██║",
    "╚═════╝ ╚═╝     ╚═╝      ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝",
)

OPCIONES = (
    ("1", "DM-SPAM", "rafaga masiva de mensajes directos a una ID"),
    ("2", "CHAT",  "chat en vivo por consola con una ID"),
    ("3", "INFO",    "requisitos, token e intents necesarios"),
    ("0", "SALIR",   "cerrar el lanzador"),
)


def clear_screen():
    os.system("clear")


def dibujar():
    clear_screen()
    print(f"{RED}{BOLD}")
    for linea in BANNER:
        print(linea)
    print(RESET, end="")
    print(f"{RED}{'=' * ANCHO}{RESET}")
    print(f"{WHITE}{BOLD}{'TERMUX PANEL'.center(ANCHO)}{RESET}")
    print(f"{RED}{'=' * ANCHO}{RESET}\n")
    for tecla, nombre, desc in OPCIONES:
        print(f"  {RED}{BOLD}[{tecla}]{RESET} {GREEN}{nombre:<9}{RESET} {GRAY}{desc}{RESET}")
    print()


def pantalla_info():
    clear_screen()
    print(f"{RED}{BOLD}{'=' * ANCHO}")
    print("REQUISITOS DEL SISTEMA".center(ANCHO))
    print(f"{'=' * ANCHO}{RESET}\n")
    print(f"{WHITE}1. Python 3.10 o superior{RESET}")
    print(f"{WHITE}2. discord.py >= 2.3{RESET}")
    print(f"{WHITE}3. prompt_toolkit >= 3.0{RESET}")
    print(f"\n{WHITE}4. En el Discord Developer Portal activa:{RESET}")
    print(f"{GRAY}   - MESSAGE CONTENT INTENT{RESET}")
    print(f"{GRAY}   - SERVER MEMBERS INTENT{RESET}")
    print(f"{GRAY}   - PRESENCE INTENT (opcional){RESET}")
    print(f"\n{YELLOW}Instalacion automatica:  bash install.sh{RESET}")
    print(f"{YELLOW}Arranque rapido:         bash run.sh{RESET}")
    input(f"\n{GREEN} -> ENTER para volver al menu...{RESET}")


def lanzar(script):
    ruta = os.path.join(BASE_DIR, script)
    if not os.path.isfile(ruta):
        print(f"\n{RED}[X] No se encontro el archivo {script}{RESET}")
        input(f"{GREEN} -> ENTER para volver...{RESET}")
        return
    print(f"\n{YELLOW}[*] Lanzando {script} ...{RESET}")
    os.execv(sys.executable, [sys.executable, ruta])


def main():
    while True:
        dibujar()
        try:
            opcion = input(f"{GREEN} -> Elige una opcion: {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{RED}[-] Cerrando lanzador.{RESET}")
            sys.exit(0)

        if opcion == "1":
            lanzar("spam_bot.py")
        elif opcion == "2":
            lanzar("chat.py")
        elif opcion == "3":
            pantalla_info()
        elif opcion in ("0", "q", "salir", "exit"):
            print(f"\n{RED}[-] Cerrando lanzador.{RESET}")
            sys.exit(0)
        else:
            print(f"\n{YELLOW}[!] Opcion invalida.{RESET}")
            input(f"{GREEN} -> ENTER para continuar...{RESET}")


if __name__ == "__main__":
    main()
