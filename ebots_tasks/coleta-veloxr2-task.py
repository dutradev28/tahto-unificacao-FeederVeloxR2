from commoncore.core_ebots import *
import requests
import pandas as pd
import json
import re


class ColetaVeloxR2Task(EbotsTaskBase):
    
    task_name = 'coletaVeloxR2' # <- Atualizar este valor com o nome da tarefa no EBots.

    def execute(self, business_key:str) -> None:
        df = self.__consultar_dados_provision()        
        df_filtrado = self.__filtrar_dados(df)
        self.__coloca_protocolos_filtrado_na_fila(df_filtrado)      
    
        

    def __consultar_dados_provision(self):

        url_api = "http://10.172.176.76/ApiAprovisionamentoVelox/api/Provision/GetUrl"
        
        json_parametro = {
            "url": "http://sispx21:8000/provision/apps/ordens_osm_excel.php?tarefa=TOTAL&periodo=TOTAL"
        }
        
            
        response_api = requests.post(url_api, json=json_parametro)
    
        if response_api.status_code == 200:        
            data = response_api.json()
            dados = data["Html"].split("\n")
            lista = list(map(lambda x: x.split("\t"), dados))
            df = pd.DataFrame(lista[1:], columns=lista[0])
            return df
        else:
            self.set_log_info(f"Erro ao realizar o request: {response_api.status_code}")
            raise Exception("Erro ao consultar provision")
        
            

    def __filtrar_dados(self, df):
        try:

            df = df[df['Processo'].str.contains('P217|P83|P215', na=False)]    
                        
            tarefa_patterns = [
            "S199 T05 Monitorar Ativação/Configurar Porta do DSLAM e Testar Velocidade",
            "S418 T01 Monitorar Tarefa Automática OBJECTEL - Consultar Circuito (OMS)",
            "S424 T01 Monitorar Tarefa Automática ASAP Desativar DSLAM (OMS)",
            "S426 T01 Monitorar Tarefa Automática ASAP - Desativar NDS (OMS)",
            "S419 Monitorar Tarefa Objectel Liberar Circuito (OMS)",
            "Monitorar Consulta",
            "S417 T01 Monitorar Tarefa Automática OBJECTEL - Designação (OMS)",
            "S202 T01 Monitorar Ativação AR-NDS/Configurar AR-NDS",
            "S425 T01 Monitorar Tarefa Automática ASAP - Ativar NDS (OMS)",            
            "S424 T0 Desativar Porta do DSLAM (ASAP) - Fallout",
            "S419 T0 Liberar Circuito (OBJ) - Fallout",
            "Monitorar Tarefa Automática",
            "S417 T0 Designar Circuito (OBJ) - Fallout"
            ]
            
            tarefa_pattern = '|'.join([re.escape(pattern) for pattern in tarefa_patterns])
           
            df = df[df['Tarefa'].str.contains(tarefa_pattern, na=False, regex=True)]

            df = df[df['Tarefa'] != "Monitorar Tarefa Automática IMP (OMS)"]
        
            return df
        except Exception as e:
            self.set_log_info(f"Ocorreu um erro ao filtrar o DataFrame ou criar a nova coluna: {e}")
            raise e


    def __coloca_protocolos_filtrado_na_fila(self, df_filtrado):

        protocolos = self.__obter_json(df_filtrado)        
        
            

        self.set_log_info(f'Total de protocolos extraídos: {len(protocolos)}')

        self.set_log_info('Colocando arquivos na fila...')

        lista_itens = []
        lista_business_key_str = []
        for protocolo in protocolos:
            business_key = protocolo
            business_key_str = json.dumps(business_key, ensure_ascii=False)
            if not business_key_str in lista_business_key_str:
                lista_business_key_str.append(business_key_str)
                business_data_str = json.dumps(protocolo, ensure_ascii=False)
                lista_itens.append({
                    'business_key': business_key_str,
                    'business_data': business_data_str
                    })

        adicionados = self.set_job(lista_itens, 'Aguardando processamento VeloxR2', True)     
        
        self.historic = f'{adicionados} protocolos adicionados.'

    def __obter_json(self, df_filtrado):
        
        self.set_log_info(f'{len(df_filtrado)} Convertendo lista em JSON...')
                
        protocolos = df_filtrado.to_json(orient='records')
        lista = json.loads(protocolos)    
       
        
        self.set_log_info(f'{len(lista)} Conversão para JSON concluída!.')

        return lista
    
    


     
 
