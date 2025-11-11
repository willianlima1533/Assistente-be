# 🤖 Assistente-be - Sistema de Trading e Apostas Inteligente

[![CI](https://github.com/willianlima1533/Assistente-be/workflows/CI/badge.svg)](https://github.com/willianlima1533/Assistente-be/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Educational-green.svg)](LICENSE)

**Sistema modular em Python para simulação educativa de apostas esportivas e trading automatizado.** Combina análise de dados, machine learning e automação segura para criar um assistente inteligente que opera 24/7.

## ⚠️ Aviso Importante

Este projeto é **exclusivamente para fins educacionais e de simulação**. **NÃO** automatize logins ou apostas reais sem autorização explícita do site e sem observar os Termos de Serviço. Apostas reais podem causar perdas financeiras e vício. **Use sempre o modo `DRY_RUN` para testes.**

## ✨ Características

- 🎲 **Simulador de Apostas Esportivas** - Análise de odds e geração de múltiplas inteligentes
- 💹 **Trading Automatizado** - Estratégias de trading com análise técnica
- 🧠 **Auto-Evolução** - Sistema de aprendizado contínuo baseado em resultados
- 🎯 **Coaching Pessoal** - Mentoria virtual inspirada em bilionários
- 🎰 **Loteria com IA** - Geração de jogos usando padrões estatísticos
- 📊 **Gestão de Bankroll** - Controle rigoroso de capital e stakes
- 🔐 **Logging Inteligente** - Sistema completo de logs com loguru
- 🚀 **CI/CD Automatizado** - Workflows GitHub Actions para testes e releases

## 📁 Estrutura do Projeto

```
Assistente-be/
├── .github/
│   └── workflows/          # GitHub Actions (CI/CD, Security, Docs)
├── assets/
│   └── data/              # Dados de fixtures e análises
├── trader/                # Módulos de trading e apostas
│   ├── analyzer.py        # Análise de odds e probabilidades
│   ├── bet_engine.py      # Geração de apostas inteligentes
│   └── manager.py         # Gestão de bankroll
├── tools/                 # Ferramentas auxiliares
│   ├── logger.py          # Sistema de logging
│   ├── utils.py           # Funções utilitárias
│   └── voice.py           # Reconhecimento de voz
├── logs/                  # Logs do sistema (gerado em runtime)
├── results/               # Resultados e histórico (gerado em runtime)
├── tests/                 # Testes automatizados
├── config.py              # Configurações principais
├── main.py                # Loop principal do sistema
├── requirements.txt       # Dependências Python
├── Pipfile                # Gerenciamento com Pipenv
├── .env.example           # Exemplo de variáveis de ambiente
└── start_assistente.ps1   # Script de inicialização para Windows
```

## 🚀 Instalação

### Windows (PowerShell)

```powershell
# 1. Clone o repositório
git clone https://github.com/willianlima1533/Assistente-be.git
cd Assistente-be

# 2. Execute o script de inicialização
.\start_assistente.ps1
```

O script `start_assistente.ps1` irá:
- Criar ambiente virtual Python
- Instalar todas as dependências
- Iniciar o sistema automaticamente

### Linux / macOS

```bash
# 1. Clone o repositório
git clone https://github.com/willianlima1533/Assistente-be.git
cd Assistente-be

# 2. Crie e ative o ambiente virtual
python3.12 -m venv venv
source venv/bin/activate  # No macOS/Linux

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o sistema
python main.py --dry-run
```

### Termux (Android)

```bash
# 1. Instale dependências do sistema
pkg update && pkg upgrade
pkg install python git

# 2. Clone o repositório
git clone https://github.com/willianlima1533/Assistente-be.git
cd Assistente-be

# 3. Instale dependências Python
pip install -r requirements.txt

# 4. Configure permissões (opcional, para notificações)
pkg install termux-api

# 5. Execute o sistema
python main.py --dry-run --interval 60
```

### Replit

1. Acesse [Replit](https://replit.com) e faça login
2. Clique em **"Create Repl"**
3. Selecione **"Import from GitHub"**
4. Cole a URL: `https://github.com/willianlima1533/Assistente-be`
5. Clique em **"Import from GitHub"**
6. No Shell do Replit, execute:

```bash
pip install -r requirements.txt
python main.py --dry-run
```

## ⚙️ Configuração

### 1. Copie o arquivo de exemplo de ambiente

```bash
cp .env.example .env
```

### 2. Edite o arquivo `.env` com suas configurações

```bash
# Modo de operação
DRY_RUN=True          # True = teste, False = simulação
DEBUG=True

# Bankroll inicial
BANKROLL_INITIAL=1000.0
MIN_STAKE_PERCENT=0.01
MAX_STAKE_PERCENT=0.02

# API Keys (opcional)
API_FOOTBALL_KEY=sua_chave_aqui
```

### 3. Configure `config.py` conforme necessário

```python
DRY_RUN = True  # Sempre True para testes
BANKROLL_INITIAL = 1000.0
API_FOOTBALL_KEY = ''  # Sua chave da API-Football (opcional)
```

## 📖 Uso

### Modo Básico (Dry Run)

```bash
python main.py --dry-run
```

### Modo com Intervalo Personalizado

```bash
python main.py --dry-run --interval 60  # Executa a cada 60 minutos
```

### Modo Background (Linux/macOS)

```bash
# Usando screen
screen -S assistente
python main.py --dry-run
# Pressione Ctrl+A, depois D para desanexar

# Para retornar à sessão
screen -r assistente
```

### Modo Background (Termux)

```bash
# Usando termux-wake-lock para evitar suspensão
termux-wake-lock
python main.py --dry-run --interval 30

# Para liberar
termux-wake-unlock
```

## 🔧 Comandos Úteis

### Verificar Logs

```bash
# Logs gerais
tail -f logs/assistente_$(date +%Y-%m-%d).log

# Logs de erros
tail -f logs/errors_$(date +%Y-%m-%d).log

# Logs de trading
tail -f logs/trading_$(date +%Y-%m-%d).log
```

### Verificar Histórico de Apostas

```bash
cat results/history.csv
```

### Verificar Estado Atual

```bash
cat state.json
```

### Executar Testes

```bash
pytest tests/ -v
```

## 📊 APIs Recomendadas

### API-Football (Dados de Futebol)

- **URL**: https://www.api-football.com/
- **Free Tier**: 100 requisições/dia
- **Uso**: Obter odds e fixtures em tempo real

### Outras APIs Úteis

- **The Odds API**: https://the-odds-api.com/
- **Football-Data.org**: https://www.football-data.org/

## 🛡️ Segurança e Ética

### ✅ Boas Práticas

- ✅ Use sempre o modo `DRY_RUN` para testes
- ✅ Nunca armazene senhas reais em texto plano
- ✅ Use variáveis de ambiente para credenciais
- ✅ Respeite os Termos de Serviço dos sites
- ✅ Respeite `robots.txt` ao fazer scraping
- ✅ Prefira APIs oficiais ao invés de scraping

### ❌ Não Faça

- ❌ Automatizar apostas reais sem permissão
- ❌ Violar Termos de Serviço de plataformas
- ❌ Usar o sistema para atividades ilegais
- ❌ Compartilhar credenciais ou API keys
- ❌ Executar em produção sem testes adequados

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📝 Changelog

### v3.0.0 (2025-11-11)

- ✨ Reestruturação completa do projeto
- ✨ Sistema de logging inteligente com loguru
- ✨ Workflows GitHub Actions (CI/CD, Security, Docs)
- ✨ Suporte para Python 3.12
- ✨ Organização modular (trader, tools, assets)
- ✨ Script PowerShell para Windows
- ✨ Documentação completa para múltiplas plataformas
- 🐛 Correção de imports e paths
- 🐛 Correção de sintaxe em módulos

### v2.0.0 (2025-10-09)

- ✨ Sistema BE Ultimate integrado
- ✨ Módulos de trading, IQ Option, loteria
- ✨ Sistema de coaching e auto-evolução

### v1.0.0 (2025-10-01)

- 🎉 Versão inicial
- 🎲 Simulador de apostas esportivas
- 📊 Gestão de bankroll

## 📄 Licença

Este projeto é destinado **exclusivamente para uso pessoal e educativo**. Adapte e use por sua conta e risco. O autor não se responsabiliza por perdas financeiras ou uso inadequado do sistema.

## 👤 Autor

**Willian Lima**

- GitHub: [@willianlima1533](https://github.com/willianlima1533)
- Repositório: [Assistente-be](https://github.com/willianlima1533/Assistente-be)

## 🙏 Agradecimentos

- Comunidade Python
- Desenvolvedores das bibliotecas utilizadas
- Contribuidores do projeto

---

**⚠️ Lembre-se: Este é um projeto educacional. Use com responsabilidade e sempre em modo de simulação!**
