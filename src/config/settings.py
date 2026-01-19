import os
from dotenv import load_dotenv
MODO_SIMULACAO = True
load_dotenv()

DB_CONFIG = {
    'driver': 'ODBC Driver 17 for SQL Server',
    'server': os.getenv('DB_SERVER'),       
    'database': os.getenv('DB_NAME'),       
    'username': os.getenv('DB_USER'),       
    'password': os.getenv('DB_PASS'),      
    'trusted_connection': 'no'
}

API_URL_BASE = "https://api.arquivei.com.br/v1/nfe"
API_ID = os.getenv("QIVE_API_ID")
API_KEY = os.getenv("QIVE_API_KEY")

DISCORD_URL = os.getenv("DISCORD_WEBHOOK_URL")