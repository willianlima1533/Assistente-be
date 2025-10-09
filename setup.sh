#!/data/data/com.termux/files/usr/bin/bash
# Script de configuração básico para Termux
echo "[BE-Termux] Iniciando setup (revise o script antes de executar)"
pkg update -y && pkg upgrade -y
pkg install python git curl wget -y
pkg install termux-api -y
pkg install openssh -y
# Instalar compiladores e ffmpeg (opcionais)
pkg install clang ffmpeg -y
python -m pip install --upgrade pip
pip install requests beautifulsoup4 pandas numpy schedule plyer speechrecognition gTTS
# OpenCV é pesado no Termux; instalar só se o usuário quiser (opcional)
echo "[BE-Termux] Dependências instaladas. Revise requirements.txt e instale extras se necessário."
echo "Para clonar de um repositório remoto use: git clone <repo>"
