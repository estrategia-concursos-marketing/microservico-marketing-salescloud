import os
import json
import FuelSDK
import requests
import ET_Client
import configparser # remover pacote depois que subir o microserviço.

"""
 MICROSERVIÇO para levar as leads do formulário aos respectivos lugares. 
  Criado com framework serverless. Usado a conta do MKT/BI para hospedar o microserviço. Para acessar o repositório, confira:
    https://github.com/estrategia-concursos-marketing/microservico-marketing-salescloud

  PROCESSO:
  1. Valida o email, respondendo sucesso ou não. Resposta no front se não for um email válido;
  2. Envia os dados para o Marketing Cloud nas respectivas bases:
    a. Leads_Gerais_5
    b. Total_Base_Geral_
    Lembrando que para acessar essas informações, elas estão salvas como variáveis no Lambda.
  3. Envia os dados para as leads no SalesCloud, para uso do comercial;
  4. Salva também como uma nova linha em um CSV no S3 da conta do MKT/BI. Para CASO acontecer algum problema entre os dois serviços, mas a lead não ser perdida.

  Qualquer PROBLEMA, entre em contato com a equipe de BI e CRM, responsáveis pela produção desse microserviço.
"""

def emailValidator():
    X = 1

def marketingCloud():
    """


    """

    debug = False
    stubObj = ET_Client.ET_Client(False, False, Bases)
    de = ET_Client.ET_DataExtension_Row()
    de.CustomerKey = DataExtensions[0][0]
    de.auth_stub = stubObj
    de.props = {
        "oid": Lead_Teste['oid'],
        "retURL": Lead_Teste['retURL'],
        "Cidade_OrigemIP__c": Lead_Teste['Cidade_OrigemIP__c'],
        "Estado_OrigemIP__c": Lead_Teste['Estado_OrigemIP__c'],
        "Modo_de_entrada__c": Lead_Teste['Modo_de_entrada__c'],
        "lead_source": Lead_Teste['lead_source'],
        "Area_de_Interesse__c": Lead_Teste['Area_de_Interesse__c'],
        "Concurso_de_Interesse__c": Lead_Teste['Concurso_de_Interesse__c'],
        "Interesse_Evento__c": Lead_Teste['Interesse_Evento__c'],
        "recordType": Lead_Teste['recordType'],
        "first_name": Lead_Teste['first_name'],
        "email": Lead_Teste['email'],
        "phone": Lead_Teste['phone']
    }
    postResponse = de.post()

    print('Post Status: ' + str(postResponse.status))
    print('Code: ' + str(postResponse.code))
    print('Message: ' + str(postResponse.message))
    print('Results: ' + str(postResponse.results))


def salesCloud():
    url = "https://webto.salesforce.com/servlet/servlet.WebToLead"
    encoding = {"encoding":"UTF-8"}

    payload = {
        "oid": Lead_Teste['oid'],
        "retURL": Lead_Teste['retURL'],
        "Cidade_OrigemIP__c": Lead_Teste['Cidade_OrigemIP__c'],
        "Estado_OrigemIP__c": Lead_Teste['Estado_OrigemIP__c'],
        "Modo_de_entrada__c": Lead_Teste['Modo_de_entrada__c'],
        "lead_source": Lead_Teste['lead_source'],
        "Area_de_Interesse__c": Lead_Teste['Area_de_Interesse__c'],
        "Concurso_de_Interesse__c": Lead_Teste['Concurso_de_Interesse__c'],
        "Interesse_Evento__c": Lead_Teste['Interesse_Evento__c'],
        "recordType": Lead_Teste['recordType'],
        "first_name": Lead_Teste['first_name'],
        "email": Lead_Teste['email'],
        "phone": Lead_Teste['phone']
    }
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "webto.salesforce.com",
        'Accept-Encoding': "gzip, deflate",
        'Content-Length': "463",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers, params=encoding)

    # body = {
    #     "message": "Contato inserido com sucesso!",
    #     "input": event
    # }
    # response = {
    #     "statusCode": 200,
    #     "body": json.dumps(body)
    # }
    # return response


def S3andCSV():
    x = 2

def main():
    config = configparser.ConfigParser()
    config.read(r"leads\cfg.cfg")
    print(configparser.get('MC', 'clientid'))
    # emailValidator()

    # salesCloud()

    # marketingCloud(basesLeads_Gerais, Leads_Teste)
    # marketingCloud(basesTotal_Gerais, Leads_Teste)

    # S3andCSV()
    
    # with open('leads\config.json') as json_file:
    #     data = json.load(json_file)
    # print(data)
  


# Variáveis externas no Lambda:
## estrutura é [Chave Externa, Nome da Base]
basesLeads_Gerais = ['03763DA8-E55A-4349-9E42-5354D8E3C176', 'TESTE-Microservico-Leads-Gerais-5'] # Base simulada de Leads-Gerais-5
basesTotal_Gerais = ['75B15A37-E175-401B-8982-7F149A464129', 'TESTE-Microservico-Total_Emails_Geral_'] # Base simulada de Total_Emails_Geral_

Bases = {
    'clientid': '',
    'clientsecret': '',
    'defaultwsdl': '',
    'authenticationurl': '',
    'baseapiurl': '',
    'soapendpoint': '',
     # 'wsdl_file_local_loc': r'<WSDL_PATH>/ExactTargetWSDL.xml',
    'useOAuth2Authentication': 'True',
    'accountId': '',
    # 'scope': '<PERMISSION_LIST>'
}

Lead_Teste = {
    "oid": "00D41000001Q9k8",
    "retURL": "https://www.estrategiaconcursos.com.br/gratis/sucesso-vade-mecum-delagado-pc-rj/",
    "Cidade_OrigemIP__c": "Barueri",
    "Estado_OrigemIP__c": "Sao Paulo",
    "Modo_de_entrada__c": "landing-page",
    "lead_source": "Landing Page",
    "Area_de_Interesse__c": "agencias-reguladoras",
    "Concurso_de_Interesse__c": "detran-sp",
    "Interesse_Evento__c": "Teste-Microservico",
    "recordType": "01241000001AP21",
    "first_name": "1043",
    "email": "israel.mendez232@gmail.com",
    "phone": "(11) 94469-1991"
}


if __name__ == '__main__':
    main()


# def hello(event, context):
#     body = {
#         "message": "Go Serverless v1.0! Your function executed successfully!",
#         "input": event
#     }
# 
#     response = {
#         "statusCode": 200,
#         "body": json.dumps(body)
#     }
# 
#     return response
# 
