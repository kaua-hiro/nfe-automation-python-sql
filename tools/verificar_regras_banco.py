import pyodbc
import os
from dotenv import load_dotenv

def testar_regras():
    print("--- 🧪 TESTE DE REGRAS DE NEGÓCIO (SIMULAÇÃO) ---")

    caminho_atual = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(os.path.join(caminho_atual, '.env'))

    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD") or os.getenv("DB_PASS")
    
    if not password:
        print("❌ Erro: Senha não encontrada.")
        return

    try:
        driver = "{ODBC Driver 17 for SQL Server}"
        conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        print("✅ Conectado para auditoria.\n")

        print(f"{'CHAVE (Final)':<15} | {'STATUS SEFAZ':<12} | {'AÇÃO DO ROBÔ (SIMULAÇÃO)'}")
        print("-" * 75)

        cursor.execute("SELECT TOP 20 ChaveAcesso, StatusSefaz FROM Nfe_Entrada ORDER BY DataImportacao DESC")
        
        for linha in cursor.fetchall():
            chave = linha[0]
            status = str(linha[1]) if linha[1] else "NULL"
            chave_resumida = "..." + chave[-10:] 

            acao = ""
            cor = "" 

            if status == '210210': # Ciência
                acao = "✅ CONFIRMAR (Regra: 210210)"
            elif status == '210240': # Não Realizada
                acao = "✅ CONFIRMAR (Regra: 210240)"
            elif status == 'NULL' or status == 'None': # Sem Status
                acao = "✅ CONFIRMAR (Regra: Nota Nova)"
            elif status == '210200': # Confirmação
                acao = "⛔ IGNORAR (Regra: Já Confirmada)"
            elif status == '210220': # Desconhecimento
                acao = "⛔ IGNORAR (Regra: Não Enviar Confirmação)"
            else:
                acao = f"❓ Status {status} (Ignorar por Segurança)"

            print(f"{chave_resumida:<15} | {status:<12} | {acao}")

    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if 'conn' in locals() and conn: conn.close()

if __name__ == "__main__":
    testar_regras()