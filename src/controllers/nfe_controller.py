import datetime
from src.models.database import DatabaseModel
from src.services.qive_api import QiveAPI

class NfeController:
    def __init__(self):
        self.db = DatabaseModel()
        self.api = QiveAPI()

    def processar_ciclo(self):
        print("[CICLO] Buscando notas na Qive...")
        notas = self.api.listar_notas(limit=50)
        if not notas: return

        print(f"[CICLO] Analisando {len(notas)} notas...")

        for nota in notas:
            try:
                chave = nota.get('access_key')
                if not chave: continue

                try:
                    ano_nota = int("20" + chave[2:4])
                except: continue

                if ano_nota < 2025: continue

                print(f"   🔎 Processando: {chave}")

                dados_banco = self.db.buscar_nota_por_chave(chave)
                status_atual = str(dados_banco[2]) if dados_banco and dados_banco[2] else None
                
                if not dados_banco:
                    self.db.gravar_empresa_na_nota(chave, "PENDENTE")

                devo_confirmar = False
                if status_atual in ['210210', '210240', None, 'None', 'PENDENTE']:
                    devo_confirmar = True
                elif status_atual in ['210200', '210220']:
                    devo_confirmar = False

                if devo_confirmar:
                    codigo_sefaz = self.api.manifestar_nota(chave)
                    
                    if codigo_sefaz == 135:
                        print("      ✅ Sucesso (135)! Confirmada.")
                        self.db.registrar_confirmacao_banco(chave, '210200')
                    
                    elif codigo_sefaz == 596:
                        print("      ⛔ Prazo Perdido (596). Marcando como Desconhecido.")
                        self.db.registrar_confirmacao_banco(chave, '210220')
                    
                    elif codigo_sefaz:
                        print(f"      ⚠️ Retorno SEFAZ incomum: {codigo_sefaz}")
                    
            except Exception as e:
                print(f"[ERRO] {e}")

    def processar_rede_seguranca(self):
        pass