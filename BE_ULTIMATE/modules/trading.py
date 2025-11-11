#!/usr/bin/env python3
# trading.py - Módulo de Trading Financeiro com MetaTrader 5
# Análise de mercados, notícias e estratégias automatizadas

import sys
import os
import json
import time
import requests
from datetime import datetime, timedelta
import numpy as np

# Tentar importar MT5 (pode não funcionar no Android)
try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False
    print("[Trading] MetaTrader5 não disponível no Android - usando simulação")

class TradingEngine:
    """
    Motor de Trading Financeiro Inteligente
    - Análise de mercados em tempo real
    - Notícias que impactam mercados
    - Estratégias automatizadas
    - Gestão de risco
    """
    
    def __init__(self, config=None):
        self.config = config or {}
        self.capital = self.config.get('capital', 1000.0)
        self.max_risk_per_trade = self.config.get('max_risk', 0.02)  # 2%
        self.positions = []
        self.history = []
        self.mt5_connected = False
        
        # Tentar conectar ao MT5
        if MT5_AVAILABLE:
            self.connect_mt5()
    
    def connect_mt5(self):
        """Conecta ao MetaTrader 5."""
        try:
            if not mt5.initialize():
                print(f"[Trading] Erro ao inicializar MT5: {mt5.last_error()}")
                return False
            
            # Login (se configurado)
            login = self.config.get('mt5_login')
            password = self.config.get('mt5_password')
            server = self.config.get('mt5_server')
            
            if login and password and server:
                if mt5.login(login, password, server):
                    print(f"[Trading] ✅ Conectado ao MT5: {server}")
                    self.mt5_connected = True
                    return True
                else:
                    print(f"[Trading] ❌ Erro ao fazer login: {mt5.last_error()}")
            else:
                print("[Trading] ⚠️ Credenciais MT5 não configuradas - modo simulação")
            
            return False
        except Exception as e:
            print(f"[Trading] Erro ao conectar MT5: {e}")
            return False
    
    def get_market_data(self, symbol='USDBRL', timeframe='H1', bars=100):
        """Busca dados de mercado."""
        if self.mt5_connected:
            try:
                # Converter timeframe
                tf_map = {
                    'M1': mt5.TIMEFRAME_M1,
                    'M5': mt5.TIMEFRAME_M5,
                    'M15': mt5.TIMEFRAME_M15,
                    'H1': mt5.TIMEFRAME_H1,
                    'H4': mt5.TIMEFRAME_H4,
                    'D1': mt5.TIMEFRAME_D1
                }
                
                tf = tf_map.get(timeframe, mt5.TIMEFRAME_H1)
                
                # Buscar dados
                rates = mt5.copy_rates_from_pos(symbol, tf, 0, bars)
                
                if rates is not None and len(rates) > 0:
                    return {
                        'symbol': symbol,
                        'timeframe': timeframe,
                        'data': rates,
                        'last_price': rates[-1]['close']
                    }
            except Exception as e:
                print(f"[Trading] Erro ao buscar dados MT5: {e}")
        
        # Fallback: dados simulados
        return self.get_simulated_data(symbol, bars)
    
    def get_simulated_data(self, symbol='USDBRL', bars=100):
        """Gera dados simulados para teste."""
        # Preço base por símbolo
        base_prices = {
            'USDBRL': 5.34,
            'EURUSD': 1.08,
            'GBPUSD': 1.25,
            'BTCUSD': 65000.0,
            'ETHUSD': 3500.0
        }
        
        base_price = base_prices.get(symbol, 100.0)
        
        # Gerar série temporal com random walk
        prices = [base_price]
        for _ in range(bars - 1):
            change = np.random.normal(0, base_price * 0.001)  # 0.1% volatilidade
            prices.append(prices[-1] + change)
        
        return {
            'symbol': symbol,
            'timeframe': 'H1',
            'data': np.array(prices),
            'last_price': prices[-1]
        }
    
    def fetch_financial_news(self, query='forex'):
        """Busca notícias financeiras que impactam mercados."""
        api_key = self.config.get('news_api_key')
        
        if not api_key:
            return self.get_simulated_news()
        
        try:
            url = f"https://newsapi.org/v2/everything"
            params = {
                'q': query,
                'apiKey': api_key,
                'language': 'pt',
                'sortBy': 'publishedAt',
                'pageSize': 10
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                
                return [{
                    'title': art['title'],
                    'description': art.get('description', ''),
                    'source': art['source']['name'],
                    'published': art['publishedAt'],
                    'url': art['url']
                } for art in articles[:5]]
        except Exception as e:
            print(f"[Trading] Erro ao buscar notícias: {e}")
        
        return self.get_simulated_news()
    
    def get_simulated_news(self):
        """Notícias simuladas."""
        return [
            {
                'title': 'Dólar sobe com tensões geopolíticas',
                'description': 'Moeda americana ganha força no mercado',
                'source': 'Simulado',
                'published': datetime.now().isoformat(),
                'impact': 'positive_usd'
            },
            {
                'title': 'Fed mantém taxa de juros',
                'description': 'Decisão era esperada pelo mercado',
                'source': 'Simulado',
                'published': datetime.now().isoformat(),
                'impact': 'neutral'
            }
        ]
    
    def analyze_sentiment(self, news):
        """Analisa sentimento das notícias."""
        # Palavras-chave positivas e negativas
        positive_keywords = ['sobe', 'alta', 'crescimento', 'lucro', 'positivo', 'forte']
        negative_keywords = ['cai', 'baixa', 'queda', 'prejuízo', 'negativo', 'fraco']
        
        sentiment_score = 0
        
        for article in news:
            text = (article.get('title', '') + ' ' + article.get('description', '')).lower()
            
            for word in positive_keywords:
                if word in text:
                    sentiment_score += 1
            
            for word in negative_keywords:
                if word in text:
                    sentiment_score -= 1
        
        # Normalizar
        if len(news) > 0:
            sentiment_score /= len(news)
        
        return sentiment_score  # -1 a 1
    
    def calculate_indicators(self, data):
        """Calcula indicadores técnicos."""
        prices = data['data'] if isinstance(data['data'], np.ndarray) else np.array([d['close'] for d in data['data']])
        
        # SMA (Simple Moving Average)
        sma_20 = np.mean(prices[-20:]) if len(prices) >= 20 else np.mean(prices)
        sma_50 = np.mean(prices[-50:]) if len(prices) >= 50 else np.mean(prices)
        
        # RSI (Relative Strength Index)
        rsi = self.calculate_rsi(prices)
        
        # MACD
        macd, signal = self.calculate_macd(prices)
        
        return {
            'sma_20': sma_20,
            'sma_50': sma_50,
            'rsi': rsi,
            'macd': macd,
            'macd_signal': signal,
            'last_price': prices[-1]
        }
    
    def calculate_rsi(self, prices, period=14):
        """Calcula RSI."""
        if len(prices) < period + 1:
            return 50.0  # Neutro
        
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calcula MACD."""
        if len(prices) < slow:
            return 0.0, 0.0
        
        # EMA rápida e lenta
        ema_fast = self.ema(prices, fast)
        ema_slow = self.ema(prices, slow)
        
        macd = ema_fast - ema_slow
        macd_signal = self.ema(np.array([macd]), signal)
        
        return macd, macd_signal
    
    def ema(self, prices, period):
        """Calcula EMA (Exponential Moving Average)."""
        if len(prices) < period:
            return np.mean(prices)
        
        multiplier = 2 / (period + 1)
        ema = np.mean(prices[:period])
        
        for price in prices[period:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
        
        return ema
    
    def generate_signal(self, symbol='USDBRL'):
        """Gera sinal de trading baseado em análise técnica e fundamental."""
        # Buscar dados
        market_data = self.get_market_data(symbol)
        news = self.fetch_financial_news(symbol)
        
        # Análise técnica
        indicators = self.calculate_indicators(market_data)
        
        # Análise fundamental (sentimento)
        sentiment = self.analyze_sentiment(news)
        
        # Lógica de decisão
        signal = 'HOLD'
        confidence = 0.5
        
        # Condições para BUY
        buy_conditions = 0
        if indicators['last_price'] < indicators['sma_20']:
            buy_conditions += 1
        if indicators['rsi'] < 30:  # Oversold
            buy_conditions += 1
        if indicators['macd'] > indicators['macd_signal']:
            buy_conditions += 1
        if sentiment > 0.3:
            buy_conditions += 1
        
        # Condições para SELL
        sell_conditions = 0
        if indicators['last_price'] > indicators['sma_20']:
            sell_conditions += 1
        if indicators['rsi'] > 70:  # Overbought
            sell_conditions += 1
        if indicators['macd'] < indicators['macd_signal']:
            sell_conditions += 1
        if sentiment < -0.3:
            sell_conditions += 1
        
        # Decisão
        if buy_conditions >= 3:
            signal = 'BUY'
            confidence = buy_conditions / 4
        elif sell_conditions >= 3:
            signal = 'SELL'
            confidence = sell_conditions / 4
        
        return {
            'symbol': symbol,
            'signal': signal,
            'confidence': confidence,
            'price': indicators['last_price'],
            'indicators': indicators,
            'sentiment': sentiment,
            'timestamp': datetime.now().isoformat()
        }
    
    def calculate_position_size(self, signal):
        """Calcula tamanho da posição baseado em risco."""
        risk_amount = self.capital * self.max_risk_per_trade
        
        # Stop loss de 2%
        stop_loss_percent = 0.02
        stop_loss_amount = signal['price'] * stop_loss_percent
        
        # Tamanho da posição
        position_size = risk_amount / stop_loss_amount
        
        return min(position_size, self.capital * 0.1)  # Máximo 10% do capital
    
    def execute_trade(self, signal):
        """Executa trade (simulado ou real)."""
        if signal['signal'] == 'HOLD':
            return None
        
        position_size = self.calculate_position_size(signal)
        
        trade = {
            'symbol': signal['symbol'],
            'type': signal['signal'],
            'entry_price': signal['price'],
            'size': position_size,
            'timestamp': datetime.now().isoformat(),
            'status': 'open',
            'confidence': signal['confidence']
        }
        
        self.positions.append(trade)
        
        print(f"[Trading] 🚀 {signal['signal']} {signal['symbol']} @ {signal['price']:.4f}")
        print(f"[Trading] 💰 Tamanho: {position_size:.2f}")
        print(f"[Trading] 📊 Confiança: {signal['confidence']*100:.1f}%")
        
        return trade
    
    def run_strategy(self, symbols=['USDBRL', 'EURUSD', 'BTCUSD']):
        """Executa estratégia de trading em múltiplos símbolos."""
        print("[Trading] 🔍 Analisando mercados...")
        
        signals = []
        
        for symbol in symbols:
            signal = self.generate_signal(symbol)
            signals.append(signal)
            
            if signal['signal'] != 'HOLD' and signal['confidence'] > 0.7:
                self.execute_trade(signal)
        
        return signals


# Teste
if __name__ == "__main__":
    config = {
        'capital': 1000.0,
        'max_risk': 0.02
    }
    
    engine = TradingEngine(config)
    signals = engine.run_strategy(['USDBRL', 'EURUSD', 'BTCUSD'])
    
    for signal in signals:
        print(f"\n{signal['symbol']}: {signal['signal']} ({signal['confidence']*100:.1f}%)")

