#!/usr/bin/env python3
# iq_option.py - Módulo IQ Option com Visão Computacional
# Monitoramento de tela, detecção de padrões e sinais automáticos

import sys
import os
import json
import time
import numpy as np
from datetime import datetime
from PIL import Image, ImageGrab
import subprocess

# Tentar importar OpenCV
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("[IQ Option] OpenCV não disponível - funcionalidade limitada")

class IQOptionBot:
    """
    Bot para IQ Option com Visão Computacional
    - Monitoramento de tela
    - Detecção de padrões de candlesticks
    - Sinais automáticos CALL/PUT
    - Análise de tendências
    """
    
    def __init__(self, config=None):
        self.config = config or {}
        self.capital = self.config.get('capital', 100.0)
        self.stake_percent = self.config.get('stake_percent', 0.05)  # 5%
        self.history = []
        self.patterns = self.load_patterns()
        
        print("[IQ Option] 🤖 Bot inicializado")
    
    def load_patterns(self):
        """Carrega padrões de candlesticks conhecidos."""
        return {
            'hammer': {
                'description': 'Martelo - Reversão de baixa para alta',
                'signal': 'CALL',
                'confidence': 0.7
            },
            'shooting_star': {
                'description': 'Estrela Cadente - Reversão de alta para baixa',
                'signal': 'PUT',
                'confidence': 0.7
            },
            'engulfing_bullish': {
                'description': 'Engolfo de Alta',
                'signal': 'CALL',
                'confidence': 0.8
            },
            'engulfing_bearish': {
                'description': 'Engolfo de Baixa',
                'signal': 'PUT',
                'confidence': 0.8
            },
            'doji': {
                'description': 'Doji - Indecisão',
                'signal': 'HOLD',
                'confidence': 0.5
            }
        }
    
    def capture_screen(self, region=None):
        """Captura tela ou região específica."""
        try:
            if region:
                # Capturar região específica (x, y, width, height)
                screenshot = ImageGrab.grab(bbox=region)
            else:
                # Capturar tela inteira
                screenshot = ImageGrab.grab()
            
            return np.array(screenshot)
        except Exception as e:
            print(f"[IQ Option] Erro ao capturar tela: {e}")
            return None
    
    def capture_screen_termux(self):
        """Captura tela no Termux usando termux-api."""
        try:
            # Usar termux-api para capturar tela
            filename = f"/sdcard/Pictures/iq_screenshot_{int(time.time())}.png"
            subprocess.run(['termux-camera-photo', '-c', '0', filename], check=True)
            
            # Carregar imagem
            img = Image.open(filename)
            return np.array(img)
        except Exception as e:
            print(f"[IQ Option] Erro ao capturar tela no Termux: {e}")
            return self.generate_simulated_chart()
    
    def generate_simulated_chart(self):
        """Gera gráfico simulado para teste."""
        # Criar imagem 800x600
        img = np.zeros((600, 800, 3), dtype=np.uint8)
        
        # Simular candlesticks
        num_candles = 20
        candle_width = 30
        spacing = 10
        
        prices = []
        current_price = 100
        
        for i in range(num_candles):
            # Gerar OHLC
            open_price = current_price
            high_price = current_price + np.random.uniform(0, 5)
            low_price = current_price - np.random.uniform(0, 5)
            close_price = current_price + np.random.uniform(-3, 3)
            
            prices.append({
                'open': open_price,
                'high': high_price,
                'low': low_price,
                'close': close_price
            })
            
            current_price = close_price
            
            # Desenhar candlestick
            x = 50 + i * (candle_width + spacing)
            
            # Normalizar preços para coordenadas Y
            y_scale = 5
            y_offset = 300
            
            y_open = int(y_offset - open_price * y_scale)
            y_close = int(y_offset - close_price * y_scale)
            y_high = int(y_offset - high_price * y_scale)
            y_low = int(y_offset - low_price * y_scale)
            
            # Cor: verde se alta, vermelho se baixa
            color = (0, 255, 0) if close_price > open_price else (0, 0, 255)
            
            # Desenhar pavio
            cv2.line(img, (x + candle_width//2, y_high), (x + candle_width//2, y_low), (255, 255, 255), 1)
            
            # Desenhar corpo
            cv2.rectangle(img, (x, y_open), (x + candle_width, y_close), color, -1)
        
        return img, prices
    
    def detect_pattern(self, candles):
        """Detecta padrões de candlesticks."""
        if len(candles) < 2:
            return None
        
        last_candle = candles[-1]
        prev_candle = candles[-2] if len(candles) > 1 else None
        
        # Calcular propriedades do último candle
        body = abs(last_candle['close'] - last_candle['open'])
        upper_shadow = last_candle['high'] - max(last_candle['open'], last_candle['close'])
        lower_shadow = min(last_candle['open'], last_candle['close']) - last_candle['low']
        total_range = last_candle['high'] - last_candle['low']
        
        # Detectar Hammer
        if (lower_shadow > body * 2 and 
            upper_shadow < body * 0.1 and
            last_candle['close'] > last_candle['open']):
            return 'hammer'
        
        # Detectar Shooting Star
        if (upper_shadow > body * 2 and 
            lower_shadow < body * 0.1 and
            last_candle['close'] < last_candle['open']):
            return 'shooting_star'
        
        # Detectar Engolfo de Alta
        if (prev_candle and
            prev_candle['close'] < prev_candle['open'] and  # Prev é baixa
            last_candle['close'] > last_candle['open'] and  # Current é alta
            last_candle['open'] < prev_candle['close'] and
            last_candle['close'] > prev_candle['open']):
            return 'engulfing_bullish'
        
        # Detectar Engolfo de Baixa
        if (prev_candle and
            prev_candle['close'] > prev_candle['open'] and  # Prev é alta
            last_candle['close'] < last_candle['open'] and  # Current é baixa
            last_candle['open'] > prev_candle['close'] and
            last_candle['close'] < prev_candle['open']):
            return 'engulfing_bearish'
        
        # Detectar Doji
        if body < total_range * 0.1:
            return 'doji'
        
        return None
    
    def analyze_trend(self, candles, period=5):
        """Analisa tendência dos últimos N candles."""
        if len(candles) < period:
            return 'NEUTRAL'
        
        recent = candles[-period:]
        
        # Calcular média de fechamentos
        closes = [c['close'] for c in recent]
        
        # Regressão linear simples
        x = np.arange(len(closes))
        slope = np.polyfit(x, closes, 1)[0]
        
        if slope > 0.5:
            return 'UPTREND'
        elif slope < -0.5:
            return 'DOWNTREND'
        else:
            return 'NEUTRAL'
    
    def calculate_rsi(self, candles, period=14):
        """Calcula RSI dos candles."""
        if len(candles) < period + 1:
            return 50.0
        
        closes = [c['close'] for c in candles]
        deltas = np.diff(closes)
        
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def generate_signal(self, candles=None):
        """Gera sinal de trading baseado em análise."""
        if candles is None:
            # Gerar candles simulados
            _, candles = self.generate_simulated_chart()
        
        # Detectar padrão
        pattern = self.detect_pattern(candles)
        
        # Analisar tendência
        trend = self.analyze_trend(candles)
        
        # Calcular RSI
        rsi = self.calculate_rsi(candles)
        
        # Gerar sinal
        signal = 'HOLD'
        confidence = 0.5
        reason = 'Nenhum padrão detectado'
        
        if pattern and pattern in self.patterns:
            pattern_info = self.patterns[pattern]
            signal = pattern_info['signal']
            confidence = pattern_info['confidence']
            reason = pattern_info['description']
            
            # Ajustar confiança baseado em tendência e RSI
            if signal == 'CALL':
                if trend == 'UPTREND':
                    confidence += 0.1
                if rsi < 30:  # Oversold
                    confidence += 0.1
            elif signal == 'PUT':
                if trend == 'DOWNTREND':
                    confidence += 0.1
                if rsi > 70:  # Overbought
                    confidence += 0.1
            
            confidence = min(confidence, 1.0)
        
        return {
            'signal': signal,
            'confidence': confidence,
            'pattern': pattern,
            'trend': trend,
            'rsi': rsi,
            'reason': reason,
            'timestamp': datetime.now().isoformat(),
            'price': candles[-1]['close'] if candles else 0
        }
    
    def calculate_stake(self):
        """Calcula valor da aposta."""
        return round(self.capital * self.stake_percent, 2)
    
    def execute_trade(self, signal):
        """Executa trade (simulado)."""
        if signal['signal'] == 'HOLD':
            return None
        
        stake = self.calculate_stake()
        
        # Simular resultado (baseado em confiança)
        won = np.random.random() < signal['confidence']
        
        payout = 0.85  # 85% de retorno
        
        if won:
            profit = stake * payout
            self.capital += profit
            result = 'WIN'
        else:
            self.capital -= stake
            profit = -stake
            result = 'LOSS'
        
        trade = {
            'signal': signal['signal'],
            'stake': stake,
            'result': result,
            'profit': profit,
            'capital': self.capital,
            'confidence': signal['confidence'],
            'pattern': signal['pattern'],
            'timestamp': datetime.now().isoformat()
        }
        
        self.history.append(trade)
        
        emoji = '✅' if won else '❌'
        print(f"[IQ Option] {emoji} {signal['signal']} - R$ {stake:.2f} - {result}")
        print(f"[IQ Option] 💰 Capital: R$ {self.capital:.2f}")
        
        return trade
    
    def run_bot(self, num_trades=10):
        """Executa bot por N trades."""
        print(f"[IQ Option] 🚀 Iniciando bot - {num_trades} trades")
        
        for i in range(num_trades):
            print(f"\n[IQ Option] 📊 Trade {i+1}/{num_trades}")
            
            # Gerar sinal
            signal = self.generate_signal()
            
            print(f"[IQ Option] 🎯 Sinal: {signal['signal']}")
            print(f"[IQ Option] 📈 Padrão: {signal['pattern']}")
            print(f"[IQ Option] 📊 Tendência: {signal['trend']}")
            print(f"[IQ Option] 💡 Confiança: {signal['confidence']*100:.1f}%")
            
            # Executar trade se confiança > 60%
            if signal['confidence'] > 0.6:
                self.execute_trade(signal)
            else:
                print(f"[IQ Option] ⏸️  Confiança baixa - aguardando...")
            
            time.sleep(2)  # Aguardar 2 segundos entre trades
        
        # Estatísticas finais
        self.print_statistics()
    
    def print_statistics(self):
        """Imprime estatísticas do bot."""
        if not self.history:
            print("[IQ Option] Nenhum trade executado")
            return
        
        wins = sum(1 for t in self.history if t['result'] == 'WIN')
        losses = len(self.history) - wins
        win_rate = (wins / len(self.history)) * 100
        
        total_profit = sum(t['profit'] for t in self.history)
        
        print("\n" + "="*50)
        print("[IQ Option] 📊 ESTATÍSTICAS FINAIS")
        print("="*50)
        print(f"Total de trades: {len(self.history)}")
        print(f"Vitórias: {wins}")
        print(f"Derrotas: {losses}")
        print(f"Taxa de acerto: {win_rate:.1f}%")
        print(f"Lucro total: R$ {total_profit:.2f}")
        print(f"Capital final: R$ {self.capital:.2f}")
        print("="*50)


# Teste
if __name__ == "__main__":
    bot = IQOptionBot({'capital': 100.0, 'stake_percent': 0.05})
    bot.run_bot(num_trades=10)

