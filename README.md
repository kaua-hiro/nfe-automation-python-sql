# ðŸ¤– RobÃ´ NFe - IntegraÃ§Ã£o EmpresaConfidencial Ã— Qive

AutomaÃ§Ã£o Python para manifestaÃ§Ã£o inteligente de notas fiscais eletrÃ´nicas via API Qive (Arquivei), com validaÃ§Ã£o cruzada no ERP da EmpresaConfidencial Brasil.

---

## ðŸ“‹ Sobre o Projeto

Sistema automatizado que gerencia o ciclo de vida das NFe recebidas, aplicando regras fiscais da Receita Federal e sincronizando com o recebimento fÃ­sico de mercadorias. Elimina manifestaÃ§Ãµes manuais e garante conformidade tributÃ¡ria.

### Problema Resolvido
- **Antes:** ManifestaÃ§Ã£o manual de centenas de notas diÃ¡rias
- **Depois:** Processo 100% automatizado com validaÃ§Ã£o de recebimento

---

## âœ¨ Funcionalidades

| Recurso | DescriÃ§Ã£o |
|---------|-----------|
| ðŸ”„ **SincronizaÃ§Ã£o AutomÃ¡tica** | Busca notas via API Qive com paginaÃ§Ã£o cursor-based |
| ðŸ“„ **Parser XML Nativo** | ExtraÃ§Ã£o de datas de autorizaÃ§Ã£o direto do XML da SEFAZ |
| ðŸ—„ï¸ **ValidaÃ§Ã£o ERP** | Consulta em tempo real na tabela `ENTRADAS` do SQL Server |
| â° **Agendamento Inteligente** | ExecuÃ§Ã£o diÃ¡ria Ã s 08:00 com retry automÃ¡tico |
| ðŸ“Š **RelatÃ³rios Discord** | NotificaÃ§Ãµes coloridas com mÃ©tricas executivas |

---

## ðŸ§  Motor de Regras Fiscais

O sistema aplica uma lÃ³gica de trÃªs camadas antes de qualquer manifestaÃ§Ã£o:

### 1ï¸âƒ£ Filtro de Prazo Legal
```
Nota com > 180 dias desde emissÃ£o â†’ DESCARTADA
```
*Fundamento: Prazo decadencial da Receita Federal*

### 2ï¸âƒ£ ConfirmaÃ§Ã£o de OperaÃ§Ã£o
```
Nota encontrada no SQL Server â†’ ManifestaÃ§Ã£o 210200 (ConfirmaÃ§Ã£o)
```
*Valida recebimento fÃ­sico da mercadoria*

### 3ï¸âƒ£ CiÃªncia EstratÃ©gica
```
â”Œâ”€ Nota NÃƒO recebida + < 10 dias â†’ ManifestaÃ§Ã£o 210210 (CiÃªncia)
â””â”€ Nota NÃƒO recebida + 11~180 dias â†’ AGUARDA (Evita ciÃªncia prematura)
```

**Diagrama de Fluxo:**
```
NFe Recebida
    â”‚
    â”œâ”€> EmissÃ£o > 180 dias? â”€â”€[SIM]â”€â”€> âŒ IGNORAR
    â”‚
    â”œâ”€> Existe no SQL? â”€â”€[SIM]â”€â”€> âœ… CONFIRMAR (210200)
    â”‚
    â””â”€> EmissÃ£o < 10 dias? â”€â”€[SIM]â”€â”€> ðŸ”” CIÃŠNCIA (210210)
                           â””â”€[NÃƒO]â”€â”€> â¸ï¸ AGUARDAR
```

---

## ðŸ—ï¸ Arquitetura (MVC)
```
EmpresaConfidencial_INTEGRACAO_QIVE/
â”‚
â”œâ”€â”€ ðŸ“‚ src/
â”‚   â”œâ”€â”€ config/        â†’ Gerenciador de variÃ¡veis (.env + validaÃ§Ãµes)
â”‚   â”œâ”€â”€ controllers/   â†’ LÃ³gica de negÃ³cio (regras 10/180 dias)
â”‚   â”œâ”€â”€ models/        â†’ Camada de dados (queries SQL Server)
â”‚   â”œâ”€â”€ services/      â†’ IntegraÃ§Ãµes externas (API Qive + XML parser)
â”‚   â””â”€â”€ views/         â†’ Camada de apresentaÃ§Ã£o (logs + webhooks)
â”‚
â”œâ”€â”€ ðŸš€ run.py          â†’ Entrypoint + scheduler
â”œâ”€â”€ ðŸ“ .env.example    â†’ Template de configuraÃ§Ã£o
â””â”€â”€ ðŸ“– README.md
```

