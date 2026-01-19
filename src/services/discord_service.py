import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class DiscordService:
    def __init__(self):
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    def enviar_relatorio_diario(self, total_processado, novos_sucessos, ja_estavam_ok, erros_prazo, erros_api):

        if not self.webhook_url:
            print("âš ï¸ URL do Discord nÃ£o configurada no .env")
            return

        cor = 0x2ecc71 

        if erros_prazo > 0:
            cor = 0xf1c40f 

        if erros_api > 0:
            cor = 0xe74c3c 

        payload = {
            "username": "EmpresaConfidencial IntegraÃ§Ã£o Qive",
            "avatar_url": "https://cdn-icons-png.flaticon.com/512/2585/2585184.png",
            "embeds": [
                {
                    "title": "ðŸ“Š Resumo DiÃ¡rio: ConfirmaÃ§Ã£o de Notas",
                    "description": f"ExecuÃ§Ã£o finalizada em **{datetime.now().strftime('%d/%m/%Y Ã s %H:%M')}**.",
                    "color": cor,
                    "fields": [
                        {
                            "name": "ðŸ”Ž Total Analisado",
                            "value": f"``` {total_processado} ```",
                            "inline": True
                        },
                        {
                            "name": "âœ… Confirmadas Hoje",
                            "value": f"``` {novos_sucessos} ```",
                            "inline": True
                        },
                        {
                            "name": "â­ï¸ JÃ¡ Confirmadas",
                            "value": f"``` {ja_estavam_ok} ```",
                            "inline": True
                        },
                        {
                            "name": "ðŸ“… Fora do Prazo (Ignoradas)",
                            "value": f"**{erros_prazo}**",
                            "inline": True
                        },
                        {
                            "name": "ðŸ’€ Erros de API",
                            "value": f"**{erros_api}**",
                            "inline": True
                        }
                    ],
                    "footer": {
                        "text": "EmpresaConfidencial Brasil â€¢ AutomaÃ§Ã£o NFe",
                        "icon_url": "https://www.EmpresaConfidencialbrasil.com.br/favicon.ico"
                    }
                }
            ]
        }

        try:
            requests.post(self.webhook_url, json=payload)
            print("ðŸ”” RelatÃ³rio enviado para o Discord com sucesso.")
        except Exception as e:
            print(f"âŒ Erro ao enviar para Discord: {e}")
