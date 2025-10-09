# manager.py - gestão de bankroll, stakes e histórico
import csv, os, json
from datetime import datetime
from config import BANKROLL_INITIAL, MIN_STAKE_PERCENT, MAX_STAKE_PERCENT, RESULTS_DIR, DRY_RUN

class BankrollManager:
    def __init__(self, initial=None):
        self.initial = initial or BANKROLL_INITIAL
        self.balance = float(self.initial)
        self.history_file = os.path.join(RESULTS_DIR, 'history.csv')
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp','type','details','stake','odd','result','balance'])

    def stake_for(self, percent=None):
        p = percent or MIN_STAKE_PERCENT
        p = max(MIN_STAKE_PERCENT, min(MAX_STAKE_PERCENT, p))
        return round(self.balance * p, 2)

    def record(self, type_, details, stake, odd, result):
        # result: 'win' or 'lose' or 'void'
        if result == 'win':
            profit = round(stake * (odd - 1.0), 2)
            self.balance += profit
        elif result == 'lose':
            self.balance -= stake
        # void -> no change
        ts = datetime.utcnow().isoformat(sep=' ', timespec='seconds')
        with open(self.history_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([ts, type_, json.dumps(details, ensure_ascii=False), stake, odd, result, self.balance])

    def snapshot(self):
        return {'initial': self.initial, 'balance': self.balance}