### Fluxo de Dados
```
API Qive â†’ services/qive_client.py â†’ controllers/nfe_processor.py 
    â†“                                          â†“
XML Parser                            models/database.py (SQL)
    â†“                                          â†“
controllers/manifest_rules.py â†’ services/qive_client.py (POST)
    â†“
views/discord_webhook.py (RelatÃ³rio)
```

---

## âš™ï¸ InstalaÃ§Ã£o

### PrÃ©-requisitos
- Python 3.8+
- SQL Server com tabela `ENTRADAS`
- Credenciais Qive (API Key)
- Webhook Discord (opcional)

### Passo a Passo

**1. Clone o repositÃ³rio**
```bash
git clone https://github.com/EmpresaConfidencial-Brasil/EmpresaConfidencial-integracao-qive.git
cd EmpresaConfidencial-integracao-qive
```

**2. Instale as dependÃªncias**
```bash
pip install -r requirements.txt
```

**3. Configure o ambiente**
```bash
cp .env.example .env
nano .env  # Edite com suas credenciais
```

**VariÃ¡veis obrigatÃ³rias no `.env`:**
```ini
# Banco de Dados
DB_SERVER=seu-servidor.database.windows.net
DB_NAME=EmpresaConfidencialBrasil
DB_USER=robot_nfe
DB_PASSWORD=SenhaSegura123!

# API Qive
QIVE_API_KEY=qive_live_abc123xyz789

# Webhooks (Opcional)
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...

# Modo de OperaÃ§Ã£o
MODO_SIMULACAO=True  # False para produÃ§Ã£o (envia para SEFAZ)
```

**4. Teste a conexÃ£o**
```bash
python -c "from src.models.database import testar_conexao; testar_conexao()"
```

**5. Execute o robÃ´**
```bash
python run.py
```

---

## ðŸŽ¯ Uso

### ExecuÃ§Ã£o Manual
```bash
python run.py --force  # Executa imediatamente (ignora agendamento)
```

### Modo SimulaÃ§Ã£o
```bash
# No .env, configure:
MODO_SIMULACAO=True
```
- âœ… Processa todas as notas
- âœ… Valida regras fiscais
- âŒ **NÃƒO envia** manifestaÃ§Ãµes para SEFAZ
- ðŸ“Š Gera relatÃ³rio completo no Discord

### Modo ProduÃ§Ã£o
```bash
MODO_SIMULACAO=False
```
- âš ï¸ **ATENÃ‡ÃƒO:** Envia eventos reais para Receita Federal

---

## ðŸ“Š Monitoramento

### Logs Locais
```bash
tail -f logs/nfe_robot.log
```

### Dashboard Discord
O robÃ´ envia cards interativos com:
- ðŸŸ¢ Notas confirmadas (210200)
- ðŸ”µ Notas com ciÃªncia (210210)
- ðŸŸ¡ Notas aguardando recebimento
- ðŸ”´ Erros e exceÃ§Ãµes

**Exemplo de RelatÃ³rio:**
```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ ðŸ¤– ROBÃ” NFe - Resumo DiÃ¡rio         â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ âœ… Confirmadas: 127 notas           â”‚
â”‚ ðŸ”” CiÃªncias:     43 notas           â”‚
â”‚ â¸ï¸  Aguardando:   18 notas           â”‚
â”‚ âŒ Erros:         2 notas           â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ â±ï¸ Tempo: 4m 32s                    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## ðŸ”§ ManutenÃ§Ã£o

### Atualizar Regras Fiscais
Edite: `src/controllers/manifest_rules.py`
```python
PRAZO_CIENCIA_DIAS = 10      # Ajustar conforme polÃ­tica interna
PRAZO_MAXIMO_DIAS = 180      # Limite legal da Receita
```

### Adicionar Novos Eventos
1. Consulte [documentaÃ§Ã£o Qive](https://docs.qive.com.br)
2. Adicione cÃ³digo em `src/services/qive_client.py`

---

## ðŸ¤ Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanÃ§as (`git commit -m 'Adiciona validaÃ§Ã£o de CFOP'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## ðŸ“œ LicenÃ§a

Propriedade da **EmpresaConfidencial Brasil** - Uso interno exclusivo.

---

## ðŸ‘¨â€ðŸ’» Desenvolvedor

**KauÃ£ Hiro**  
AutomaÃ§Ã£o & IntegraÃ§Ãµes Fiscais  
EmpresaConfidencial Brasil - 2026

---

## ðŸ†˜ Suporte

**Em caso de erros:**
1. Verifique os logs: `logs/nfe_robot.log`
2. Teste a conexÃ£o SQL: `python -c "from src.models.database import testar_conexao; testar_conexao()"`
3. Valide a API Key Qive no [painel administrativo](https://app.qive.com.br)

---

<div align="center">

**[â¬† Voltar ao topo](#-robÃ´-nfe---integraÃ§Ã£o-EmpresaConfidencial--qive)**

</div>
