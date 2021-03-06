import os
import json
import requests
import ET_Client
import urllib.parse
from urllib.parse import urlencode
from datetime import datetime

"""
 MICROSERVIÇO para levar as leads do formulário aos respectivos lugares. 
  Criado com framework serverless. Usado a conta do MKT/BI para hospedar o microserviço. Para acessar o repositório, confira:
    https://github.com/estrategia-concursos-marketing/microservico-marketing-salescloud

  PROCESSO:
  1. Envia os dados para o Marketing Cloud nas respectivas bases:
    a. Leads_Gerais_5
    b. Total_Base_Geral_
    Lembrando que para acessar essas informações, elas estão salvas como variáveis no Lambda.
  2. Envia os dados para as leads no SalesCloud, para uso do comercial.

  Qualquer PROBLEMA, entre em contato com a equipe de BI e CRM, responsáveis pela produção desse microserviço.
"""

context = '1'
with open('file.json') as json_file:
    event = json.load(json_file)

def add(event, context):
    event1 = json.loads(urllib.parse.parse_qs(event['body'])['data'][0])
    print(event1)

    def marketingCloud(bases, event1):
        stubObj = ET_Client.ET_Client(
            False, False,
            {
                'clientid': os.environ['clientid'],
                'clientsecret': os.environ['clientsecret'],
                'defaultwsdl': 'https://webservice.exacttarget.com/etframework.wsdl',
                'authenticationurl': os.environ['authenticationurl'],
                'baseapiurl': os.environ['baseapiurl'],
                'soapendpoint': os.environ['soapendpoint'],
                'wsdl_file_local_loc': r'/tmp/ExactTargetWSDL.xml',
                'useOAuth2Authentication': 'True',
                'accountId': os.environ['accountId']
            })
        de = ET_Client.ET_DataExtension_Row()
        de.CustomerKey = bases
        de.auth_stub = stubObj
        de.props = props1 if de.CustomerKey == os.environ['basesLeads_Gerais'] else props2
        postResponse = de.post()
        # Mensagens de error para debugar depois! Caso necessário:
        ## print("Post Status: " + str(postResponse.status))
        ## print("Code: " + str(postResponse.code))
        ## print("Message: " + str(postResponse.message))
        ## print("Results: " + str(postResponse.results))

        if postResponse.status:
            return True

    def salesCloud(payload):
        url = 'http://customlead-dev.us-east-1.elasticbeanstalk.com/lead'
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Accept-Encoding': "gzip, deflate",
            'Referer': "http://customlead-dev.us-east-1.elasticbeanstalk.com/lead",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }

        encode = urlencode(payload)

        response = requests.request('POST', url, data=encode, headers=headers)

    def boasVindas(email, event1):
        # Validação do AUTH:
        url = "https://mck0g3r840gk4n89wnf1-q7jml7y.auth.marketingcloudapis.com/v2/token"

        payload = {
            "grant_type": "client_credentials",
            "client_id": os.environ['clientid'],
            "client_secret": os.environ['clientsecret'],
            "account_id": os.environ['accountId']
        }
        payload = json.dumps(payload)

        headers = {
            'Content-Type': "application/json",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Host': "mck0g3r840gk4n89wnf1-q7jml7y.auth.marketingcloudapis.com",
            'Accept-Encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
            }

        response = requests.request("POST", url, data=payload, headers=headers)
        auth = json.loads(response.text)['access_token']

        # Enviar os dados pela Jornada:
        url = "https://mck0g3r840gk4n89wnf1-q7jml7y.rest.marketingcloudapis.com/interaction/v1/events"

        payload = {
            "ContactKey": email,
            "EventDefinitionKey": "APIEvent-f291623d-eaf5-3250-21ba-8c5ffaa90f33",
            "Data": {
                "Nome": event1['first_name'],
                "Email": email,
                "Interesse - Evento": event1['Interesse_Evento__c'],
                "Interesse - Area": event1['Area_de_Interesse__c']
            }
        }

        payload = json.dumps(payload)

        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer " + auth,
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Host': "mck0g3r840gk4n89wnf1-q7jml7y.rest.marketingcloudapis.com",
            'Accept-Encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
            }

        response = requests.request("POST", url, data=payload, headers=headers)
    
    email = event1['email']

    payload = {
        'oid': event1['oid'],
        'retURL': event1['retURL'],
        'Cidade_OrigemIP__c': event1['Cidade_OrigemIP__c'],
        'Estado_OrigemIP__c': event1['Estado_OrigemIP__c'],
        'Modo_de_entrada__c': event1['Modo_de_entrada__c'],
        'leadSource': event1['lead_source'],
        'Area_de_Interesse__c': event1['Area_de_Interesse__c'],
        'Concurso_de_Interesse__c': event1['Concurso_de_Interesse__c'],
        'Interesse_Evento__c': event1['Interesse_Evento__c'],
        'recordTypeId': event1['recordType'],
        'lastName': event1['first_name'],
        'email': event1['email'],
        'mobilePhone': event1['phone']
    }

    props1 = {
        'Cidade de Origem do IP': event1['Cidade_OrigemIP__c'],
        'Estado de Origem do IP': event1['Estado_OrigemIP__c'],
        'Modo de entrada': event1['Modo_de_entrada__c'],
        'Origem do lead': event1['lead_source'],
        'Interesse - Área': event1['Area_de_Interesse__c'],
        'Interesse - Concurso': event1['Concurso_de_Interesse__c'],
        'Interesse - Evento': event1['Interesse_Evento__c'],
        'Nome': event1['first_name'],
        'Email': event1['email'],
        'Telefone': event1['phone'],
        'Data de criação': datetime.now().strftime('%d/%m/%Y'),
        'Hora de Criação': datetime.now().strftime('%H:%M')
    }

    props2 = {
        'Email': event1['email'],
        'Nome': event1['first_name']
    }

    # Principal do Microserviço
    def main(event1):
        salesCloud(payload)

        marketingCloud(os.environ['basesLeads_Gerais'], event1)

        if marketingCloud(os.environ['basesTotal_Gerais'], event1):
            boasVindas(email, event1)

        # Resposta do Request.
        body = {
            'message': 'Lead inserida com sucesso.',
            'input': event1
        }
        response = {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
                "Content-Type": "application/json"
            },
            'body': json.dumps(body)
        }
        print(response)
        return response
    
    main(event1)

add(event, context)
