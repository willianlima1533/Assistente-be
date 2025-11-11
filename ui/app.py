"""
Assistente-be Desktop UI - Painel de Controle Kivy
Simulação de iPhone com controles para o sistema de backend.
"""
import os
import threading
import sys
from pathlib import Path

# Adicionar diretórios ao path para importar módulos do backend
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR / "tools"))
sys.path.insert(0, str(BASE_DIR / "trader"))

# Importar módulos do backend
from logger import logger, log_startup, log_shutdown
from utils import load_state, save_state
from config import DRY_RUN, BANKROLL_INITIAL, SAVE_STATE_FILE
from main import main_loop # Importar a função principal do backend

# Importar Kivy
try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.uix.textinput import TextInput
    from kivy.uix.screenmanager import ScreenManager, Screen
    from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
    from kivy.clock import Clock
    from kivy.core.window import Window
    
    # Kivy 3D (para futura implementação do iPhone 3D)
    # from kivy.graphics.opengl import *
    # from kivy.graphics import *
    
except ImportError:
    logger.error("Kivy não está instalado. Execute 'pip install kivy'")
    sys.exit(1)

# Configurações iniciais da janela (simulando proporções de um iPhone)
Window.size = (400, 800)
Window.title = "Assistente-be Desktop UI"

# ============================================================================
# 1. Gerenciador de Estado da UI
# ============================================================================

class UIState:
    """Gerencia o estado da aplicação Kivy e a comunicação com o backend."""
    
    def __init__(self):
        self.is_running = False
        self.balance = BANKROLL_INITIAL
        self.status_message = "Sistema parado. Pressione INICIAR."
        self.backend_thread = None
        self.stop_event = threading.Event()
        self.load_initial_state()
        
    def load_initial_state(self):
        state = load_state()
        if state and 'balance' in state:
            self.balance = state['balance']
            self.status_message = f"Estado carregado. Saldo: R$ {self.balance:.2f}"
        
    def start_system(self):
        if not self.is_running:
            self.is_running = True
            self.status_message = "🚀 Sistema iniciado (DRY_RUN)..."
            logger.info("UI: Sistema iniciado via botão.")
            
            # Iniciar o loop principal em uma thread separada
            self.stop_event.clear() # Limpa o evento de parada
            self.backend_thread = threading.Thread(
                target=main_loop,
                kwargs={'dry_run': DRY_RUN, 'interval_minutes': 1, 'stop_event': self.stop_event}, # Passa o evento de parada
                daemon=True
            )
            self.backend_thread.start()
            
            # Agendar a atualização da UI
            Clock.schedule_interval(self.update_simulation, 5)
            return True
        return False
        
    def stop_system(self):
        if self.is_running:
            self.is_running = False
            self.status_message = "🛑 Sistema parado."
            logger.info("UI: Sistema parado via botão.")
            Clock.unschedule(self.update_simulation)
            
            # Sinalizar para a thread do backend parar
            self.stop_event.set()
            self.backend_thread.join(timeout=10) # Espera a thread terminar por 10s
            
            if self.backend_thread.is_alive():
                logger.error("UI: Thread do backend não terminou em 10s.")
            
            return True
        return False
        
    def update_simulation(self, dt):
        """Atualização de estado do backend lendo o state.json."""
        if self.is_running:
            state = load_state()
            if state and 'balance' in state:
                self.balance = state['balance']
                self.status_message = f"🔄 Rodando... Saldo: R$ {self.balance:.2f}"
            
            # Verifica se a thread do backend ainda está viva
            if not self.backend_thread.is_alive():
                self.is_running = False
                self.status_message = "❌ Backend parou inesperadamente."
                Clock.unschedule(self.update_simulation)
                logger.error("UI: Backend parou inesperadamente.")
                
        elif self.backend_thread and self.backend_thread.is_alive():
            # Caso a UI tenha parado, mas o backend ainda esteja rodando
            self.is_running = True # Corrige o estado da UI
            logger.warning("UI: Corrigindo estado. Backend ainda rodando.")

# ============================================================================
# 2. Telas da Aplicação
# ============================================================================

