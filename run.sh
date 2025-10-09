#!/data/data/com.termux/files/usr/bin/bash
# Script leve para rodar o main em background usando screen (instale screen via pkg)
if ! command -v screen >/dev/null 2>&1; then
  echo "screen não encontrado. Instalando..."
  pkg install screen -y
fi
screen -dmS be_termux python main.py
echo "BE-Termux iniciado em screen (nome: be_termux). Use 'screen -r be_termux' para anexar."
