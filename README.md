# BE-Termux (Simulador de Apostas + Assistente JARVIS-like)

**Descrição:** Projeto modular em Python para rodar no Termux (Android). Combina um simulador
educativo de apostas esportivas (EstrelaBet - simulação via API / scraping ético) com um assistente
JARVIS-like (BE) que traz escuta por voz, análises, coaching e automações seguras via intents.

**Aviso importante:** Este projeto é **apenas para fins educacionais e de simulação**. **NÃO** automatize
logins ou apostas reais sem autorização explícita do site e sem observar os Termos de Serviço. Apostas reais
podem causar perdas financeiras e vício. Use o modo `DRY_RUN` para testes.

## Estrutura do projeto
- config.py           -> chaves, credenciais mockadas e parâmetros principais
- analyzer.py         -> coleta de odds / dados (API-Football exemplo) + modelo simples
- bet_engine.py       -> gera múltiplas "humanas" e aplica filtros de value bet
- manager.py          -> gerencia bankroll, simula apostas e grava histórico (CSV/JSON)
- utils.py            -> funções auxiliares (login simulado, notificações via termux)
- main.py             -> loop principal com agendamento 24/7 (schedule)
- voice.py            -> reconhecimento de voz (modo básico)
- setup.sh            -> script de instalação para Termux (pkg + pip install)
- requirements.txt    -> dependências Python recomendadas
- run.sh              -> script para iniciar em screen/tmux
- data/fixtures_sample.csv -> amostra de partidas para testes offline
- results/            -> saída de logs e relatórios (gerado em runtime)

## Como usar (resumo)
1. No Termux execute:
   ```bash
   bash setup.sh
   ```
   (verifique o conteúdo do script antes de rodar)

2. Configure `config.py` (adicione sua chave de API-Football se quiser usar dados reais).

3. Teste em modo dry-run (sem apostas reais):
   ```bash
   python main.py --dry-run
   ```

4. Para rodar em background (ex.: screen/tmux):
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

## Notas sobre APIs
- API sugerida para dados reais: https://www.api-football.com/ (free tier disponível).
- Se você usar scraping de sites como EstrelaBet, respeite `robots.txt` e os Termos de Serviço — prefira APIs.

## Segurança / Ética
- Nunca armazene senhas reais em texto plano. Este projeto usa credenciais mockadas apenas para simulação.
- Não automatize apostas reais sem permissão. Automação de login/execução de apostas pode violar ToS.
- Use o modo `DRY_RUN` sempre ao testar.

## Licença
Uso pessoal e educativo. Adaptar por sua conta e risco.
