# API de Gateway de Pagamento e Cálculo de Frete

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Descrição

Este projeto é uma API RESTful para servir como gateway de pagamento e realizar cálculos de frete. Construído com Python e Django, o projeto é totalmente containerizado com Docker, facilitando a configuração e o deploy em qualquer ambiente.

## Funcionalidades

- **Processamento de Pagamentos:** Integração com serviços de pagamento para processar transações.
- **Cálculo de Frete:** Cálculo de custos de envio baseado em diferentes critérios.
- **Gerenciamento de Pedidos:** Funcionalidades para criar, visualizar e gerenciar pedidos.
- **Autenticação e Autorização:** Endpoints seguros com autenticação baseada em token.
- **Cache de Alto Desempenho:** Uso de Redis para cachear consultas frequentes e melhorar a performance.

## Tecnologias Utilizadas

- **Backend:** Python, Django, Django REST Framework
- **Banco de Dados:** PostgreSQL
- **Cache:** Redis
- **Containerização:** Docker, Docker Compose

## Configuração do Projeto

### Pré-requisitos

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Instalação

1.  **Clone o repositório:**

    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd api-pagamento-frete
    ```

2.  **Configure as variáveis de ambiente:**

    Crie uma cópia do arquivo de exemplo `.env.example` e renomeie para `.env`. Em seguida, ajuste as variáveis conforme necessário para o seu ambiente.

    ```bash
    cp .env.example .env
    ```

3.  **Construa e execute os containers:**

    Para ambiente de **desenvolvimento** (com hot-reload):

    ```bash
    docker-compose up --build
    ```

    Para ambiente de **produção**:

    Primeiro, certifique-se de que a variável `ENV` no seu arquivo `.env` está configurada para `prod` e `DEBUG` para `False`. Em seguida, execute:

    ```bash
    docker-compose up --build -d
    ```

4.  **Execute as migrações do banco de dados:**

    ```bash
    docker-compose exec web python manage.py migrate
    ```

    A aplicação estará disponível em `http://localhost:8000` (ou na porta que você configurou em `.env`).

## Configuração

As seguintes variáveis de ambiente podem ser configuradas no arquivo `.env`:

| Variável          | Descrição                                               | Valor Padrão (dev)          |
| ----------------- | ------------------------------------------------------- | --------------------------- |
| `ENV`             | Ambiente de execução (`dev` ou `prod`)                  | `dev`                       |
| `SECRET_KEY`      | Chave secreta do Django                                 | (gerar uma nova)            |
| `DEBUG`           | Ativa/desativa o modo de debug do Django                | `True`                      |
| `ALLOWED_HOSTS`   | Hosts permitidos para a aplicação                       | `localhost,127.0.0.1`       |
| `PORT`            | Porta em que a aplicação web será exposta               | `8000`                      |
| `POSTGRES_DB`     | Nome do banco de dados PostgreSQL                       | `api_db`                    |
| `POSTGRES_USER`   | Usuário do banco de dados                               | `user`                      |
| `POSTGRES_PASSWORD` | Senha do banco de dados                                 | `password`                  |
| `POSTGRES_HOST`   | Host do banco de dados (nome do serviço no Docker)      | `db`                        |
| `POSTGRES_PORT`   | Porta do banco de dados                                 | `5432`                      |
| `REDIS_HOST`      | Host do Redis (nome do serviço no Docker)               | `redis`                     |
| `REDIS_PORT`      | Porta do Redis                                          | `6379`                      |

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
