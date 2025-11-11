#!/data/data/com.termux/files/usr/bin/bash
# Script de instalação do BE Ultimate para Termux

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║              🧠 BE ULTIMATE - INSTALAÇÃO                    ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Verificar se está no Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo "⚠️  Este script é para Termux no Android"
    exit 1
fi

# Atualizar pacotes
echo "📦 Atualizando pacotes do Termux..."
pkg update -y
pkg upgrade -y

# Instalar Python e dependências do sistema
echo "🐍 Instalando Python e dependências..."
pkg install -y python python-pip git wget curl

# Instalar termux-api
echo "📱 Instalando Termux API..."
pkg install -y termux-api

# Criar diretórios
echo "📁 Criando estrutura de diretórios..."
mkdir -p ~/BE_ULTIMATE/{modules,config,data,logs}

# Instalar dependências Python
echo "📦 Instalando dependências Python..."
pip install --upgrade pip

# Instalar pacotes essenciais
pip install numpy pandas requests python-dotenv flask schedule beautifulsoup4 lxml pillow

# Tentar instalar OpenCV (pode falhar no Android)
echo "🔧 Tentando instalar OpenCV..."
pip install opencv-python 2>/dev/null || echo "⚠️  OpenCV não disponível - funcionalidade limitada"

# Tentar instalar MT5 (não funciona no Android, mas não é crítico)
echo "🔧 Tentando instalar MetaTrader5..."
pip install MetaTrader5 2>/dev/null || echo "⚠️  MT5 não disponível - usando simulação"

# Copiar arquivos (se existirem)
if [ -f "main.py" ]; then
    echo "📋 Copiando arquivos..."
    cp -r . ~/BE_ULTIMATE/
fi

# Tornar executável
chmod +x ~/BE_ULTIMATE/main.py 2>/dev/null || true
chmod +x ~/BE_ULTIMATE/scripts/*.sh 2>/dev/null || true

# Criar arquivo .env
if [ ! -f ~/BE_ULTIMATE/.env ]; then
    echo "⚙️  Criando arquivo de configuração..."
    cat > ~/BE_ULTIMATE/.env << 'ENVEOF'
# BE Ultimate - Configuração

# APIs
API_FOOTBALL_KEY=
NEWS_API_KEY=
ALPHA_VANTAGE_KEY=

# MetaTrader 5 (se disponível)
MT5_LOGIN=
MT5_PASSWORD=
MT5_SERVER=

# Configurações
DRY_RUN=True
VOICE_ENABLED=False
AUTO_EVOLUTION=True
ENVEOF
fi

# Criar script de inicialização
cat > ~/BE_ULTIMATE/start.sh << 'STARTEOF'
#!/data/data/com.termux/files/usr/bin/bash
cd ~/BE_ULTIMATE
python main.py
STARTEOF

chmod +x ~/BE_ULTIMATE/start.sh

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║              ✅ INSTALAÇÃO CONCLUÍDA!                        ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 Para iniciar o BE Ultimate:"
echo "   cd ~/BE_ULTIMATE"
echo "   ./start.sh"
echo ""
echo "⚙️  Configure as chaves de API em:"
echo "   nano ~/BE_ULTIMATE/.env"
echo ""
echo "📖 Documentação completa em:"
echo "   ~/BE_ULTIMATE/docs/README.md"
echo ""

