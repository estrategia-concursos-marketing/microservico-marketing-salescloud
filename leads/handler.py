import os
import re
import json
import FuelSDK
import smtplib
import requests
import ET_Client
import dns.resolver
import configparser # remover pacote depois que subir o microserviço.
from datetime import datetime

config = configparser.ConfigParser()
config.read("cfg.cfg")

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


def emailValidator(Lead_Teste):
    email = Lead_Teste['email']
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
        return True
        
def marketingCloud(Bases, Lead_Teste):
    """


    """

    debug = False
    stubObj = ET_Client.ET_Client(False, debug, Authentication)
    de = ET_Client.ET_DataExtension_Row()
    de.CustomerKey = Bases
    de.auth_stub = stubObj
    de.props = props1 if de.CustomerKey == basesLeads_Gerais else props2
    postResponse = de.post()

    # print('Post Status: ' + str(postResponse.status))
    # print('Code: ' + str(postResponse.code))
    # print('Message: ' + str(postResponse.message))
    print('Results: ' + str(postResponse.results))

    print("Lead no MC com Sucesso")
    return "Lead inserida no MC com Sucesso"


def salesCloud(Lead_Teste):
    url = "https://webto.salesforce.com/servlet/servlet.WebToLead"
    encoding = {"encoding":"UTF-8"}

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

    print("Lead no Salescloud com Sucesso")
    return "Lead no Salescloud com Sucesso"


def main():
    if emailValidator(Lead_Teste):
            body = {
                "message": "Email não existente. Retornar para o usuário.",
                "input": Lead_Teste['email']
            }

            response = {
                "statusCode": 200,
                "body": json.dumps(body)
            }

            return response
        else:
            emailValidator(Lead_Teste)

            salesCloud(Lead_Teste)

            marketingCloud(basesLeads_Gerais, Lead_Teste)

            marketingCloud(basesTotal_Gerais, Lead_Teste)

    
# ===> Variáveis externas no Lambda:
## estrutura é [Chave Externa, Nome da Base]
basesLeads_Gerais = ['TESTE-Microservico-Leads-Gerais-5', 'TESTE-Microservico-Leads-Gerais-5'] # Base simulada de Leads-Gerais-5
basesTotal_Gerais = ['TESTE-Microservico-Total_Emails_Geral_', 'TESTE-Microservico-Total_Emails_Geral_'] # Base simulada de Total_Emails_Geral_

Lead_Teste = {
    "oid": config['LEADS']['oid'],
    "retURL": config['LEADS']['retURL'],
    "Cidade_OrigemIP__c": config['LEADS']['Cidade_OrigemIP__c'],
    "Estado_OrigemIP__c": config['LEADS']['Estado_OrigemIP__c'],
    "Modo_de_entrada__c": config['LEADS']['Modo_de_entrada__c'],
    "lead_source": config['LEADS']['lead_source'],
    "Area_de_Interesse__c": config['LEADS']['Area_de_Interesse__c'],
    "Concurso_de_Interesse__c": config['LEADS']['Concurso_de_Interesse__c'],
    "Interesse_Evento__c": config['LEADS']['Interesse_Evento__c'],
    "recordType": config['LEADS']['recordType'],
    "first_name": config['LEADS']['first_name'],
    "email": config['LEADS']['email'],
    "phone": config['LEADS']['phone']
}

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

Authentication = {
    'clientid': config['MC']['clientid'],
    'clientsecret': config['MC']['clientsecret'],
    'defaultwsdl': config['MC']['defaultwsdl'],
    'authenticationurl': config['MC']['authenticationurl'],
    'baseapiurl': config['MC']['baseapiurl'],
    'soapendpoint': config['MC']['soapendpoint'],
     # 'wsdl_file_local_loc': r'<WSDL_PATH>/ExactTargetWSDL.xml',
    'useOAuth2Authentication': config['MC']['useOAuth2Authentication'],
    'accountId': config['MC']['accountId'],
    # 'scope': '<PERMISSION_LIST>'
}


props1 = {
    "Cidade de Origem do IP": Lead_Teste['Cidade_OrigemIP__c'],
    "Estado de Origem do IP": Lead_Teste['Estado_OrigemIP__c'],
    "Modo de entrada": Lead_Teste['Modo_de_entrada__c'],
    "Origem do lead": Lead_Teste['lead_source'],
    "Interesse - Área": Lead_Teste['Area_de_Interesse__c'],
    "Interesse - Concurso": Lead_Teste['Concurso_de_Interesse__c'],
    "Interesse - Evento": Lead_Teste['Interesse_Evento__c'],
    "Nome": Lead_Teste['first_name'],
    "Email": Lead_Teste['email'],
    "Telefone": Lead_Teste['phone'],
    "Data de criação": datetime.now().strftime("%d/%m/%Y"),
    "Hora de Criação": datetime.now().strftime("%H:%M")
}

props2 = {
    "Email": Lead_Teste['email'],
    "Nome": Lead_Teste['first_name']
}
# ===> Variáveis externas no Lambda:

if __name__ == '__main__':
    main()


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