class MainScreen(Screen):
    """Tela principal com a simulação do iPhone e controles."""
    
    status_label = ObjectProperty(None)
    balance_label = ObjectProperty(None)
    start_button = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ui_state = App.get_running_app().ui_state
        Clock.schedule_interval(self.update_ui, 0.5)
        
    def update_ui(self, dt):
        """Atualiza os labels com o estado atual."""
        self.status_label.text = self.ui_state.status_message
        self.balance_label.text = f"Saldo: R$ {self.ui_state.balance:.2f}"
        self.start_button.text = "PARAR" if self.ui_state.is_running else "INICIAR"
        self.start_button.background_color = (0.8, 0.2, 0.2, 1) if self.ui_state.is_running else (0.2, 0.8, 0.2, 1)
        
    def toggle_system(self):
        """Inicia ou para o sistema."""
        if self.ui_state.is_running:
            self.ui_state.stop_system()
        else:
            self.ui_state.start_system()

class LoginScreen(Screen):
    """Tela para configurar logins (MetaTrader, Corretora)."""
    
    mt_login = ObjectProperty(None)
    mt_pass = ObjectProperty(None)
    broker_login = ObjectProperty(None)
    broker_pass = ObjectProperty(None)
    
    def save_logins(self):
        """Salva as credenciais no .env (simulação)."""
        # Apenas simulação de salvamento no .env, pois o .env não é lido automaticamente pelo config.py
        # Para um sistema real, usaríamos python-dotenv para ler e escrever
        
        # Obter valores
        mt_login_val = self.mt_login.text
        mt_pass_val = self.mt_pass.text
        broker_login_val = self.broker_login.text
        broker_pass_val = self.broker_pass.text
        
        logger.info(f"UI: Credenciais salvas (simulação). MT Login: {mt_login_val}")
        
        # Retornar à tela principal
        self.manager.current = 'main'

class ConfigScreen(Screen):
    """Tela para editar configurações (DRY_RUN, BANKROLL)."""
    
    dry_run_input = ObjectProperty(None)
    bankroll_input = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Carrega valores atuais
        self.dry_run_input.text = str(DRY_RUN)
        self.bankroll_input.text = str(BANKROLL_INITIAL)
        
    def save_config(self):
        """Salva as configurações no config.py (simulação)."""
        
        # Obter valores
        dry_run_val = self.dry_run_input.text.lower() == 'true'
        bankroll_val = float(self.bankroll_input.text)
        
        # Simulação de escrita no config.py
        config_path = BASE_DIR / "config.py"
        
        try:
            with open(config_path, 'r') as f:
                content = f.read()
            
            # Substituir DRY_RUN
            content = content.replace(f"DRY_RUN = {DRY_RUN}", f"DRY_RUN = {dry_run_val}")
            
            # Substituir BANKROLL_INITIAL
            content = content.replace(f"BANKROLL_INITIAL = {BANKROLL_INITIAL}", f"BANKROLL_INITIAL = {bankroll_val}")
            
            with open(config_path, 'w') as f:
                f.write(content)
                
            logger.info(f"UI: Configurações salvas em config.py. DRY_RUN={dry_run_val}, BANKROLL={bankroll_val}")
            
        except Exception as e:
            logger.error(f"UI: Erro ao salvar configurações: {e}")
            
        # Retornar à tela principal
        self.manager.current = 'main'

# ============================================================================
# 3. Aplicação Principal
# ============================================================================

class AssistenteApp(App):
    
    ui_state = UIState()
    
    def build(self):
        
        # Gerenciador de Telas
        sm = ScreenManager()
        
        # 1. Tela Principal (iPhone)
        main_screen = MainScreen(name='main')
        
        # 2. Tela de Login
        login_screen = LoginScreen(name='login')
        
        # 3. Tela de Configuração
        config_screen = ConfigScreen(name='config')
        
        sm.add_widget(main_screen)
        sm.add_widget(login_screen)
        sm.add_widget(config_screen)
        
        return sm

# ============================================================================
# 4. Kivy Language (KV) - Layout do iPhone
# ============================================================================

