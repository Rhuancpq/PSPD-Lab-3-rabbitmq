# PSPD - 2021/2 - Laboratório 3 (RabbitMQ)
## Integrantes

- João Luis Baraky - 18/0033646
- Rhuan Carlos Queiroz - 180054848

## Execução

**OBS**: É necessário ter o pacote Pika instalado (`$ pip install pika`)

Para executar o programa, é necessário primeiro subir uma instância do RabbitMQ na porta 5672:


`$ docker-compose up`

Executar o arquivo de configuração:

`$ python3 config.py`

Em seguida, executar o(s) worker(s) (servidor):

`$ python3 server.py`

Por fim, executar o cliente:

`$ python3 client.py`

## Utilização

A utilização é de forma automática, sem interação com o usuário

