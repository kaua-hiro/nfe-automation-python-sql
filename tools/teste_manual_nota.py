#O que ele faz: Ele simula o Robô Principal (run.py), mas só para uma nota específica.
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.database import DatabaseModel
from src.services.qive_api import QiveAPI

def testar_nota_unica():
    print("\n--- 🧪 TESTE MANUAL COM CÓDIGO SEFAZ (V2.0) ---")
    chave = input("👉 Cole a Chave: ").strip()

    try:
        db = DatabaseModel()
        api = QiveAPI()

        print("[1] Garantindo nota no banco...")
        db.gravar_empresa_na_nota(chave, "TESTE_MANUAL")

        print("[2] Enviando Manifesto...")
        codigo = api.manifestar_nota(chave)

        print(f"\n📡 RETORNO DA SEFAZ: {codigo}")

        if codigo == 135:
            print("✅ SUCESSO! (135 - Evento Registrado)")
            print("   -> Atualizando banco para 210200")
            db.registrar_confirmacao_banco(chave, '210200')
        
        elif str(codigo) in ['210200', '210210', '200']:
             print(f"✅ SUCESSO! (Status: {codigo} - Já estava OK)")
             print("   -> Atualizando banco para 210200")
             db.registrar_confirmacao_banco(chave, '210200')

        elif codigo == 596:
            print("⛔ FALHA DE PRAZO (596 - Evento fora do prazo)")
            print("   -> Atualizando banco para 210220 (Erro Prazo)")
            db.registrar_confirmacao_banco(chave, '210220')
            
        else:
            print(f"⚠️ Outro código: {codigo}")
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")

if __name__ == "__main__":
    testar_nota_unica()