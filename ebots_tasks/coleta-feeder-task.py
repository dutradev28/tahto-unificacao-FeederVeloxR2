from commoncore.core_ebots import *
import requests
import pandas as pd
import json


class ColetaFeederTask(EbotsTaskBase):
    
    task_name = 'coletaFeeder' # <- Atualizar este valor com o nome da tarefa no EBots.

    def execute(self, business_key:str) -> None:
        df = self.__consultar_dados_provision()        
        df_filtrado = self.__filtrar_dados(df)
        self.__coloca_protocolos_filtrado_na_fila(df_filtrado)      
    
        

    def __consultar_dados_provision(self):

        url_api = "http://10.172.176.76/ApiAprovisionamentoVelox/api/Provision/GetUrl"
        
        json_parametro = {
            "url": "http://sispx21:8000/provision/apps/ordens_expediter_excel.php?tarefa=TOTAL&periodo=TOTAL&responsavel="
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
            df_filtrado = df[df['Responsavel'].str.contains('GAS', na=False) & 
            df['Atividade'].str.contains('FEEDER', na=False)].copy()                       
            df_filtrado.loc[:, 'Circuito TOT'] = df_filtrado['Localidade'] + 'AD' + df_filtrado['Numero Circuito']
            return df_filtrado
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

        adicionados = self.set_job(lista_itens, 'Aguardando processamento Feeder', True)     
        
        self.historic = f'{adicionados} protocolos adicionados.'

    def __obter_json(self, df_filtrado):
        
        self.set_log_info(f'{len(df_filtrado)} Convertendo lista em JSON...')
                
        protocolos = df_filtrado.to_json(orient='records')
        lista = json.loads(protocolos)    
       
        
        self.set_log_info(f'{len(lista)} Conversão para JSON concluída!.')

        return lista
    
    


     
 
