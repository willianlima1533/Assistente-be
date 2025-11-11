# 📱 Assistente-be Desktop UI (Kivy)

Esta é a interface gráfica (UI) do Assistente-be, desenvolvida em Kivy para simular um painel de controle estilo iPhone.

## ✨ Funcionalidades

- **Controle de Sistema:** Botão INICIAR/PARAR que controla o loop principal do `main.py` em uma thread separada.
- **Visualização de Status:** Exibe o status atual do sistema e o saldo do Bankroll (lido do `state.json`).
- **Configurações:** Telas para simular a edição de credenciais de login e parâmetros do sistema (`DRY_RUN`, `BANKROLL_INITIAL`).

## 🚀 Como Executar a UI

### Pré-requisitos

1.  **Python 3.11+** instalado.
2.  **Ambiente Virtual** configurado (o script `start_assistente.ps1` faz isso).
3.  **Kivy** instalado.

### 1. Instalar Kivy (Se ainda não o fez)

Se você usou o `start_assistente.ps1`, o Kivy pode não ter sido instalado automaticamente.

**No PowerShell (Windows):**

```powershell
# Ativar o ambiente virtual
.\venv\Scripts\Activate.ps1

# Instalar Kivy
pip install kivy
```

**No Linux/macOS:**

```bash
# Ativar o ambiente virtual
source venv/bin/activate

# Instalar Kivy
pip install kivy
```

### 2. Executar a Aplicação

Com o ambiente virtual ativado, execute o script de inicialização da UI:

```bash
python ui/run_ui.py
```

Uma janela desktop será aberta, simulando um iPhone.

### 3. Usando a UI

1.  **Status:** A tela principal mostra o saldo atual (lido do `state.json`) e o status do sistema.
2.  **INICIAR/PARAR:** Clique no botão **INICIAR** para começar o loop de análise e simulação do backend. O status e o saldo serão atualizados a cada 5 segundos.
3.  **CONFIGURAÇÕES:** Use o botão **CONFIGURAÇÕES** para simular a edição dos parâmetros `DRY_RUN` e `BANKROLL_INITIAL` no arquivo `config.py`.
4.  **LOGINS:** Use o botão **LOGINS** para simular a entrada de credenciais (MetaTrader e Corretora).

**Nota:** A simulação 3D/4D do iPhone é um *placeholder* (espaço reservado) no código. A implementação completa de renderização 3D exigiria um modelo 3D (`.obj`) e mais código Kivy, o que pode ser feito em uma próxima iteração.

---

## 📝 Estrutura da UI

- **`ui/app.py`**: Contém a lógica principal da aplicação Kivy, o gerenciamento de estado (`UIState`), as telas (`MainScreen`, `LoginScreen`, `ConfigScreen`) e o código KV (layout).
- **`ui/run_ui.py`**: Script simples para iniciar a aplicação.
- **`ui/__init__.py`**: Arquivo de inicialização do pacote.
