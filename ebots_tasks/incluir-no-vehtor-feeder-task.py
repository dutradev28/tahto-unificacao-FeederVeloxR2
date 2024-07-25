from commoncore.core_ebots import *
from commonvehtor import vehtor_api

class IncluirNoVehtorFeederTask(EbotsTaskBase):
    
    task_name = 'incluirFeederNoVehtor'

    def execute(self, business_key:str) -> None:

        #self.next_status = 'skipped'
        
        dados_str = business_key.split('|')[1]        
        #vehtor_url_homolog = self.get_param("vehtor_url_homolog")
        vehtor_url_homolog = 'http://siwhw01a/UnificadoApi/api'
        config_vehtor = {
            'url': vehtor_url_homolog, 
            'ambiente': 'APROVISIONAMENTO' #'crv' 'ambtest' 
        }
        

        dados = json.loads(dados_str)


        self.set_log_info('Criando protocolo no Vehtor...')
        retorno_api = self.__criar_protocolo_no_vehtor(dados, config_vehtor)

        self.set_log_info(f'Retorno da API: {retorno_api}')

        if 'Protocolo já cadastrado' in retorno_api:
            retorno_api = retorno_api.replace('Code 400 - {"Message":"Protocolo já cadastrado: ', '')
            retorno_api = retorno_api.replace('"}', '')
            retorno_api = json.dumps({"Protocolo": retorno_api})

        if 'Code 400' in retorno_api or 'Code 500' in retorno_api:
            raise Exception(retorno_api)
        
        protocolo_json = json.loads(retorno_api)
        try:
            protocolo_json = json.loads(protocolo_json) #as vezes precisa fazer isso
        except:
            pass
        protocolo = protocolo_json['Protocolo']

        self.set_log_info(f'Protocolo: {protocolo}')

        self.historic = json.dumps(protocolo_json, ensure_ascii=False)

        #self.next_status = 'Incluido no Vehtor'

    def __criar_protocolo_no_vehtor(self, dados, config_vehtor):

        
        payload = {
            "Mailing": "FEEDER R1",
            "NomeDaFila": "FEEDER R1 Temporario",
            "EmailUsuario": "stc@btcc.net.br",
            "TipoDados":"DESCRICAO",
            "Dados": dados
        }

        payload_str = json.dumps(payload, ensure_ascii=False)
        self.set_log_info(payload_str)
        print(f"[Config Vehtor] - {str(config_vehtor)}")
        api = vehtor_api.Vehtor(config_vehtor) 
        protocolo = api.tratativa.incluirProtocolo(payload_str)

        return protocolo    
