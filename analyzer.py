# analyzer.py - busca dados de partidas e calcula probabilidades simples
# Usa API-Football quando disponível; caso contrário, usa CSV local de fixtures.
import requests, pandas as pd, numpy as np
from config import API_FOOTBALL_KEY
import os

DATA_CSV = os.path.join('data','fixtures_sample.csv')

def fetch_fixtures_from_api(league_id=None):
    """Exemplo de fetch usando API-Football (precisa de chave)."""
    if not API_FOOTBALL_KEY:
        return None
    headers = {'x-apisports-key': API_FOOTBALL_KEY}
    url = 'https://v3.football.api-sports.io/fixtures?live=all'
    if league_id:
        url += f'&league={league_id}'
    r = requests.get(url, headers=headers, timeout=15)
    if r.status_code != 200:
        return None
    data = r.json().get('response', [])
    rows = []
    for f in data:
        # Simplificar campos úteis
        try:
            rows.append({
                'date': f['fixture']['date'][:10],
                'home_team': f['teams']['home']['name'],
                'away_team': f['teams']['away']['name'],
                'home_odds': None,
                'draw_odds': None,
                'away_odds': None
            })
        except Exception:
            continue
    return pd.DataFrame(rows)

def load_fixtures_local():
    return pd.read_csv(DATA_CSV, parse_dates=['date'])

def estimate_probs_poisson(home_mean=1.3, away_mean=1.0):
    """Retorna probabilidades simplificadas para 1X2 com modelo Poisson (aprox)."""
    # Para velocidade, calcular heurístico simples
    # Prob home win approx = sigmoid(home_mean - away_mean)
    def sigmoid(x): return 1/(1+np.exp(-x))
    p_home = sigmoid((home_mean - away_mean))
    p_away = 1 - p_home - 0.08  # reserva para empate
    p_draw = 0.08
    return max(0.01, p_home), max(0.01, p_draw), max(0.01, p_away)

def enrich_with_probs(df: pd.DataFrame):
    df = df.copy()
    probs = []
    for _idx, row in df.iterrows():
        # estimativas de média de gols podem vir de estatísticas reais; aqui usamos heurísticas
        hm = np.random.uniform(0.8, 1.8)
        am = np.random.uniform(0.6, 1.4)
        p_home, p_draw, p_away = estimate_probs_poisson(hm, am)
        probs.append({'p_home': p_home, 'p_draw': p_draw, 'p_away': p_away})
    probs_df = pd.DataFrame(probs)
    return pd.concat([df.reset_index(drop=True), probs_df], axis=1)
