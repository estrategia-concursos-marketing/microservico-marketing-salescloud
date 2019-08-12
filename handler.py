import os
import json
import smtplib
import requests
import ET_Client
import dns.resolver
import urllib.parse
from datetime import datetime

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
  3. Envia os dados para as leads no SalesCloud, para uso do comercial.

  Qualquer PROBLEMA, entre em contato com a equipe de BI e CRM, responsáveis pela produção desse microserviço.
"""

# context = '1'
# event = {
#     "key": "1",
#     "body": {
#         "oid": "00D41000001Q9k8",
#         "retURL": "https://www.estrategiaconcursos.com.br/gratis/sucesso/",
#         "Cidade_OrigemIP__c": "Barueri",
#         "Estado_OrigemIP__c": "Sao Paulo",
#         "Modo_de_entrada__c": "landing-page",
#         "lead_source": "Landing Page",
#         "Area_de_Interesse__c": "tribunais",
#         "Concurso_de_Interesse__c": "",
#         "Interesse_Evento__c": "TJ CE e TJ AM",
#         "recordType": "01241000001AP21",
#         "first_name": "",
#         "email": "israel.mendes2323232@estrategiaconcursos.com.br",
#         "phone": ""
#       }
#   }

def add(event, context):
    event = event['body']

    def emailValidator(email):
        splitAddress = email.split('@')
        domain = str(splitAddress[1])
    
        records = dns.resolver.query(domain, 'MX')
        mxRecord = records[0].exchange
        mxRecord = str(mxRecord)

        server = smtplib.SMTP()
        server.set_debuglevel(0)
        server.connect(mxRecord)
        server.helo(server.local_hostname)
        server.mail(email)

        code, message = server.rcpt(str(email))
        server.quit()
        if code == 250:
            return 'existingEmail'
        else:
            return 'notExistingEmail'


    def marketingCloud(bases, event):
        stubObj = ET_Client.ET_Client(
            False, False,
            {
                'clientid': 'frd0kjo8x032pu3bcd4pxpn4',
                'clientsecret': 'AD0fLFSqfrTkPnXpRCo5Nn2w',
                'defaultwsdl': 'https://webservice.exacttarget.com/etframework.wsdl',
                'authenticationurl': 'https://mck0g3r840gk4n89wnf1-q7jml7y.auth.marketingcloudapis.com/',
                'baseapiurl': 'https://mck0g3r840gk4n89wnf1-q7jml7y.rest.marketingcloudapis.com/',
                'soapendpoint': 'https://mck0g3r840gk4n89wnf1-q7jml7y.soap.marketingcloudapis.com/',
                'wsdl_file_local_loc': r'/tmp/ExactTargetWSDL.xml',
                'useOAuth2Authentication': 'True',
                'accountId': '100002066'
                # 'clientid': os.environ['clientid'],
                # 'clientsecret': os.environ['clientsecret'],
                # 'defaultwsdl': 'https://webservice.exacttarget.com/etframework.wsdl',
                # 'authenticationurl': os.environ['authenticationurl'],
                # 'baseapiurl': os.environ['baseapiurl'],
                # 'soapendpoint': os.environ['soapendpoint'],
                # 'wsdl_file_local_loc': r'ExactTargetWSDL.xml',
                # 'useOAuth2Authentication': 'True',
                # 'accountId': os.environ['accountId']
            })
        de = ET_Client.ET_DataExtension_Row()
        de.CustomerKey = bases
        de.auth_stub = stubObj
        de.props = props1 if de.CustomerKey == basesLeads_Gerais else props2
        postResponse = de.post()

        # Mensagens de error para debugar depois! Caso necessário:
        ## print("Post Status: " + str(postResponse.status))
        ## print("Code: " + str(postResponse.code))
        ## print("Message: " + str(postResponse.message))
        ## print("Results: " + str(postResponse.results))

    def salesCloud(event):
        url = 'https://webto.salesforce.com/servlet/servlet.WebToLead'
        encoding = {'encoding':'UTF-8'}

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Cache-Control': 'no-cache',
            'Host': 'webto.salesforce.com',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Length': '463',
            'Connection': 'keep-alive',
            'cache-control': 'no-cache'
        }

        response = requests.request('POST', url, data=payload, headers=headers, params=encoding)
    
    email = event['email']

    payload = {
        'oid': event['oid'],
        'retURL': event['retURL'],
        'Cidade_OrigemIP__c': event['Cidade_OrigemIP__c'],
        'Estado_OrigemIP__c': event['Estado_OrigemIP__c'],
        'Modo_de_entrada__c': event['Modo_de_entrada__c'],
        'lead_source': event['lead_source'],
        'Area_de_Interesse__c': event['Area_de_Interesse__c'],
        'Concurso_de_Interesse__c': event['Concurso_de_Interesse__c'],
        'Interesse_Evento__c': event['Interesse_Evento__c'],
        'recordType': event['recordType'],
        'first_name': event['first_name'],
        'email': event['email'],
        'phone': event['phone']
    }

    props1 = {
        'Cidade de Origem do IP': event['Cidade_OrigemIP__c'],
        'Estado de Origem do IP': event['Estado_OrigemIP__c'],
        'Modo de entrada': event['Modo_de_entrada__c'],
        'Origem do lead': event['lead_source'],
        'Interesse - Área': event['Area_de_Interesse__c'],
        'Interesse - Concurso': event['Concurso_de_Interesse__c'],
        'Interesse - Evento': event['Interesse_Evento__c'],
        'Nome': event['first_name'],
        'Email': event['email'],
        'Telefone': event['phone'],
        'Data de criação': datetime.now().strftime('%d/%m/%Y'),
        'Hora de Criação': datetime.now().strftime('%H:%M')
    }

    props2 = {
        'Email': event['email'],
        'Nome': event['first_name']
    }

    basesLeads_Gerais = 'TESTE-Microservico-Leads-Gerais-5'
    basesTotal_Gerais = 'TESTE-Microservico-Total_Emails_Geral_'

    # basesLeads_Gerais = os.environ['basesLeads_Gerais']
    # basesTotal_Gerais = os.environ['basesTotal_Gerais']

    # Principal do Microserviço
    if emailValidator(email) == 'notExistingEmail':
        body = {
            'message': 'Email nao existente. Retornar para o usuario.',
            'input': email
        }
        response = {
            statusCode: 409,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': true,
                'Content-Type': 'application/json',
            },
            body: json.dumps(body)
        }
        print(response)
        return response
    else:
        salesCloud(event)
        marketingCloud(basesLeads_Gerais, event)
        marketingCloud(basesTotal_Gerais, event)
        body = {
            'message': 'Leads inseridas com sucesso',
            'input': event
        }
        response = {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': true,
                'Content-Type': 'application/json',
            },
            body: json.dumps(body)
        }
        print(response)
        return response

# add(event, context)
