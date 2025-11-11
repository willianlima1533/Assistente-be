# ============================================================================
# Assistente-be - Script de Inicialização para Windows PowerShell
# ============================================================================
# Este script automatiza a configuração e inicialização do Assistente-be
# no Windows usando PowerShell.
#
# Uso: .\start_assistente.ps1
# ============================================================================

# Configurar política de execução para o processo atual
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# Cores para output
function Write-ColorOutput {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# Banner
Clear-Host
Write-ColorOutput "============================================================================" "Cyan"
Write-ColorOutput "                  🤖 ASSISTENTE-BE v3.0.0                                  " "Cyan"
Write-ColorOutput "              Sistema de Trading e Apostas Inteligente                     " "Cyan"
Write-ColorOutput "============================================================================" "Cyan"
Write-Host ""

# Verificar Python
Write-ColorOutput "🔍 Verificando instalação do Python..." "Yellow"
try {
    $pythonVersion = python --version 2>&1
    Write-ColorOutput "✅ Python encontrado: $pythonVersion" "Green"
} catch {
    Write-ColorOutput "❌ Python não encontrado!" "Red"
    Write-ColorOutput "Por favor, instale Python 3.11+ de https://www.python.org/downloads/" "Red"
    Write-ColorOutput "Certifique-se de marcar 'Add Python to PATH' durante a instalação." "Yellow"
    pause
    exit 1
}

# Verificar se Python é 3.11+
$pythonVersionNumber = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
if ([version]$pythonVersionNumber -lt [version]"3.11") {
    Write-ColorOutput "⚠️  Versão do Python ($pythonVersionNumber) é inferior a 3.11" "Yellow"
    Write-ColorOutput "Recomendamos atualizar para Python 3.11 ou 3.12" "Yellow"
    Write-Host ""
}

# Criar ambiente virtual
Write-ColorOutput "📦 Configurando ambiente virtual..." "Yellow"
if (Test-Path "venv") {
    Write-ColorOutput "✅ Ambiente virtual já existe" "Green"
} else {
    Write-ColorOutput "🔨 Criando ambiente virtual..." "Yellow"
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-ColorOutput "✅ Ambiente virtual criado com sucesso" "Green"
    } else {
        Write-ColorOutput "❌ Erro ao criar ambiente virtual" "Red"
        pause
        exit 1
    }
}

# Ativar ambiente virtual
Write-ColorOutput "🔌 Ativando ambiente virtual..." "Yellow"
& .\venv\Scripts\Activate.ps1

if ($LASTEXITCODE -eq 0) {
    Write-ColorOutput "✅ Ambiente virtual ativado" "Green"
} else {
    Write-ColorOutput "⚠️  Não foi possível ativar o ambiente virtual automaticamente" "Yellow"
    Write-ColorOutput "Execute manualmente: .\venv\Scripts\Activate.ps1" "Yellow"
}

# Atualizar pip
Write-ColorOutput "⬆️  Atualizando pip..." "Yellow"
python -m pip install --upgrade pip --quiet
Write-ColorOutput "✅ pip atualizado" "Green"

# Instalar dependências
Write-ColorOutput "📚 Instalando dependências..." "Yellow"
Write-ColorOutput "Isso pode levar alguns minutos na primeira vez..." "Cyan"
pip install -r requirements.txt --quiet

if ($LASTEXITCODE -eq 0) {
    Write-ColorOutput "✅ Dependências instaladas com sucesso" "Green"
} else {
    Write-ColorOutput "⚠️  Algumas dependências podem ter falhado" "Yellow"
    Write-ColorOutput "Verifique os erros acima e tente instalar manualmente se necessário" "Yellow"
}

# Verificar arquivo .env
Write-Host ""
Write-ColorOutput "🔧 Verificando configuração..." "Yellow"
if (Test-Path ".env") {
    Write-ColorOutput "✅ Arquivo .env encontrado" "Green"
} else {
    Write-ColorOutput "⚠️  Arquivo .env não encontrado" "Yellow"
    if (Test-Path ".env.example") {
        Write-ColorOutput "📋 Copiando .env.example para .env..." "Yellow"
        Copy-Item ".env.example" ".env"
        Write-ColorOutput "✅ Arquivo .env criado" "Green"
        Write-ColorOutput "⚠️  IMPORTANTE: Edite o arquivo .env com suas configurações!" "Yellow"
    }
}

# Criar diretórios necessários
Write-ColorOutput "📁 Criando diretórios necessários..." "Yellow"
$directories = @("logs", "results", "assets/data")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-ColorOutput "  ✅ Criado: $dir" "Green"
    }
}

# Informações finais
Write-Host ""
Write-ColorOutput "============================================================================" "Cyan"
Write-ColorOutput "                          🚀 PRONTO PARA INICIAR!                          " "Green"
Write-ColorOutput "============================================================================" "Cyan"
Write-Host ""
Write-ColorOutput "📖 Comandos disponíveis:" "Yellow"
Write-Host ""
Write-ColorOutput "  • Modo teste (recomendado):" "White"
Write-ColorOutput "    python main.py --dry-run" "Cyan"
Write-Host ""
Write-ColorOutput "  • Modo teste com intervalo personalizado:" "White"
Write-ColorOutput "    python main.py --dry-run --interval 60" "Cyan"
Write-Host ""
Write-ColorOutput "  • Ver ajuda:" "White"
Write-ColorOutput "    python main.py --help" "Cyan"
Write-Host ""
Write-ColorOutput "  • Ver versão:" "White"
Write-ColorOutput "    python main.py --version" "Cyan"
Write-Host ""
Write-ColorOutput "============================================================================" "Cyan"
Write-Host ""

# Perguntar se deseja iniciar
$response = Read-Host "Deseja iniciar o Assistente-be agora? (S/N)"
if ($response -eq "S" -or $response -eq "s") {
    Write-Host ""
    Write-ColorOutput "🚀 Iniciando Assistente-be em modo DRY_RUN..." "Green"
    Write-ColorOutput "Pressione Ctrl+C para parar" "Yellow"
    Write-Host ""
    Start-Sleep -Seconds 2
    python main.py --dry-run
} else {
    Write-Host ""
    Write-ColorOutput "✅ Ambiente configurado!" "Green"
    Write-ColorOutput "Execute 'python main.py --dry-run' quando estiver pronto." "Cyan"
    Write-Host ""
}

# Manter janela aberta
Write-Host ""
Write-ColorOutput "Pressione qualquer tecla para sair..." "Gray"
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
