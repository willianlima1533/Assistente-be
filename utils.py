# utils.py - funções auxiliares (login simulado, notificação, persistência)
import json, os, subprocess
from config import DRY_RUN, SAVE_STATE_FILE, RESULTS_DIR
import datetime

os.makedirs(RESULTS_DIR, exist_ok=True)

def login_simulado(user, passwd):
    """Simula um login — NÃO use para efetuar login real automatizado."""
    # Apenas validação local para simulação
    print(f"[login_simulado] simulando login para {user}")
    return True

def save_state(state: dict):
    with open(SAVE_STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def load_state():
    if os.path.exists(SAVE_STATE_FILE):
        with open(SAVE_STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def notify(msg: str):
    """Notifica via termux-notification quando não estiver em DRY_RUN."""
    ts = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
    print(f"[NOTIF] {ts} - {msg}")
    if not DRY_RUN:
        # termux-notification requires termux-api pkg
        try:
            subprocess.run(['termux-notification', '--title', 'BE-Termux', '--content', msg])
        except Exception as e:
            print('[notify] erro ao chamar termux-notification:', e)
