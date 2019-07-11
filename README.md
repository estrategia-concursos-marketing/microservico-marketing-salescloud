# Microserviço em Marketing Cloud e Salescloud
Microserviço que vai levar os dados de CRM em POST para o Marketing Cloud e Salescloud.

## Estrutura
Os dados são recebidos dos formulários, seja da home do [Estratégia Concursos](https://www.estrategiaconcursos.com.br/) ou do `/grátis`, e enviado para esse microserviço.

Ele foi construído em NodeJS, usando framework Serverless para enviar as configurações principais para AWS. 

## Resultado
Dessa maneira, as informações serão replicadas para o time de vendas (na conta do Salescloud) e temos em tempo real os dados dos clientes inscritos nos eventos. Assim, é possível fazer réguas mais assertivas.