kv_code = """
<MainScreen>:
    status_label: status_label
    balance_label: balance_label
    start_button: start_button
    
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        
        # ------------------------------------------------
        # 1. Top Bar (Simulação de Notch/Status Bar)
        # ------------------------------------------------
        BoxLayout:
            size_hint_y: 0.1
            Label:
                text: 'Assistente-be'
                font_size: '20sp'
                color: 0, 0, 0, 1
            Label:
                text: '🔋 100%'
                size_hint_x: 0.3
                color: 0, 0, 0, 1
        
        # ------------------------------------------------
        # 2. Visualização Principal (3D/4D - Placeholder)
        # ------------------------------------------------
        BoxLayout:
            size_hint_y: 0.5
            canvas.before:
                Color:
                    rgb: 0.9, 0.9, 0.9 # Cor de fundo do "iPhone"
                Rectangle:
                    pos: self.pos
                    size: self.size
            
            Label:
                text: 'Simulação 3D/4D do iPhone aqui'
                color: 0.2, 0.2, 0.2, 1
                font_size: '18sp'
        
        # ------------------------------------------------
        # 3. Painel de Status
        # ------------------------------------------------
        GridLayout:
            cols: 2
            size_hint_y: 0.15
            padding: 10
            spacing: 5
            
            Label:
                text: 'STATUS:'
                color: 0, 0, 0, 1
                halign: 'left'
                text_size: self.size
            Label:
                id: status_label
                text: 'Sistema parado.'
                color: 0.5, 0.5, 0.5, 1
                halign: 'right'
                text_size: self.size
            
            Label:
                text: 'BANKROLL:'
                color: 0, 0, 0, 1
                halign: 'left'
                text_size: self.size
            Label:
                id: balance_label
                text: 'R$ 0.00'
                color: 0.2, 0.5, 0.2, 1
                halign: 'right'
                text_size: self.size
        
        # ------------------------------------------------
        # 4. Botões de Controle
        # ------------------------------------------------
        BoxLayout:
            size_hint_y: 0.25
            orientation: 'vertical'
            spacing: 10
            padding: 10
            
            Button:
                id: start_button
                text: 'INICIAR'
                font_size: '24sp'
                background_color: 0.2, 0.8, 0.2, 1
                on_release: root.toggle_system()
            
            BoxLayout:
                size_hint_y: 0.4
                spacing: 10
                
                Button:
                    text: 'CONFIGURAÇÕES'
                    on_release: app.root.current = 'config'
                
                Button:
                    text: 'LOGINS'
                    on_release: app.root.current = 'login'

<LoginScreen>:
    mt_login: mt_login
    mt_pass: mt_pass
    broker_login: broker_login
    broker_pass: broker_pass
    
    BoxLayout:
        orientation: 'vertical'
        padding: 30
        spacing: 15
        
        Label:
            text: 'Configuração de Logins'
            size_hint_y: 0.1
            font_size: '24sp'
        
        Label:
            text: 'MetaTrader / Plataforma de Trading'
            size_hint_y: 0.05
            halign: 'left'
            text_size: self.size
        TextInput:
            id: mt_login
            hint_text: 'Login MT'
            size_hint_y: 0.1
        TextInput:
            id: mt_pass
            hint_text: 'Senha MT'
            password: True
            size_hint_y: 0.1
            
        Label:
            text: 'Corretora / Broker'
            size_hint_y: 0.05
            halign: 'left'
            text_size: self.size
        TextInput:
            id: broker_login
            hint_text: 'Login Corretora'
            size_hint_y: 0.1
        TextInput:
            id: broker_pass
            hint_text: 'Senha Corretora'
            password: True
            size_hint_y: 0.1
            
        Button:
            text: 'SALVAR E VOLTAR'
            size_hint_y: 0.1
            on_release: root.save_logins()
            
        Button:
            text: 'CANCELAR'
            size_hint_y: 0.05
            on_release: app.root.current = 'main'

<ConfigScreen>:
    dry_run_input: dry_run_input
    bankroll_input: bankroll_input
    
    BoxLayout:
        orientation: 'vertical'
        padding: 30
        spacing: 15
        
        Label:
            text: 'Configurações do Sistema'
            size_hint_y: 0.1
            font_size: '24sp'
        
        Label:
            text: 'Modo DRY_RUN (True/False)'
            size_hint_y: 0.05
            halign: 'left'
            text_size: self.size
        TextInput:
            id: dry_run_input
            hint_text: 'True ou False'
            size_hint_y: 0.1
            
        Label:
            text: 'BANKROLL Inicial (R$)'
            size_hint_y: 0.05
            halign: 'left'
            text_size: self.size
        TextInput:
            id: bankroll_input
            hint_text: 'Ex: 1000.0'
            input_type: 'number'
            size_hint_y: 0.1
            
        Button:
            text: 'SALVAR E VOLTAR'
            size_hint_y: 0.1
            on_release: root.save_config()
            
        Button:
            text: 'CANCELAR'
            size_hint_y: 0.05
            on_release: app.root.current = 'main'
"""

# Carregar o KV Code
from kivy.lang import Builder
Builder.load_string(kv_code)

if __name__ == '__main__':
    # Iniciar o logger antes de tudo
    log_startup("UI", ["Kivy", "Backend"])
    
    try:
        AssistenteApp().run()
    except Exception as e:
        logger.exception(f"Erro fatal na aplicação Kivy: {e}")
    finally:
        log_shutdown()
