# Microserviço em Marketing Cloud e Salescloud
Microserviço que vai levar os dados de CRM em POST para o Marketing Cloud e Salescloud.

## Estrutura
Os dados são recebidos dos formulários, seja da home do [Estratégia Concursos](https://www.estrategiaconcursos.com.br/) ou do `/grátis`, e enviado para esse microserviço.

Ele foi construído em Python, usando framework Serverless para enviar as configurações principais para AWS. 

## Processo
1. Envia os dados para o Marketing Cloud nas respectivas bases:
  a. Leads_Gerais_5
  b. Total_Base_Geral_
  Lembrando que para acessar essas informações, elas estão salvas como variáveis no Lambda.
2. Envia os dados para as leads no SalesCloud, para uso do comercial.

## Resultado
Dessa maneira, as informações serão replicadas para o time de vendas (na conta do Salescloud) e temos em tempo real os dados dos clientes inscritos nos eventos. Assim, é possível fazer réguas mais assertivas.

### Observações
Qualquer PROBLEMA, entre em contato com a equipe de BI e CRM, responsáveis pela produção desse microserviço.
