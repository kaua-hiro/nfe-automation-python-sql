import requests
import os
import json
from dotenv import load_dotenv

class QiveAPI:
    def __init__(self):
        caminho_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_raiz = os.path.abspath(os.path.join(caminho_atual, '..', '..'))
        load_dotenv(os.path.join(caminho_raiz, '.env'))

        self.base_url = "https://api.arquivei.com.br"
        self.api_id = os.getenv("API_ID")
        self.api_key = os.getenv("API_KEY") or os.getenv("API_TOKEN")
        
        self.headers = {
            "Content-Type": "application/json",
            "x-api-id": self.api_id,
            "x-api-key": self.api_key
        }

    def listar_notas(self, limit=50, cursor=0):
        url = f"{self.base_url}/v1/nfe/received"
        params = {"limit": limit, "cursor": cursor, "access_key_in": ""}
        try:
            response = requests.get(url, headers=self.headers, params=params)
            return response.json().get('data', []) if response.status_code == 200 else []
        except:
            return []

    def consultar_status_manifesto(self, chave):
        url = f"{self.base_url}/v2/nfe/manifest"
        params = { "access_key[]": chave } 
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                dados = response.json().get('data', [])
                if not dados: return None
                codigos = [item.get('code') for item in dados]
                if '210200' in codigos: return '210200'
                if '210220' in codigos: return '210220'
                if '210240' in codigos: return '210240'
                if '210210' in codigos: return '210210'
                return codigos[0]
            return None
        except:
            return None

    def manifestar_nota(self, chave):

        url = f"{self.base_url}/v1/nfe/manifest"
        payload = {
            "manifests": [ { "access_key": chave, "code": "210200" } ]
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                resp_json = response.json()
                data = resp_json.get('data')

                if isinstance(data, dict) and 'request_id' in data:
                    print(f"      [API] Pedido enfileirado! ID: {data['request_id']}")
                    return 135 

                item = None
                if isinstance(data, list) and len(data) > 0:
                    item = data[0]
                elif isinstance(data, dict):
                    item = data
                
                if item:
                    sefaz = item.get('sefaz_response', {})
                    c_stat = sefaz.get('c_stat')
                    if c_stat: return int(c_stat)

                return 135 
            else:
                print(f"[API] Erro HTTP {response.status_code}")
                return None
        except Exception as e:
            print(f"[API] Erro POST: {e}")
            return None