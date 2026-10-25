import os
import sys

import discord
from discord.ext import commands

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

ANCHO = 58
LINEA = "=" * ANCHO

BANNER = (
    "██████╗ ███╗   ███╗      ███████╗██████╗  █████╗ ███╗   ███╗",
    "██╔══██╗████╗ ████║      ██╔════╝██╔══██╗██╔══██╗████╗ ████║",
    "██║  ██║██╔████╔██║█████╗███████╗██████╔╝███████║██╔████╔██║",
    "██║  ██║██║╚██╔╝██║╚════╝╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║",
    "██████╔╝██║ ╚═╝ ██║      ███████║██║     ██║  ██║██║ ╚═╝ ██║",
    "╚═════╝ ╚═╝     ╚═╝      ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝",
)

# Si es True, al terminar la rafaga el script se reinicia y vuelve a pedir
# los datos. Si es False, el bot queda conectado y puedes usar .idnuke.
REINICIAR_AL_TERMINAR = True

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)

bot.target_id_consola = None
bot.mensaje_ataque = "spam"
bot.cantidad_mensajes = 50


# ------------------------------------------------------------------
#   INTERFAZ
# ------------------------------------------------------------------
def clear_screen():
    os.system("clear")
    print(f"{RED}{BOLD}")
    for linea in BANNER:
        print(linea)
    print(RESET, end="")
    print(f"{RED}{LINEA}{RESET}")
    print(f"{WHITE}{BOLD}{'DM-SPAM :: TERMINAL SYSTEM'.center(ANCHO)}{RESET}")
    print(f"{RED}{LINEA}{RESET}")


def titulo(texto, color=BLUE):
    print(f"\n{color}{BOLD}[ {texto} ]{RESET}")


def pedir(etiqueta):
    return input(f"{GREEN} -> {etiqueta}: {RESET}").strip()


def salir_con_error(mensaje):
    print(f"\n{RED}{BOLD}[X] {mensaje}{RESET}")
    sys.exit(1)


# ------------------------------------------------------------------
#   NUCLEO DEL ATAQUE
# ------------------------------------------------------------------
async def ejecutar_ataque_id(target_id, ctx=None):
    try:
        target_user = await bot.fetch_user(target_id)
    except Exception:
        print(f"\n{RED}{BOLD}[X] ERROR: usuario no encontrado o ID invalida.{RESET}")
        if ctx:
            await ctx.send("[X] ID de usuario invalida o el bot no comparte servidores.")
        return

    print(f"\n{RED}{BOLD}{LINEA}")
    print(f"[*] OBJETIVO : {target_user.name.upper()} ({target_user.id})")
    print(f"{LINEA}{RESET}")

    if ctx:
        await ctx.send(f"[*] Iniciando rafaga DM-SPAM sobre **{target_user.name}**...")

    print(f"{YELLOW}[*] Inyectando rafagas al mensaje privado...{RESET}\n")

    enviados = 0
    for _ in range(bot.cantidad_mensajes):
        try:
            await target_user.send(content=bot.mensaje_ataque)
            enviados += 1
            print(f"{GREEN}[+] [{enviados}/{bot.cantidad_mensajes}] enviado.{RESET}")
            await asyncio.sleep(0.7)
        except discord.errors.Forbidden:
            print(f"\n{RED}{BOLD}[X] CANCELADO: el usuario bloqueo al bot o cerro sus DMs.{RESET}")
            break
        except discord.errors.HTTPException:
            await asyncio.sleep(1.0)
        except Exception:
            pass

    print(f"\n{GREEN}{BOLD}{LINEA}")
    print(f"[OK] RAFAGA FINALIZADA. TOTAL ENVIADOS: {enviados}")
    print(f"{LINEA}{RESET}")

    if ctx:
        await ctx.send(f"[OK] Rafaga finalizada. Mensajes enviados: {enviados}")

    await asyncio.sleep(2)

    if REINICIAR_AL_TERMINAR:
        os.execv(sys.executable, [sys.executable, os.path.abspath(__file__)])


# ------------------------------------------------------------------
#   EVENTOS Y COMANDOS
# ------------------------------------------------------------------
@bot.event
async def on_ready():
    print(f"\n{GREEN}{BOLD}[OK] CONECTADO COMO: {bot.user.name.upper()}{RESET}")
    print(f"{YELLOW}[*] Procesando la solicitud del panel...{RESET}")

    if getattr(bot, "target_id_consola", None):
        asyncio.create_task(ejecutar_ataque_id(bot.target_id_consola))


@bot.command(name="idnuke")
@commands.is_owner()
async def idnuke_command(ctx, target_id: int):
    await ejecutar_ataque_id(target_id, ctx)


# ------------------------------------------------------------------
#   ARRANQUE
# ------------------------------------------------------------------
def main():
    clear_screen()

    titulo("CONFIGURACION DE CONEXION")
    token = pedir("Coloca el token del bot")
    if not token:
        salir_con_error("El token no puede estar vacio.")

    titulo("CONFIGURACION DEL OBJETIVO")
    id_input = pedir("Coloca la ID del usuario a atacar")
    if not id_input:
        salir_con_error("La ID es obligatoria.")
    try:
        bot.target_id_consola = int(id_input)
    except ValueError:
        salir_con_error("La ID debe ser un numero valido.")

    titulo("CONFIGURACION DEL MENSAJE")
    texto = pedir("Escribe tu mensaje personalizado")
    if not texto:
        salir_con_error("El mensaje no puede estar vacio.")
    bot.mensaje_ataque = texto

    titulo("CONFIGURACION DE CANTIDAD")
    cantidad = pedir("Cuantos mensajes quieres enviar (ej: 10, 50, 100)")
    if not cantidad:
        print(f"{YELLOW}[*] Sin cantidad, usando 50 por defecto.{RESET}")
        bot.cantidad_mensajes = 50
    else:
        try:
            bot.cantidad_mensajes = max(1, int(cantidad))
        except ValueError:
            print(f"{YELLOW}[*] Entrada invalida, usando 50 por defecto.{RESET}")
            bot.cantidad_mensajes = 50

    print(f"\n{YELLOW}{BOLD}{LINEA}")
    print("[*] Validando parametros y estableciendo conexion...")
    print(f"{LINEA}{RESET}")

    try:
        bot.run(token)
    except discord.errors.LoginFailure:
        print(f"\n{RED}{BOLD}[X] ERROR: el token es incorrecto o expiro.{RESET}")
    except KeyboardInterrupt:
        print(f"\n{RED}{BOLD}[-] Script cerrado por el usuario.{RESET}")


if __name__ == "__main__":
    main()
