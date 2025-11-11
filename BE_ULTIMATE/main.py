#!/usr/bin/env python3
"""
BE ULTIMATE - Bot de Estratégias Inteligentes
Sistema completo com todas as funcionalidades integradas
"""

import sys
import os
import time
import json
from datetime import datetime

# Adicionar módulos ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

# Importar módulos
try:
    from trading import TradingEngine
    from iq_option import IQOptionBot
    from lottery import LotteryAI
    from coaching import CoachingAI
    from auto_evolution import AutoEvolutionAI
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    print("Executando em modo limitado...")

class BEUltimate:
    """
    BE Ultimate - Sistema Integrado
    Combina todos os módulos em um único sistema inteligente
    """
    
    def __init__(self):
        self.version = "2.0.0"
        self.start_time = datetime.now()
        
        print(self.get_banner())
        
        # Inicializar módulos
        self.modules = {}
        self.initialize_modules()
        
        # Estado global
        self.state = {
            'capital_total': 10000.0,
            'capital_betting': 1000.0,
            'capital_trading': 5000.0,
            'capital_lottery': 100.0,
            'capital_reserve': 3900.0,
            'total_profit': 0.0,
            'operations_today': 0,
            'active': True
        }
    
    def get_banner(self):
        return f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              🧠 BE ULTIMATE v{self.version}                      ║
