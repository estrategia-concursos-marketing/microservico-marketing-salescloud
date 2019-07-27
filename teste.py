import os
import FuelSDK
import ET_Client

# Estruturas das Data Extensions é [CustomerKpip install Salesforce-FuelSDKey, Nome da Base]
DataExtensions = [
    ['52C5B801-D0C2-49A2-B6E1-0BF0BF43E47C', 'Estrategia_cliente']  # Base pequena de testes. EXCLUIR NA PRODUÇÃO FINAL.
]

# Configuração da conta. Colocar isso como variável externa no AIRFLOW. EXCLUIR NA PRODUÇÃO FINAL.
debug = False
stubObj = ET_Client.ET_Client(
  False, False,
  {
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
  })

print('>>>  Add a row to a data extension')
de = ET_Client.ET_DataExtension_Row()
de.CustomerKey = DataExtensions[0][0]
de.auth_stub = stubObj
de.props = {"Nome" : "Teste", "Email" : "teste@gmail.com"}
postResponse = de.post()
print('Post Status: ' + str(postResponse.status))
print('Code: ' + str(postResponse.code))
print('Message: ' + str(postResponse.message))
print('Results: ' + str(postResponse.results))
