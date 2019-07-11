'use strict';

module.exports.add = async (event) => {
  console.log("Iniciando função de adição de lead (handler.add);");

  // Configurações:
  const events = require('./event');
  const account = require('./account');
  const assert = require('assert');
  const ET_Client = require('sfmc-fuelsdk-node');
  const Name = dataExtensionName;
  const client = new ET_Client(
    clientId = account.MarketingCloud.ClientID,
    clientSecret = account.MarketingCloud.ClientSecret,
    stack = 's10',
    );

  const keyField = {
    Name: account.DataExtensions.dataExtensionName, 
    FieldType: 'Text', 
    IsPrimaryKey: true, 
    IsRequired: true, 
    MaxLength: 100
  };

  const props = {
    Name: dataExtensionName, 
    Fields: {Field: [keyField]}
  };

  const props = {Key: dataExtensionRowKey};

  var request = new XMLHttpRequest();
  request.open('GET', '/my/url', true);

  request.onload = function() {
    if (request.status >= 200 && request.status < 400) {
      // POST code for Marketing Cloud:
      client.dataExtensionRow({Name, props}).post((err, response) => {
          if (err) throw new Error(err);
          assert.equal(response.res.statusCode, 200);
          done();
      });

      // POST code for Salescloud:
      const actionSC = account.Salescloud-Post;

      var resp = request.responseText;

    } else {
      console.log("Erro na chamada enviada do formulário.");
    }
  };

  request.onerror = function() {
    // There was a connection error of some sort
  };

  request.send();

  return {
    statusCode: 200,
    message: `O email ${event.email} foi cadastrado com sucesso`
  }
};


// Configurações do Serverless no AWS:
// serverless config credentials --provider aws --key <key_code> --secret <key_secret_code>
// Doc: https://serverless.com/framework/docs/providers/aws/guide/credentials/#using-aws-profiles
