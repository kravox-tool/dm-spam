#!/data/data/com.termux/files/usr/bin/bash
# ==================================================================
#   DM-SPAM  ::  INSTALADOR AUTOMATICO PARA TERMUX
# ==================================================================
set -e

echo -e "\033[1;91m==================================================\033[0m"
echo -e "\033[1;91m[*] DM-SPAM :: INSTALANDO ENTORNO\033[0m"
echo -e "\033[1;91m==================================================\033[0m"

echo -e "\033[1;93m[*] Actualizando paquetes...\033[0m"
pkg update -y && pkg upgrade -y

echo -e "\033[1;93m[*] Instalando Python...\033[0m"
pkg install -y python

echo -e "\033[1;93m[*] Instalando dependencias pip...\033[0m"
pip install --upgrade pip
pip install -r requirements.txt

echo -e "\033[1;93m[*] Solicitando acceso al almacenamiento...\033[0m"
termux-setup-storage || true

chmod +x dm-spam.py spam_bot.py hexvox.py run.sh 2>/dev/null || true

echo -e "\033[1;92m[OK] Instalacion completada.\033[0m"
echo -e "\033[1;92m[*] Ejecuta:  python dm-spam.py   o   bash run.sh\033[0m"
