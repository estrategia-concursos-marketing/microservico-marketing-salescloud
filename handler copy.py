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
# event = {"body": "data=%7B%22oid%22%3A%2200D41000001Q9k8%22%2C%22retURL%22%3A%22https%3A%2F%2Fwww.estrategiaconcursos.com.br%2Fgratis%2Fsucesso%2F%22%2C%22Cidade_OrigemIP__c%22%3A%22Barueri%22%2C%22Estado_OrigemIP__c%22%3A%22Sao+Paulo%22%2C%22Modo_de_entrada__c%22%3A%22landing-page%22%2C%22lead_source%22%3A%22Landing+Page%22%2C%22Area_de_Interesse__c%22%3A%22tribunais%22%2C%22Concurso_de_Interesse__c%22%3A%22%22%2C%22Interesse_Evento__c%22%3A%22%22%2C%22recordType%22%3A%2201241000001AP21%22%2C%22first_name%22%3A%22israel%22%2C%22email%22%3A%22israel.mendes%40estrategiaconcursos.com.br%22%2C%22phone%22%3A%22(55)+11944-6919%22%7D", "isBase64Encoded": 0}

def add(event, context):
    event1 = json.loads(urllib.parse.parse_qs(event['body'])['data'][0])
    
    def emailValidator(email):
        splitAddress = email.split('@')
        domain = str(splitAddress[1])

        # try:
        #     records = dns.resolver.query(domain, 'MX')
        # except:
        #     return 'notExistingEmail'
        
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
        de.props = props1 if de.CustomerKey == 'TESTE-Microservico-Leads-Gerais-5' else props2
        postResponse = de.post()
        # Mensagens de error para debugar depois! Caso necessário:
        ## print("Post Status: " + str(postResponse.status))
        ## print("Code: " + str(postResponse.code))
        ## print("Message: " + str(postResponse.message))
        ## print("Results: " + str(postResponse.results))

        if not postResponse.status:
            return False
        else:
            return True

    def salesCloud(payload):
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
    
    email = event1['email']

    payload = {
        'oid': event1['oid'],
        'retURL': event1['retURL'],
        'Cidade_OrigemIP__c': event1['Cidade_OrigemIP__c'],
        'Estado_OrigemIP__c': event1['Estado_OrigemIP__c'],
        'Modo_de_entrada__c': event1['Modo_de_entrada__c'],
        'lead_source': event1['lead_source'],
        'Area_de_Interesse__c': event1['Area_de_Interesse__c'],
        'Concurso_de_Interesse__c': event1['Concurso_de_Interesse__c'],
        'Interesse_Evento__c': event1['Interesse_Evento__c'],
        'recordType': event1['recordType'],
        'first_name': event1['first_name'],
        'email': event1['email'],
        'phone': event1['phone']
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

    # bases = [
    #     os.environ['basesLeads_Gerais'],
    #     os.environ['basesTotal_Gerais']
    # ]

    bases = [
        'TESTE-Microservico-Leads-Gerais-5',
        'TESTE-Microservico-Total_Emails_Geral_'
    ]

    # Principal do Microserviço
    if emailValidator(email) == 'notExistingEmail':
        body = {
            'message': 'Email nao existente. Retornar para o usuario.',
            'input': email
        }
        response = {
            'statusCode': 409,
            'headers': {
                "Access-Control-Allow-Credentials": True,
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            'body': json.dumps(body)
        }
        print(response)
        return response
    else:
        salesCloud(event1)

        for base in bases:
            marketingCloud(base, event1)

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

# add(event, context)