║         Bot de Estratégias Inteligentes                     ║
║                                                              ║
║  🎲 Apostas Esportivas  |  💹 Trading Financeiro            ║
║  🎰 Loteria com IA      |  🎯 Coaching Pessoal              ║
║  🤖 Auto-Evolução       |  📊 Análise Avançada              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
    
    def initialize_modules(self):
        """Inicializa todos os módulos."""
        print("\n[BE] 🚀 Inicializando módulos...")
        
        try:
            # Trading
            self.modules['trading'] = TradingEngine({
                'capital': self.state['capital_trading'],
                'max_risk': 0.02
            })
            print("[BE] ✅ Trading Engine inicializado")
        except Exception as e:
            print(f"[BE] ⚠️  Trading Engine: {e}")
        
        try:
            # IQ Option
            self.modules['iq_option'] = IQOptionBot({
                'capital': self.state['capital_betting'],
                'stake_percent': 0.05
            })
            print("[BE] ✅ IQ Option Bot inicializado")
        except Exception as e:
            print(f"[BE] ⚠️  IQ Option Bot: {e}")
        
        try:
            # Loteria
            self.modules['lottery'] = LotteryAI('mega_sena')
            print("[BE] ✅ Lottery AI inicializado")
        except Exception as e:
            print(f"[BE] ⚠️  Lottery AI: {e}")
        
        try:
            # Coaching
            self.modules['coaching'] = CoachingAI()
            print("[BE] ✅ Coaching AI inicializado")
        except Exception as e:
            print(f"[BE] ⚠️  Coaching AI: {e}")
        
        try:
            # Auto-Evolution
            self.modules['evolution'] = AutoEvolutionAI()
            print("[BE] ✅ Auto-Evolution AI inicializado")
        except Exception as e:
            print(f"[BE] ⚠️  Auto-Evolution AI: {e}")
        
        print(f"\n[BE] ✅ {len(self.modules)} módulos ativos\n")
    
    def run_daily_routine(self):
        """Executa rotina diária."""
        print("\n" + "="*60)
        print(f"[BE] 🌅 ROTINA DIÁRIA - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print("="*60)
        
        # 1. Coaching diário
        if 'coaching' in self.modules:
            print("\n[1/5] 🎯 COACHING DIÁRIO")
            self.modules['coaching'].print_daily_coaching()
        
        # 2. Análise de mercados
        if 'trading' in self.modules:
            print("\n[2/5] 💹 ANÁLISE DE MERCADOS")
            signals = self.modules['trading'].run_strategy(['USDBRL', 'EURUSD', 'BTCUSD'])
            for signal in signals:
                if signal['signal'] != 'HOLD':
                    print(f"  📊 {signal['symbol']}: {signal['signal']} ({signal['confidence']*100:.1f}%)")
        
        # 3. IQ Option
        if 'iq_option' in self.modules:
            print("\n[3/5] 🎲 IQ OPTION")
            signal = self.modules['iq_option'].generate_signal()
            if signal['signal'] != 'HOLD' and signal['confidence'] > 0.7:
                print(f"  🎯 Sinal: {signal['signal']} ({signal['confidence']*100:.1f}%)")
                print(f"  📈 Padrão: {signal['pattern']}")
        
        # 4. Loteria
        if 'lottery' in self.modules:
            print("\n[4/5] 🎰 LOTERIA")
            games = self.modules['lottery'].generate_game(strategy='hybrid', num_games=1)
            if games:
                numbers = ' - '.join([f"{n:02d}" for n in games[0]['numbers']])
                print(f"  🎲 Jogo sugerido: {numbers}")
        
        # 5. Auto-Evolução
        if 'evolution' in self.modules and self.state['operations_today'] >= 10:
            print("\n[5/5] 🧠 AUTO-EVOLUÇÃO")
            self.modules['evolution'].evolve()
        
        print("\n" + "="*60)
        print("[BE] ✅ Rotina diária concluída")
        print("="*60)
    
    def run_trading_session(self):
        """Executa sessão de trading."""
        if 'trading' not in self.modules:
            return
        
        print("\n[BE] 💹 Iniciando sessão de trading...")
        
        symbols = ['USDBRL', 'EURUSD', 'BTCUSD']
        signals = self.modules['trading'].run_strategy(symbols)
        
        for signal in signals:
            if signal['signal'] != 'HOLD' and signal['confidence'] > 0.7:
                trade = self.modules['trading'].execute_trade(signal)
                if trade:
                    self.state['operations_today'] += 1
                    
                    # Aprender com resultado (simulado)
                    if 'evolution' in self.modules:
                        result = 'win' if signal['confidence'] > 0.75 else 'loss'
                        reward = 1.0 if result == 'win' else -0.5
                        self.modules['evolution'].learn_from_result(
                            'trading_ai',
                            f"trade_{trade['symbol']}",
                            result,
                            reward
                        )
    
    def run_iq_option_session(self, num_trades=5):
        """Executa sessão de IQ Option."""
        if 'iq_option' not in self.modules:
            return
        
        print(f"\n[BE] 🎲 Iniciando sessão IQ Option ({num_trades} trades)...")
        
        for i in range(num_trades):
            signal = self.modules['iq_option'].generate_signal()
            
            if signal['confidence'] > 0.6:
                trade = self.modules['iq_option'].execute_trade(signal)
                if trade:
                    self.state['operations_today'] += 1
                    
                    # Aprender com resultado
                    if 'evolution' in self.modules:
                        reward = 1.0 if trade['result'] == 'WIN' else -0.5
                        self.modules['evolution'].learn_from_result(
                            'betting_ai',
                            f"iq_trade_{i}",
                            trade['result'],
                            reward
                        )
                
                time.sleep(1)  # Aguardar entre trades
    
    def generate_lottery_games(self, num_games=3):
        """Gera jogos de loteria."""
        if 'lottery' not in self.modules:
            return
        
        print(f"\n[BE] 🎰 Gerando {num_games} jogos de loteria...")
        
        games = self.modules['lottery'].generate_game(strategy='hybrid', num_games=num_games)
        self.modules['lottery'].print_games(games)
        
        return games
    
    def get_coaching(self):
        """Obtém coaching personalizado."""
        if 'coaching' not in self.modules:
            return
        
        self.modules['coaching'].print_daily_coaching()
        
        # Criar plano de ação
        plan = self.modules['coaching'].create_action_plan(
            'Aumentar capital em 50%',
            '60 dias'
        )
        
        print(f"\n📋 Plano de Ação:")
        print(f"   Meta: {plan['goal']}")
        print(f"   Mentor: {plan['mentor']}")
        print(f"   Estratégia: {plan['strategy']}")
    
    def print_status(self):
        """Imprime status do sistema."""
        print("\n" + "="*60)
        print("[BE] 📊 STATUS DO SISTEMA")
        print("="*60)
        
        print(f"\n💰 CAPITAL:")
        print(f"   Total: R$ {self.state['capital_total']:,.2f}")
        print(f"   Trading: R$ {self.state['capital_trading']:,.2f}")
        print(f"   Betting: R$ {self.state['capital_betting']:,.2f}")
        print(f"   Loteria: R$ {self.state['capital_lottery']:,.2f}")
        print(f"   Reserva: R$ {self.state['capital_reserve']:,.2f}")
        
        print(f"\n📊 OPERAÇÕES:")
        print(f"   Hoje: {self.state['operations_today']}")
        print(f"   Lucro Total: R$ {self.state['total_profit']:,.2f}")
        
        print(f"\n🤖 MÓDULOS ATIVOS:")
        for name in self.modules.keys():
            print(f"   ✅ {name.title()}")
        
        uptime = datetime.now() - self.start_time
        print(f"\n⏱️  Uptime: {uptime}")
        
        print("="*60)
    
    def interactive_menu(self):
        """Menu interativo."""
        while True:
            print("\n" + "="*60)
            print("[BE] 🎮 MENU PRINCIPAL")
            print("="*60)
            print("\n1. 🌅 Executar Rotina Diária")
            print("2. 💹 Sessão de Trading")
            print("3. 🎲 Sessão IQ Option")
            print("4. 🎰 Gerar Jogos de Loteria")
            print("5. 🎯 Coaching Pessoal")
            print("6. 🧠 Executar Auto-Evolução")
            print("7. 📊 Ver Status")
            print("8. 🚪 Sair")
            
            choice = input("\n[BE] Escolha uma opção: ").strip()
            
            if choice == '1':
                self.run_daily_routine()
            elif choice == '2':
                self.run_trading_session()
            elif choice == '3':
                self.run_iq_option_session()
            elif choice == '4':
                self.generate_lottery_games()
            elif choice == '5':
                self.get_coaching()
            elif choice == '6':
                if 'evolution' in self.modules:
                    self.modules['evolution'].evolve()
            elif choice == '7':
                self.print_status()
            elif choice == '8':
                print("\n[BE] 👋 Até logo!")
                break
            else:
                print("\n[BE] ❌ Opção inválida")


def main():
    """Função principal."""
    be = BEUltimate()
    
    # Executar rotina diária automaticamente
    be.run_daily_routine()
    
    # Menu interativo
    be.interactive_menu()


if __name__ == "__main__":
    main()

