"""
Módulo de logging centralizado usando loguru
Fornece logging estruturado e inteligente para todo o sistema
"""
import sys
import os
from pathlib import Path
from loguru import logger

# Configuração de diretórios
LOGS_DIR = Path(__file__).parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Remover handler padrão
logger.remove()

# Console handler com cores e formatação
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
    colorize=True,
)

# File handler - logs gerais
logger.add(
    LOGS_DIR / "assistente_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="00:00",  # Rotação diária à meia-noite
    retention="30 days",  # Manter logs por 30 dias
    compression="zip",  # Comprimir logs antigos
    encoding="utf-8",
)

# File handler - erros críticos
logger.add(
    LOGS_DIR / "errors_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}\n{exception}",
    level="ERROR",
    rotation="00:00",
    retention="90 days",
    compression="zip",
    encoding="utf-8",
    backtrace=True,
    diagnose=True,
)

# File handler - operações de trading
logger.add(
    LOGS_DIR / "trading_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
    level="INFO",
    rotation="00:00",
    retention="90 days",
    compression="zip",
    encoding="utf-8",
    filter=lambda record: "TRADE" in record["extra"],
)


def get_logger(name: str):
    """
    Retorna um logger configurado para o módulo especificado
    
    Args:
        name: Nome do módulo (geralmente __name__)
    
    Returns:
        Logger configurado
    """
    return logger.bind(name=name)


def log_trade(action: str, details: dict):
    """
    Registra operação de trading com contexto específico
    
    Args:
        action: Tipo de ação (BUY, SELL, CLOSE, etc.)
        details: Dicionário com detalhes da operação
    """
    logger.bind(TRADE=True).info(f"{action} | {details}")


def log_health_check():
    """Registra health check do sistema"""
    logger.info("🏥 Health check - Sistema operacional")


def log_startup(version: str, modules: list):
    """
    Registra inicialização do sistema
    
    Args:
        version: Versão do sistema
        modules: Lista de módulos carregados
    """
    logger.info("="*60)
    logger.info(f"🚀 Assistente-be v{version} iniciando...")
    logger.info(f"📦 Módulos carregados: {', '.join(modules)}")
    logger.info("="*60)


def log_shutdown():
    """Registra encerramento do sistema"""
    logger.info("="*60)
    logger.info("🛑 Assistente-be encerrando...")
    logger.info("="*60)


# Exportar logger padrão
__all__ = ["logger", "get_logger", "log_trade", "log_health_check", "log_startup", "log_shutdown"]
