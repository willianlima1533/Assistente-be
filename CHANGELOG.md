# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [3.0.0] - 2025-11-11

### ✨ Adicionado

- Sistema de logging inteligente com loguru
  - Logs rotativos diários
  - Separação de logs por tipo (geral, erros, trading)
  - Formatação colorida no console
  - Compressão automática de logs antigos
- Workflows GitHub Actions completos
  - CI/CD com testes automatizados
  - Security scanning (Bandit, Safety, CodeQL)
  - Documentação automática
  - Release automation
- Script PowerShell para Windows (`start_assistente.ps1`)
  - Configuração automática de ambiente virtual
  - Instalação de dependências
  - Verificação de requisitos
  - Interface amigável com cores
- Estrutura de diretórios reorganizada
  - `trader/` - Módulos de trading e apostas
  - `tools/` - Ferramentas auxiliares
  - `assets/` - Dados e recursos
  - `logs/` - Logs do sistema
  - `tests/` - Testes automatizados
- Arquivo `.env.example` para configurações
- Arquivo `Pipfile` para gerenciamento com Pipenv
- Arquivo `.gitignore` completo
- Documentação expandida no README.md
  - Instruções para Windows (PowerShell)
  - Instruções para Termux (Android)
  - Instruções para Replit
  - Seção de segurança e ética
  - Comandos úteis
- Diretório `data/` com fixtures de exemplo
- Módulo `__init__.py` para pacotes Python

### 🔧 Modificado

- `main.py` completamente reescrito
  - Integração com sistema de logging
  - Melhor tratamento de erros
  - Argumentos de linha de comando aprimorados
  - Health checks automáticos
  - Shutdown gracioso
- `utils.py` refatorado
  - Uso de loguru ao invés de print()
  - Funções utilitárias adicionais
  - Melhor tratamento de paths
  - Type hints adicionados
- `requirements.txt` atualizado
  - Versões específicas para Python 3.12
  - Novas dependências (loguru, etc.)
  - Dependências de desenvolvimento separadas
- `config.py` mantido compatível
- Imports corrigidos em todos os módulos

### 🐛 Corrigido

- Erro de sintaxe em `coaching.py` (f-string com aspas)
- Paths incorretos em `analyzer.py` (data/fixtures_sample.csv)
- Imports circulares e dependências quebradas
- Falta de diretório `data/` causando erros
- Compatibilidade com Python 3.12

### 🔒 Segurança

- Adicionado scanning de segurança automatizado
- Verificação de dependências vulneráveis
- Análise de código com Bandit
- Secret scanning com TruffleHog
- CodeQL analysis habilitado

### 📚 Documentação

- README.md completamente reescrito
- Instruções detalhadas para múltiplas plataformas
- Seção de segurança e ética expandida
- Exemplos de uso adicionados
- Changelog criado

## [2.0.0] - 2025-10-09

### ✨ Adicionado

- Sistema BE Ultimate integrado
- Módulo de trading financeiro
- Módulo IQ Option
- Sistema de loteria com IA
- Sistema de coaching pessoal
- Auto-evolução com aprendizado de máquina

## [1.0.0] - 2025-10-01

### 🎉 Inicial

- Versão inicial do projeto
- Simulador de apostas esportivas
- Análise de odds básica
- Gestão de bankroll
- Geração de múltiplas
- Integração com API-Football
- Modo DRY_RUN para testes

---

## Tipos de Mudanças

- ✨ **Adicionado** - para novas funcionalidades
- 🔧 **Modificado** - para mudanças em funcionalidades existentes
- 🗑️ **Depreciado** - para funcionalidades que serão removidas
- 🔥 **Removido** - para funcionalidades removidas
- 🐛 **Corrigido** - para correção de bugs
- 🔒 **Segurança** - para vulnerabilidades corrigidas
- 📚 **Documentação** - para mudanças na documentação
