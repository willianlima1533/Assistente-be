"""
Funções auxiliares (login simulado, notificação, persistência)
"""
import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Importar logger
try:
    from logger import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

# Importar config
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from config import DRY_RUN, SAVE_STATE_FILE, RESULTS_DIR

# Criar diretórios necessários
os.makedirs(RESULTS_DIR, exist_ok=True)


def login_simulado(user: str, passwd: str) -> bool:
    """
    Simula um login — NÃO use para efetuar login real automatizado.
    
    Args:
        user: Nome de usuário
        passwd: Senha
    
    Returns:
        True se simulação bem-sucedida
    """
    logger.info(f"🔐 Simulando login para usuário: {user}")
    return True


def save_state(state: dict) -> None:
    """Salva estado do sistema em arquivo JSON"""
    try:
        state_path = BASE_DIR / SAVE_STATE_FILE
        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        logger.debug(f"💾 Estado salvo em {state_path}")
    except Exception as e:
        logger.error(f"❌ Erro ao salvar estado: {e}")


def load_state() -> dict:
    """Carrega estado do sistema de arquivo JSON"""
    try:
        state_path = BASE_DIR / SAVE_STATE_FILE
        if state_path.exists():
            with open(state_path, 'r', encoding='utf-8') as f:
                state = json.load(f)
            logger.debug(f"📂 Estado carregado de {state_path}")
            return state
        else:
            logger.debug("📂 Nenhum estado anterior encontrado")
            return {}
    except Exception as e:
        logger.error(f"❌ Erro ao carregar estado: {e}")
        return {}


def notify(msg: str) -> None:
    """Notifica via termux-notification quando não estiver em DRY_RUN"""
    ts = datetime.now().isoformat(sep=' ', timespec='seconds')
    logger.info(f"📢 {msg}")
    
    if not DRY_RUN:
        try:
            subprocess.run(
                ['termux-notification', '--title', 'Assistente-be', '--content', msg],
                timeout=5,
                check=False
            )
        except FileNotFoundError:
            logger.debug("termux-notification não disponível")
        except Exception as e:
            logger.warning(f"⚠️  Erro ao chamar termux-notification: {e}")
