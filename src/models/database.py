import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseModel:
    def __init__(self):
        self.server = os.getenv("DB_SERVER")
        self.database = os.getenv("DB_DATABASE") or "EmpresaConfidencial_Integracao_NFe"
        self.username = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        
        self.conn = None
        self.cursor = None
        self.conectar()

    def conectar(self):
        try:
            conn_str = f'DRIVER={{SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
            self.conn = pyodbc.connect(conn_str)
            self.cursor = self.conn.cursor()
            print("âœ… [DB] Conectado ao banco SQL Server (Local).")
        except Exception as e:
            print(f"âŒ [DB] Erro de conexÃ£o Local: {e}")
            raise e

    def buscar_notas_pendentes(self):

        try:
            prod_server = os.getenv("DB_PROD_SERVER") or '192.168.10.5'
            prod_db = os.getenv("DB_PROD_DATABASE") or 'EmpresaConfidencial_PRODUCAO'
            prod_user = os.getenv("DB_PROD_USER") or self.username 
            prod_pass = os.getenv("DB_PROD_PASS") or self.password

            conn_str_prod = f'DRIVER={{SQL Server}};SERVER={prod_server};DATABASE={prod_db};UID={prod_user};PWD={prod_pass}'
            conn_prod = pyodbc.connect(conn_str_prod)
            cursor_prod = conn_prod.cursor()

            # Pega notas dos Ãºltimos 15 dias
            query_prod = """
                SELECT CHAVE_NFE 
                FROM ENTRADAS 
                WHERE DATA_AUTORIZACAO_NFE >= DATEADD(DAY, -15, CAST(GETDATE() AS date))
                AND CHAVE_NFE IS NOT NULL
            """
            cursor_prod.execute(query_prod)
            chaves_erp = {row[0] for row in cursor_prod.fetchall()}
            conn_prod.close()
        
        except Exception as e:
            print(f"âŒ [DB] Erro ao buscar no ERP (ProduÃ§Ã£o): {e}")
            return []

        try:
            query_local = "SELECT ChaveAcesso FROM Nfe_Entrada WHERE StatusSefaz IN ('210200', '210220')"
            self.cursor.execute(query_local)
            chaves_locais = {row[0] for row in self.cursor.fetchall()}
        except Exception as e:
            print(f"âŒ [DB] Erro ao buscar no Local: {e}")
            chaves_locais = set()

        pendentes = list(chaves_erp - chaves_locais)
        return [(p,) for p in pendentes]

    def buscar_nota_por_chave(self, chave):
        query = "SELECT ChaveAcesso FROM Nfe_Entrada WHERE ChaveAcesso = ?"
        try:
            self.cursor.execute(query, (chave,))
            return self.cursor.fetchone()
        except:
            return None

    def gravar_empresa_na_nota(self, chave, nome_empresa="ROBO_AUTO"):
        if self.buscar_nota_por_chave(chave):
            return

        query = """
        INSERT INTO Nfe_Entrada (ChaveAcesso, EMPRESA_DESTINO, DataImportacao, StatusSefaz)
        VALUES (?, ?, GETDATE(), 'PENDENTE')
        """
        try:
            self.cursor.execute(query, (chave, nome_empresa))
            self.conn.commit()
        except Exception as e:
            print(f"âš ï¸ Erro ao gravar nota nova: {e}")

    def registrar_confirmacao_banco(self, chave, status_code):
        if not self.buscar_nota_por_chave(chave):
            self.gravar_empresa_na_nota(chave, "ROBO_AUTO")

        query = """
        UPDATE Nfe_Entrada
        SET StatusSefaz = ?
        WHERE ChaveAcesso = ?
        """
        try:
            self.cursor.execute(query, (str(status_code), chave))
            self.conn.commit()
        except Exception as e:
            print(f"âš ï¸ Erro ao atualizar status: {e}")
