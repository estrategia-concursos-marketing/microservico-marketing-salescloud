import os
import json
import FuelSDK
import ET_Client

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

def emailValidator(Lead_Teste.Email):


def marketingCloud():
    """


    """

    debug = False
    stubObj = ET_Client.ET_Client(False, False, Bases)
    de = ET_Client.ET_DataExtension_Row()
    de.CustomerKey = DataExtensions[0][0]
    de.auth_stub = stubObj
    de.props = Lead_Teste
    postResponse = de.post()

    print('Post Status: ' + str(postResponse.status))
    print('Code: ' + str(postResponse.code))
    print('Message: ' + str(postResponse.message))
    print('Results: ' + str(postResponse.results))


def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

def salesCloud(Lead_Teste.Email):


def S3andCSV():




def main():
    emailValidator()

    marketingCloud()

    salesCloud()

    S3andCSV()
  

# Variáveis externas no Lambda:
DataExtensions = [ # Estrutura é [Chave Externa, Nome da Base]
    ['03763DA8-E55A-4349-9E42-5354D8E3C176', 'TESTE-Microservico-Leads-Gerais-5'],  # Base simulada de Leads-Gerais-5
    ['75B15A37-E175-401B-8982-7F149A464129', 'TESTE-Microservico-Total_Emails_Geral_']   # Base simulada de Total_Emails_Geral_
]

Bases = {
    'clientid': 'frd0kjo8x032pu3bcd4pxpn4',
    'clientsecret': 'AD0fLFSqfrTkPnXpRCo5Nn2w',
    'defaultwsdl': 'https://webservice.exacttarget.com/etframework.wsdl',
    'authenticationurl': 'https://mck0g3r840gk4n89wnf1-q7jml7y.auth.marketingcloudapis.com/',
    'baseapiurl': 'https://mck0g3r840gk4n89wnf1-q7jml7y.rest.marketingcloudapis.com/',
    'soapendpoint': 'https://mck0g3r840gk4n89wnf1-q7jml7y.soap.marketingcloudapis.com/',
     # 'wsdl_file_local_loc': r'<WSDL_PATH>/ExactTargetWSDL.xml',
    'useOAuth2Authentication': 'True',
    'accountId': '100002066',
    # 'scope': '<PERMISSION_LIST>'
}

Lead_Teste = {
    "Nome" : "Israel Mendes", 
    "Email" : "teste123@gmail.com"
}


if __name__ == '__main__':
  main()
