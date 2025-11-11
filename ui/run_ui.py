"""
Script de inicialização da UI Kivy
"""
import sys
import os
from pathlib import Path

# Adicionar o diretório raiz do projeto ao path para importar módulos
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Importar o logger para garantir que a UI use o sistema de logging
try:
    from tools.logger import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

# Executar a aplicação Kivy
try:
    from ui.app import AssistenteApp
    
    if __name__ == '__main__':
        AssistenteApp().run()
        
except ImportError as e:
    logger.error(f"Erro ao importar a aplicação Kivy: {e}")
    logger.error("Verifique se o Kivy está instalado no seu ambiente virtual.")
    sys.exit(1)
except Exception as e:
    logger.exception(f"Erro fatal ao executar a UI: {e}")
    sys.exit(1)
