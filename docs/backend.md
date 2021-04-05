Aluguel de Instrumentos Musicais
================================

# Endpoints

## Categorias

### `GET /api/categorias/`
- Permissões: público
- GET params:
    + `page`: Paginação

### `POST /api/categorias/`
- Permissões: admin
- Payload:
    + `name`: Nome da categoria

Cria uma nova categoria.

### `PATCH,PUT /api/categorias/<id_categoria>/`
- Permissões: admin
- Payload:
    + `name`: Nome da categoria

Modifica uma categoria.

### `DELETE /api/categorias/<id_categoria>/`
- Permissões: admin

Deleta uma categoria.


## Equipamentos

### `GET /api/equipamentos/`
- Permissões: público
- GET params:
    + `start_date`: Exibe só os equips disponíveis a partir dessa data
    + `end_date`: Exibe só os equips disponíveis até essa data
    + `page`: Paginação
    + `categoria`: Exibe só os equips dessa categoria
    + `sort`: Ordena a lista por esse parâmetro

Lista todos os equipamentos disponíveis para alugar.

### `GET /api/equipamentos/<id_equip>/`
- Permissões: público

Retorna os dados de um equipamento, incluindo as datas em que está disponível para alugar.

### `POST /api/equipamentos/`
- Permissões: admin
- Payload:
    + `name`: Nome do equipamento
    + `price_per_day`: Preço por dia de aluguel
    + `description` (opcional): Descrição do equipamento
    + `categorias` (opcional): Categorias do equipamento

Registra um novo equipamento no sistema.

### `PATCH,PUT /api/equipamentos/<id_equip>/`
- Permissões: admin
- Payload:
    + `name`: Nome do equipamento
    + `price_per_day`: Preço por dia de aluguel
    + `description` (opcional): Descrição do equipamento
    + `categorias` (opcional): Categorias do equipamento

Altera informações sobre um equipamento

### `DELETE /api/equipamentos/<id_equip>/`
- Permissões: admin

Remove um equipamento do sistema


## Pedidos

### `GET /api/pedidos/`
- Permissões: autenticado

Retorna uma lista com todos os pedidos referentes ao usuário.

### `GET /api/pedidos/<id_pedido>/`
- Permissões: autenticado, dono do pedido

Retorna os dados do pedido.

### `POST /api/pedidos/`
- Permissões: autenticado
- Payload:
    + `equipamentos`: IDs do equipamento a serem adicionados no pedido
    + `start_date` (opcional): Data de início do aluguel
    + `end_date` (opcional): Data de término do aluguel

Cria um novo pedido e adiciona o item passado nele.

### `POST /api/pedidos/<id_pedido>/`
- Permissões: autenticado, dono do pedido
- Payload:
    + `equipamento`: Id do equipamento a ser adicionado no pedido
    
Adiciona um equipamento a um pedido já existente

### `PATCH /api/pedidos/<id_pedido>/`
- Permissões: autenticado, dono do pedido
- Payload:
    + `start_date`: Data de início do aluguel
    + `end_date`: Data de término do aluguel

Altera a data de aluguel do pedido. Não pode ser usado para alterar os equipamentos do pedido

### `DELETE /api/pedidos/<id_pedido>/equipamentos/<id_equip>/`
- Permissões: autenticado, dono do pedido

Remove um equipamento do pedido.

### `DELETE /api/pedidos/<id_pedido>/`

Apaga um pedido ainda não confirmado.

### `POST /api/pedidos/<id_pedido>/confirmation/`
- Permissões: autenticado, dono do pedido

Confirma que o pedido foi realizado e deve ser efetuado.

### `POST /api/pedidos/<id_pedido>/cancelation/`
- Permissões: autenticado, dono do pedido

Cancela um pedido que havia side confirmado.