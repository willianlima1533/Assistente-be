# main.py - loop principal que agenda análises e simula apostas
import argparse, time, schedule, os, json
from utils import login_simulado, notify, save_state, load_state
from analyzer import load_fixtures_local, fetch_fixtures_from_api, enrich_with_probs
from bet_engine import make_accumulators
from manager import BankrollManager
from config import DRY_RUN, SAVE_STATE_FILE, RESULTS_DIR

os.makedirs(RESULTS_DIR, exist_ok=True)

def run_round(bank):
    # 1) tentar buscar fixtures ao vivo via API; senão usar CSV local
    df = fetch_fixtures_from_api() or load_fixtures_local()
    dfp = enrich_with_probs(df)
    accs = make_accumulators(dfp)
    # para cada acumulador, simular stake e resultado futuro
    for acc in accs:
        stake = bank.stake_for()
        details = {'selections': acc['selections'], 'total_odd': acc['total_odd']}
        # marcar como 'apostado' (simulação) e registrar; o resultado real deve ser resolvido
        if DRY_RUN:
            notify(f"[DRY_RUN] Apostaria R$ {stake} em múltipla odd {acc['total_odd']:.2f}")
            # gravar como 'void' enquanto não houver resultado
            bank.record('multiple', details, stake, acc['total_odd'], 'void')
        else:
            # Não automatizamos aposta real aqui — somente simulação segura.
            notify(f"[SIM] Apostado R$ {stake} em múltipla odd {acc['total_odd']:.2f}")
            bank.record('multiple', details, stake, acc['total_odd'], 'void')

def job(bank):
    login_simulado('usuario_sim', 'senha_sim')
    run_round(bank)
    # salvar estado
    save_state(bank.snapshot())

def main_loop(dry_run=False, interval_minutes=30):
    bank = BankrollManager()
    state = load_state()
    if state and 'balance' in state:
        bank.balance = state['balance']
    schedule.every(interval_minutes).minutes.do(job, bank)
    print(f"[main] iniciando loop com intervalo {interval_minutes} minutos. DRY_RUN={dry_run}")
    while True:
        schedule.run_pending()
        time.sleep(5)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--dry-run', action='store_true', help='Executar em modo de teste (padrão)')
    p.add_argument('--interval', type=int, default=30, help='Intervalo em minutos entre rodadas')
    args = p.parse_args()
    main_loop(dry_run=args.dry_run or DRY_RUN, interval_minutes=args.interval)
