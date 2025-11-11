# bet_engine.py - lógica para gerar múltiplas 'humanas' e selecionar value bets
import random, itertools
import numpy as np
from analyzer import enrich_with_probs
import sys; sys.path.insert(0, ".."); from config import MIN_STAKE_PERCENT, MAX_STAKE_PERCENT, BANKROLL_INITIAL

random.seed()

def implied_prob(odd):
    try:
        return 1.0 / float(odd)
    except Exception:
        return 0.0

def select_value_selections(df, conf_threshold=0.65):
    """Seleciona seleções com probabilidade estimada > conf_threshold e odds indicando value."""
    picks = []
    for idx, row in df.iterrows():
        # Ex.: teste para vitória do time da casa
        if 'home_odds' in row and row.get('home_odds') and row['p_home'] > conf_threshold:
            ip = implied_prob(row['home_odds'])
            # value bet se prob estimada > implied_prob + margem
            if row['p_home'] > ip + 0.05:
                picks.append({'idx': idx, 'market': '1', 'odd': row['home_odds'], 'conf': row['p_home']})
        # draw / away selection (pode adicionar outros mercados)
    return picks

def make_accumulators(df, max_selections=4, target_total_odd_min=5.0, target_total_odd_max=12.0):
    """Gera 1-3 múltiplas por rodada misturando mercados e adicionando 'erro humano' leve."""
    dfp = enrich_with_probs(df)
    candidates = select_value_selections(dfp, conf_threshold=0.60)
    random.shuffle(candidates)
    accs = []
    # Tentar formar acumuladores com 3-4 seleções
    for r in range(3):
        k = random.randint(3, min(max_selections, max(3, len(candidates))))
        comb = random.sample(candidates, k) if len(candidates) >= k else candidates
        total_odd = np.prod([c['odd'] for c in comb]) if comb else 0
        # introduzir pequena chance de erro humano: trocar uma seleção por outra sub-ótima
        if random.random() < 0.12 and len(comb) >= 1:
            # simular erro trocando uma odd por odd * (1 +/- 0.1)
            i = random.randrange(len(comb))
            comb[i]['odd'] = comb[i]['odd'] * (1 + random.uniform(-0.08, 0.12))
        if total_odd >= target_total_odd_min and total_odd <= target_total_odd_max:
            accs.append({'selections': comb, 'total_odd': float(total_odd)})
    return accs
