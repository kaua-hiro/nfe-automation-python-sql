import os
from dotenv import load_dotenv
from src.services.qive_api import QiveAPI
from src.models.database import DatabaseModel
from src.services.discord_service import DiscordService
from src.utils.logger import setup_logger 

load_dotenv()

logger = setup_logger()

def main():
    logger.info("🚀 --- INICIANDO EXECUÇÃO DO ROBÔ ---")

    try:
        db = DatabaseModel()
        api = QiveAPI()
        discord = DiscordService()
    except Exception as e:
        logger.error(f"❌ Erro fatal ao iniciar serviços: {e}")
        return

    try:
        notas = db.buscar_notas_pendentes()
        total_notas = len(notas)
        logger.info(f"📋 Total de notas pendentes (Delta): {total_notas}")
    except Exception as e:
        logger.error(f"❌ Erro ao buscar notas no banco: {e}")
        return

    count_sucesso = 0
    count_ja_ok = 0
    count_prazo = 0
    count_erro_api = 0

    for nota in notas:
        chave = nota[0]
        
        try:
            codigo_retorno = api.manifestar_nota(chave)
            
            if codigo_retorno == 135:
                # SUCESSO
                logger.info(f"✅ SUCESSO (135) | Nota: {chave}")
                db.registrar_confirmacao_banco(chave, '210200')
                count_sucesso += 1
                
            elif codigo_retorno == '210200' or codigo_retorno == 200:
                # JÁ ESTAVA OK
                logger.info(f"⏭️ JA EXISTE (API) | Nota: {chave}")
                db.registrar_confirmacao_banco(chave, '210200')
                count_ja_ok += 1

            elif codigo_retorno == 596:
                # PRAZO PERDIDO
                logger.warning(f"⛔ PRAZO ESTOURADO (596) | Nota: {chave}")
                db.registrar_confirmacao_banco(chave, '210220')
                count_prazo += 1
                
            else:
                # OUTROS ERROS
                logger.error(f"⚠️ ERRO API ({codigo_retorno}) | Nota: {chave}")
                count_erro_api += 1

        except Exception as e:
            logger.error(f"❌ EXCEÇÃO NO LOOP | Nota: {chave} | Erro: {e}")
            count_erro_api += 1

    # 3. Finalização
    logger.info("🏁 Processamento finalizado. Enviando relatório para Discord...")
    
    discord.enviar_relatorio_diario(
        total_processado=total_notas,
        novos_sucessos=count_sucesso,
        ja_estavam_ok=count_ja_ok,
        erros_prazo=count_prazo,
        erros_api=count_erro_api
    )
    
    logger.info("💤 Fim da execução. Até amanhã!")

if __name__ == "__main__":
    main()