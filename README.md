# Projeto Simulado - BI com Flask

Aplicacao web em Flask para analise de indicadores de negocio a partir do DW simulado.

## 1. Criar banco Docker
Use o arquivo `infra/docker/criar_databases.txt`.

## 2. Criar estrutura do DW
No PgAdmin, conectado ao banco `bi_dw`, execute:
- `db/init/cria_fontes.sql`

## 3. Configurar ambiente da aplicacao
O arquivo `.env` ja foi criado com os parametros padrao.

## 4. Instalar dependencias
`pip install -r requirements.txt`

## 5. Rodar aplicacao
`python run.py`

## Rotas
- `/` inicio
- `/vendas` painel vendas (4 graficos)
- `/produtos` painel produtos (4 graficos)
- `/estoques` painel estoques (4 graficos)
