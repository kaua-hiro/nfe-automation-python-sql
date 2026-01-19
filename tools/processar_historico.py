import sys
import os
import pyodbc
import time
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.qive_api import QiveAPI
from src.models.database import DatabaseModel

caminho_env = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(caminho_env)

DB_PROD_SERVER = '192.168.10.5'
DB_PROD_DATABASE = 'EmpresaConfidencial_PRODUCAO'
DB_PROD_USER = 'suporte.linx'
DB_PROD_PASS = 'p@ssw0rdEmpresaConfidencial'

def conectar_producao():
    try:
        conn_str = f'DRIVER={{SQL Server}};SERVER={DB_PROD_SERVER};DATABASE={DB_PROD_DATABASE};UID={DB_PROD_USER};PWD={DB_PROD_PASS}'
        return pyodbc.connect(conn_str)
    except Exception as e:
        print(f"âŒ Erro ao conectar no ERP (ProduÃ§Ã£o): {e}")
        return None

def conectar_local():
    try:
        server = '192.168.10.27'      
        database = 'EmpresaConfidencial_Integracao_NFe'  
        user = 'suporte.linx'         
        password = 'p@ssw0rdEmpresaConfidencial'              
        
        conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password}'
        return pyodbc.connect(conn_str)
    except Exception as e:
        print(f"âŒ Erro ao conectar no Banco Local (.27): {e}")
        return None

def rodar_historico():
    print("\n--- ðŸ“œ CARGA HISTÃ“RICA OTIMIZADA (DELTA) ---")

    conn_prod = conectar_producao()
    conn_local = conectar_local()
    
    if not conn_prod or not conn_local:
        return

    api = QiveAPI()
    db_local_model = DatabaseModel()

    print("â³ Carregando notas jÃ¡ processadas no banco local...")
    cursor_local = conn_local.cursor()
    cursor_local.execute("SELECT ChaveAcesso FROM Nfe_Entrada WHERE StatusSefaz IN ('210200', '210220')")
    notas_feitas = {row[0] for row in cursor_local.fetchall()} 
    print(f"   -> {len(notas_feitas)} notas jÃ¡ estÃ£o resolvidas no banco local.")

    print("â³ Buscando notas na ProduÃ§Ã£o (Ãºltimos 175 dias)...")
    cursor_prod = conn_prod.cursor()
    query_plena = """
        SELECT CHAVE_NFE 
        FROM ENTRADAS
        WHERE DATA_AUTORIZACAO_NFE >= DATEADD(DAY, -175, CAST(GETDATE() AS date)) 
        AND CHAVE_NFE is not null
    """
    cursor_prod.execute(query_plena)
    notas_erp = [row[0] for row in cursor_prod.fetchall()]
    print(f"   -> {len(notas_erp)} notas encontradas na janela de tempo do ERP.")

    fila_pendente = [chave for chave in notas_erp if chave not in notas_feitas]
    
    total_pendente = len(fila_pendente)
    
    if total_pendente == 0:
        print("\nâœ… TUDO EM DIA! Nenhuma nota pendente para processar.")
        return

    print(f"\nðŸš€ INICIANDO PROCESSAMENTO DE {total_pendente} NOTAS PENDENTES...")
    print("(As notas jÃ¡ confirmadas foram removidas da fila)\n")

    contador = 0
    for chave in fila_pendente:
        contador += 1
        print(f"[{contador}/{total_pendente}] Processando: {chave}")

        dados_banco = db_local_model.buscar_nota_por_chave(chave)
        if not dados_banco:
            db_local_model.gravar_empresa_na_nota(chave, "HISTORICO_ERP")

        status_api = api.consultar_status_manifesto(chave)
        
        if status_api == '210200':
            print("   -> JÃ¡ confirmada na API. Sincronizando banco...")
            db_local_model.registrar_confirmacao_banco(chave, '210200')
        else:
            print("   -> Enviando ConfirmaÃ§Ã£o...")
            codigo_retorno = api.manifestar_nota(chave)
            
            if codigo_retorno == 135:
                print("      âœ… Sucesso (135)! Banco atualizado.")
                db_local_model.registrar_confirmacao_banco(chave, '210200')
            elif codigo_retorno == 596:
                print("      â›” Prazo Perdido (596). Marcando Desconhecido.")
                db_local_model.registrar_confirmacao_banco(chave, '210220')
            else:
                print(f"      âš ï¸ Retorno: {codigo_retorno}")

    print("\nðŸ PROCESSO FINALIZADO!")
    conn_prod.close()
    conn_local.close()

if __name__ == "__main__":
    rodar_historico()
