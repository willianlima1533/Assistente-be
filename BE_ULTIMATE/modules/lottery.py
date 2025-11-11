#!/usr/bin/env python3
# lottery.py - Módulo de Loteria Caixa com IA
# Análise de padrões, frequências e geração inteligente de números

import sys
import os
import json
import requests
import numpy as np
from datetime import datetime
from collections import Counter
import itertools

class LotteryAI:
    """
    IA para Loteria Caixa
    - Análise de resultados históricos
    - Detecção de padrões e frequências
    - Geração inteligente de jogos
    - Múltiplas estratégias
    """
    
    def __init__(self, game_type='mega_sena'):
        self.game_type = game_type
        self.config = self.get_game_config(game_type)
        self.historical_data = []
        self.load_historical_data()
        
        print(f"[Loteria] 🎲 IA inicializada para {game_type}")
    
    def get_game_config(self, game_type):
        """Retorna configuração do jogo."""
        configs = {
            'mega_sena': {
                'name': 'Mega-Sena',
                'min_number': 1,
                'max_number': 60,
                'numbers_per_game': 6,
                'min_bet': 6,
                'max_bet': 15,
                'prize_tiers': [6, 5, 4]
            },
            'quina': {
                'name': 'Quina',
                'min_number': 1,
                'max_number': 80,
                'numbers_per_game': 5,
                'min_bet': 5,
                'max_bet': 15,
                'prize_tiers': [5, 4, 3, 2]
            },
            'lotofacil': {
                'name': 'Lotofácil',
                'min_number': 1,
                'max_number': 25,
                'numbers_per_game': 15,
                'min_bet': 15,
                'max_bet': 20,
                'prize_tiers': [15, 14, 13, 12, 11]
            },
            'lotomania': {
                'name': 'Lotomania',
                'min_number': 0,
                'max_number': 99,
                'numbers_per_game': 50,
                'min_bet': 50,
                'max_bet': 50,
                'prize_tiers': [20, 19, 18, 17, 16, 0]
            }
        }
        
        return configs.get(game_type, configs['mega_sena'])
    
    def load_historical_data(self):
        """Carrega dados históricos da loteria."""
        # Tentar buscar da API da Caixa
        try:
            data = self.fetch_from_api()
            if data:
                self.historical_data = data
                return
        except Exception as e:
            print(f"[Loteria] Erro ao buscar API: {e}")
        
        # Fallback: gerar dados simulados
        self.historical_data = self.generate_simulated_data(100)
    
    def fetch_from_api(self):
        """Busca resultados da API da Caixa."""
        # API não oficial da Loteria
        urls = {
            'mega_sena': 'https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena',
            'quina': 'https://servicebus2.caixa.gov.br/portaldeloterias/api/quina',
            'lotofacil': 'https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil'
        }
        
        url = urls.get(self.game_type)
        if not url:
            return None
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Processar dados
            return self.parse_api_data(data)
        
        return None
    
    def parse_api_data(self, data):
        """Processa dados da API."""
        results = []
        
        # Formato varia por jogo
        if isinstance(data, list):
            for draw in data:
                numbers = draw.get('dezenas', [])
                results.append({
                    'contest': draw.get('numero', 0),
                    'date': draw.get('data', ''),
                    'numbers': [int(n) for n in numbers]
                })
        
        return results
    
    def generate_simulated_data(self, num_draws=100):
        """Gera dados simulados para teste."""
        results = []
        
        for i in range(num_draws):
            # Gerar números aleatórios
            numbers = sorted(np.random.choice(
                range(self.config['min_number'], self.config['max_number'] + 1),
                size=self.config['numbers_per_game'],
                replace=False
            ).tolist())
            
            results.append({
                'contest': i + 1,
                'date': datetime.now().isoformat(),
                'numbers': numbers
            })
        
        return results
    
    def analyze_frequency(self):
        """Analisa frequência de cada número."""
        all_numbers = []
        
        for draw in self.historical_data:
            all_numbers.extend(draw['numbers'])
        
        frequency = Counter(all_numbers)
        
        # Ordenar por frequência
        sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'frequency': dict(frequency),
            'most_common': sorted_freq[:10],
            'least_common': sorted_freq[-10:],
            'total_draws': len(self.historical_data)
        }
    
    def analyze_patterns(self):
        """Analisa padrões nos sorteios."""
        patterns = {
            'consecutive': 0,
            'same_decade': 0,
            'even_odd_ratio': [],
            'sum_range': []
        }
        
        for draw in self.historical_data:
            numbers = draw['numbers']
            
            # Números consecutivos
            for i in range(len(numbers) - 1):
                if numbers[i+1] - numbers[i] == 1:
                    patterns['consecutive'] += 1
            
            # Mesma dezena
            decades = [n // 10 for n in numbers]
            if len(set(decades)) < len(decades):
                patterns['same_decade'] += 1
            
            # Razão par/ímpar
            even = sum(1 for n in numbers if n % 2 == 0)
            odd = len(numbers) - even
            patterns['even_odd_ratio'].append((even, odd))
            
            # Soma dos números
            patterns['sum_range'].append(sum(numbers))
        
        # Calcular médias
        avg_even_odd = np.mean([e for e, o in patterns['even_odd_ratio']])
        avg_sum = np.mean(patterns['sum_range'])
        
        return {
            'consecutive_freq': patterns['consecutive'] / len(self.historical_data),
            'same_decade_freq': patterns['same_decade'] / len(self.historical_data),
            'avg_even': avg_even_odd,
            'avg_odd': self.config['numbers_per_game'] - avg_even_odd,
            'avg_sum': avg_sum,
            'sum_std': np.std(patterns['sum_range'])
        }
    
    def analyze_delays(self):
        """Analisa atrasos (números que não saem há muito tempo)."""
        max_number = self.config['max_number']
        min_number = self.config['min_number']
        
        # Última aparição de cada número
        last_seen = {n: -1 for n in range(min_number, max_number + 1)}
        
        for i, draw in enumerate(self.historical_data):
            for number in draw['numbers']:
                last_seen[number] = i
        
        # Calcular atraso
        current_draw = len(self.historical_data)
        delays = {n: current_draw - last for n, last in last_seen.items()}
        
        # Ordenar por atraso
        sorted_delays = sorted(delays.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'delays': delays,
            'most_delayed': sorted_delays[:10],
            'least_delayed': sorted_delays[-10:]
        }
    
    def generate_numbers_frequency(self):
        """Gera números baseado em frequência."""
        freq_analysis = self.analyze_frequency()
        
        # Pegar números mais frequentes
        most_common = [n for n, f in freq_analysis['most_common']]
        
        # Adicionar alguns menos frequentes para diversificar
        least_common = [n for n, f in freq_analysis['least_common']]
        
        # Combinar: 70% mais frequentes, 30% menos frequentes
        num_from_common = int(self.config['numbers_per_game'] * 0.7)
        num_from_rare = self.config['numbers_per_game'] - num_from_common
        
        selected = []
        selected.extend(np.random.choice(most_common[:20], size=num_from_common, replace=False))
        selected.extend(np.random.choice(least_common[:20], size=num_from_rare, replace=False))
        
        return sorted(selected)
    
    def generate_numbers_delay(self):
        """Gera números baseado em atraso."""
        delay_analysis = self.analyze_delays()
        
        # Pegar números mais atrasados
        most_delayed = [n for n, d in delay_analysis['most_delayed']]
        
        # Selecionar aleatoriamente dos mais atrasados
        selected = np.random.choice(most_delayed[:30], size=self.config['numbers_per_game'], replace=False)
        
        return sorted(selected)
    
    def generate_numbers_pattern(self):
        """Gera números baseado em padrões."""
        pattern_analysis = self.analyze_patterns()
        
        # Usar razão par/ímpar média
        target_even = int(pattern_analysis['avg_even'])
        target_odd = self.config['numbers_per_game'] - target_even
        
        # Gerar números pares e ímpares
        max_num = self.config['max_number']
        min_num = self.config['min_number']
        
        even_numbers = [n for n in range(min_num, max_num + 1) if n % 2 == 0]
        odd_numbers = [n for n in range(min_num, max_num + 1) if n % 2 != 0]
        
        selected = []
        selected.extend(np.random.choice(even_numbers, size=target_even, replace=False))
        selected.extend(np.random.choice(odd_numbers, size=target_odd, replace=False))
        
        return sorted(selected)
    
    def generate_numbers_random(self):
        """Gera números completamente aleatórios."""
        numbers = np.random.choice(
            range(self.config['min_number'], self.config['max_number'] + 1),
            size=self.config['numbers_per_game'],
            replace=False
        )
        
        return sorted(numbers.tolist())
    
    def generate_numbers_hybrid(self):
        """Gera números usando estratégia híbrida."""
        # Combinar múltiplas estratégias
        strategies = [
            self.generate_numbers_frequency,
            self.generate_numbers_delay,
            self.generate_numbers_pattern,
            self.generate_numbers_random
        ]
        
        # Gerar com cada estratégia
        all_numbers = []
        for strategy in strategies:
            all_numbers.extend(strategy())
        
        # Contar frequência
        number_freq = Counter(all_numbers)
        
        # Selecionar os mais frequentes
        most_common = [n for n, f in number_freq.most_common()]
        
        # Pegar quantidade necessária
        selected = most_common[:self.config['numbers_per_game']]
        
        return sorted(selected)
    
    def generate_game(self, strategy='hybrid', num_games=1):
        """Gera jogo(s) com estratégia escolhida."""
        strategies = {
            'frequency': self.generate_numbers_frequency,
            'delay': self.generate_numbers_delay,
            'pattern': self.generate_numbers_pattern,
            'random': self.generate_numbers_random,
            'hybrid': self.generate_numbers_hybrid
        }
        
        strategy_func = strategies.get(strategy, self.generate_numbers_hybrid)
        
        games = []
        for _ in range(num_games):
            numbers = strategy_func()
            games.append({
                'numbers': numbers,
                'strategy': strategy,
                'game_type': self.game_type,
                'timestamp': datetime.now().isoformat()
            })
        
        return games
    
    def print_analysis(self):
        """Imprime análise completa."""
        print("\n" + "="*60)
        print(f"[Loteria] 📊 ANÁLISE - {self.config['name']}")
        print("="*60)
        
        # Frequência
        freq = self.analyze_frequency()
        print("\n🔢 NÚMEROS MAIS FREQUENTES:")
        for num, count in freq['most_common'][:5]:
            print(f"   {num:02d}: {count} vezes")
        
        print("\n🔢 NÚMEROS MENOS FREQUENTES:")
        for num, count in freq['least_common'][:5]:
            print(f"   {num:02d}: {count} vezes")
        
        # Padrões
        patterns = self.analyze_patterns()
        print(f"\n📈 PADRÕES:")
        print(f"   Média de pares: {patterns['avg_even']:.1f}")
        print(f"   Média de ímpares: {patterns['avg_odd']:.1f}")
        print(f"   Soma média: {patterns['avg_sum']:.1f}")
        
        # Atrasos
        delays = self.analyze_delays()
        print("\n⏰ NÚMEROS MAIS ATRASADOS:")
        for num, delay in delays['most_delayed'][:5]:
            print(f"   {num:02d}: {delay} sorteios atrás")
        
        print("="*60)
    
    def print_games(self, games):
        """Imprime jogos gerados."""
        print("\n" + "="*60)
        print(f"[Loteria] 🎲 JOGOS GERADOS - {self.config['name']}")
        print("="*60)
        
        for i, game in enumerate(games, 1):
            numbers_str = ' - '.join([f"{n:02d}" for n in game['numbers']])
            print(f"\nJogo {i} ({game['strategy']}):")
            print(f"   {numbers_str}")
        
        print("="*60)


# Teste
if __name__ == "__main__":
    # Mega-Sena
    lottery = LotteryAI('mega_sena')
    lottery.print_analysis()
    
    games = lottery.generate_game(strategy='hybrid', num_games=3)
    lottery.print_games(games)

