#!/usr/bin/env python3
"""
Assistente-be - Sistema de Trading e Apostas Inteligente
Loop principal que agenda análises e simula apostas
"""
import argparse
import time
import schedule
import os
import sys
from pathlib import Path

# Adicionar diretórios ao path
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR / "tools"))
sys.path.insert(0, str(BASE_DIR / "trader"))

# Importar logger primeiro
from logger import logger, log_startup, log_shutdown, log_health_check

# Importar módulos do sistema
try:
    from utils import login_simulado, notify, save_state, load_state
    from analyzer import load_fixtures_local, fetch_fixtures_from_api, enrich_with_probs
    from bet_engine import make_accumulators
    from manager import BankrollManager
    from config import DRY_RUN, SAVE_STATE_FILE, RESULTS_DIR
except ImportError as e:
    logger.error(f"Erro ao importar módulos: {e}")
    logger.info("Verifique se a estrutura de diretórios está correta")
    sys.exit(1)

# Versão do sistema
VERSION = "3.0.0"

# Criar diretórios necessários
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs("logs", exist_ok=True)


def run_round(bank: BankrollManager):
    """
    Executa uma rodada de análise e apostas
    
    Args:
        bank: Gerenciador de bankroll
    """
    try:
        logger.info("🎲 Iniciando rodada de análise...")
        
        # 1) Tentar buscar fixtures ao vivo via API; senão usar CSV local
        df = fetch_fixtures_from_api()
        if df is None:
            logger.warning("API indisponível, usando dados locais")
            df = load_fixtures_local()
        
        # 2) Enriquecer com probabilidades
        dfp = enrich_with_probs(df)
        logger.info(f"📊 {len(dfp)} partidas analisadas")
        
        # 3) Gerar acumuladores
        accs = make_accumulators(dfp)
        logger.info(f"🎯 {len(accs)} acumuladores gerados")
        
        # 4) Para cada acumulador, simular stake e resultado futuro
        for i, acc in enumerate(accs, 1):
            stake = bank.stake_for()
            details = {
                'selections': acc['selections'],
                'total_odd': acc['total_odd']
            }
            
            if DRY_RUN:
                logger.info(f"[DRY_RUN] Aposta {i}: R$ {stake:.2f} @ {acc['total_odd']:.2f}")
                notify(f"[DRY_RUN] Apostaria R$ {stake} em múltipla odd {acc['total_odd']:.2f}")
                bank.record('multiple', details, stake, acc['total_odd'], 'void')
            else:
                logger.warning(f"[SIMULAÇÃO] Aposta {i}: R$ {stake:.2f} @ {acc['total_odd']:.2f}")
                notify(f"[SIM] Apostado R$ {stake} em múltipla odd {acc['total_odd']:.2f}")
                bank.record('multiple', details, stake, acc['total_odd'], 'void')
        
        logger.success("✅ Rodada concluída com sucesso")
        
    except Exception as e:
        logger.exception(f"❌ Erro durante rodada: {e}")


def job(bank: BankrollManager):
    """
    Job agendado que executa login e rodada
    
    Args:
        bank: Gerenciador de bankroll
    """
    try:
        log_health_check()
        login_simulado('usuario_sim', 'senha_sim')
        run_round(bank)
        
        # Salvar estado
        state = bank.snapshot()
        save_state(state)
        logger.info(f"💾 Estado salvo - Saldo: R$ {state['balance']:.2f}")
        
    except Exception as e:
        logger.exception(f"❌ Erro no job agendado: {e}")


def main_loop(dry_run: bool = False, interval_minutes: int = 30):
    """
    Loop principal do sistema
    
    Args:
        dry_run: Modo de teste (não registra apostas reais)
        interval_minutes: Intervalo entre rodadas em minutos
    """
    # Startup
    modules = ["analyzer", "bet_engine", "manager", "utils", "voice"]
    log_startup(VERSION, modules)
    
    # Inicializar bankroll
    bank = BankrollManager()
    state = load_state()
    
    if state and 'balance' in state:
        bank.balance = state['balance']
        logger.info(f"💰 Estado anterior carregado - Saldo: R$ {bank.balance:.2f}")
    else:
        logger.info(f"💰 Novo bankroll iniciado - Saldo: R$ {bank.balance:.2f}")
    
    # Configurar agendamento
    schedule.every(interval_minutes).minutes.do(job, bank)
    logger.info(f"⏰ Agendamento configurado: a cada {interval_minutes} minutos")
    logger.info(f"🔧 Modo: {'DRY_RUN (teste)' if dry_run else 'SIMULAÇÃO'}")
    
    # Loop principal
    try:
        logger.info("🔄 Loop principal iniciado - Pressione Ctrl+C para parar")
        while True:
            schedule.run_pending()
            time.sleep(5)
    
    except KeyboardInterrupt:
        logger.warning("⚠️  Interrupção detectada (Ctrl+C)")
    
    except Exception as e:
        logger.exception(f"❌ Erro fatal no loop principal: {e}")
    
    finally:
        # Salvar estado final
        save_state(bank.snapshot())
        log_shutdown()


def main():
    """Função principal com argumentos de linha de comando"""
    parser = argparse.ArgumentParser(
        description="Assistente-be - Sistema de Trading e Apostas Inteligente",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python main.py --dry-run                    # Modo de teste
  python main.py --interval 60                # Intervalo de 60 minutos
  python main.py --dry-run --interval 15      # Teste com intervalo de 15 min
        """
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Executar em modo de teste (padrão: usa config.DRY_RUN)'
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        default=30,
        help='Intervalo em minutos entre rodadas (padrão: 30)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'Assistente-be v{VERSION}'
    )
    
    args = parser.parse_args()
    
    # Executar loop principal
    main_loop(dry_run=args.dry_run or DRY_RUN, interval_minutes=args.interval)


if __name__ == '__main__':
    main()
