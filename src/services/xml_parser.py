import base64
import xml.etree.ElementTree as ET
from datetime import datetime

class XmlParserService:
    @staticmethod
    def ler_xml_completo(xml_b64):

        try:
            if not xml_b64: return None, 9999, None
            
            xml_bytes = base64.b64decode(xml_b64)
            root = ET.fromstring(xml_bytes.decode('utf-8'))
            ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
            
            data_tag = root.find('.//nfe:dhRecbto', ns) or root.find('.//nfe:dhEmi', ns)
            dt_nota = None
            dias = 9999
            if data_tag is not None and data_tag.text:
                dt_nota = datetime.fromisoformat(data_tag.text)
                dias = (datetime.now() - dt_nota.replace(tzinfo=None)).days

            dest_cnpj_tag = root.find('.//nfe:dest/nfe:CNPJ', ns)
            dest_cnpj = dest_cnpj_tag.text if dest_cnpj_tag is not None else None

            emit_cnpj_tag = root.find('.//nfe:emit/nfe:CNPJ', ns)
            emit_cnpj = emit_cnpj_tag.text if emit_cnpj_tag is not None else None
            
            return dt_nota, dias, (dest_cnpj, emit_cnpj)
                
        except Exception:
            return None, 9999, (None, None)