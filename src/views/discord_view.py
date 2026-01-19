import requests
from datetime import datetime
from src.config.settings import DISCORD_URL, MODO_SIMULACAO

class DiscordView:
    @staticmethod
    def log(mensagem, tipo="info"):
        print(f"[{tipo.upper()}] {mensagem}")
        
        if not DISCORD_URL: return

        # Cores: Verde(Sucesso), Vermelho(Erro), Azul(Info), Amarelo(Simulação)
        colors = {'info': 3447003, 'erro': 15548997, 'sucesso': 5763719, 'teste': 16776960}
        color = colors.get(tipo, 3447003)

        payload = {
            "embeds": [{
                "title": f"Robô NFe - {'Simulação' if MODO_SIMULACAO and tipo=='teste' else tipo.capitalize()}",
                "description": mensagem,
                "color": color,
                "timestamp": datetime.now().isoformat()
            }]
        }
        try:
            requests.post(DISCORD_URL, json=payload)
        except:
            pass