# 🤖 Automação de Manifestação e Gestão de NFe (RPA)

> **Nota:** Este repositório contém a documentação e a arquitetura de um projeto real desenvolvido em ambiente corporativo. Por questões de propriedade intelectual e segurança, o código-fonte completo não está disponível publicamente, mas a lógica e estrutura estão detalhadas abaixo.

## 📌 Sobre o Projeto
Robô autônomo desenvolvido em **Python** para automatizar o ciclo de vida de Notas Fiscais Eletrônicas (NFe). O sistema integra a API de um fornecedor de dados fiscais (Qive/Arquivei) diretamente com o Banco de Dados (SQL Server) do ERP da empresa.

O objetivo foi eliminar o processo manual de conferência, garantir conformidade fiscal (compliance) e notificar a equipe em tempo real sobre pendências.

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.12
* **Banco de Dados:** SQL Server (Azure/Local)
* **Integração:** API RESTful (Requests)
* **Bibliotecas Chave:** `pyodbc` (Conexão SQL), `requests`, `python-dotenv`, `logging`.
* **DevOps:** Git Flow, Windows Task Scheduler, Discord Webhooks.

## ⚙️ Arquitetura da Solução

O projeto segue o padrão MVC (Model-View-Controller) adaptado para scripts de automação:

1.  **Extract (Extração):** O robô consulta a API de terceiros buscando apenas notas novas (lógica incremental).
2.  **Transform (Transformação):** Valida status, prazos de ciência e confirmação (Prazos Legais SEFAZ).
3.  **Load (Carga):** Insere ou atualiza os registros no SQL Server para leitura do ERP.
4.  **Alerting:** Envia relatório de execução (Sucessos/Falhas) para um canal no Discord.

### 🧠 Destaques Técnicos (Desafios Resolvidos)
* **Lógica Delta:** O robô não processa tudo todo dia. Ele compara o que tem no banco vs. o que tem na API e processa apenas a diferença (Delta), economizando requisições e processamento.
* **Logger Rotativo:** Implementação de logs que se renovam a cada 7 dias para evitar consumo excessivo de disco.
* **Resiliência:** Tratamento de erros de rede (Timeouts) e reconexão automática com o banco.
* **Modo Debug:** Ferramentas internas CLI para consultar o status real de uma nota específica sem alterar o banco de dados.

## 📁 Estrutura do Projeto (Visualização)

```text
├── src/
│   ├── controllers/   # Lógica de controle de fluxo
│   ├── models/        # Comandos SQL e conexão com Banco
│   └── services/      # Comunicação com a API Externa
├── tools/             # Scripts de Debug e Testes Manuais
├── logs/              # Arquivos de log rotativos
├── .env.example       # Modelo de variáveis de ambiente
├── run.py             # Ponto de entrada (Entrypoint)
└── requirements.txt   # Dependências

Desenvolvido por Kauã Hiro