# datasprints_streaming

### Segunda parte
---
Foi desenvolvido um sistema de streaming baseado em Apache Kafka como broker e Faust (python) como agente.

A funcionalidade da aplicação é:

1- Recebe um JSON contendo as informações de corrida de taxi;

2- Consulta a API do googleMaps para encotnrar o endereço das coordenadas de *pickup* do passageiro;

3- Envia esse endereço para o banco de dados

### Para executar o serviço:
---
- Criar uma cópia do arquivo .env.example papara .env

`$ cp .env.example .env`

  - Preencher com a URI do banco de dados (fornecida no email para fins de testagem do projeto apenas)
  
  **OBS: A API do Google não precisa ser enviada, pois os endereços são gerados através de um faker.**
  
  Para executar o programa, basta rodar: 
  
  `$ docker-compose up --build`
 
 É Necessário aguardar alguns segundos para que todo o ambiente esteja configurado e a aplicação comece a fazer o streaming dos JSON.
