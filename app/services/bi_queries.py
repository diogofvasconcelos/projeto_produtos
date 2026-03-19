from app.db import fetch_all


# ---------------------------------------------------------------------------
# Opções dos filtros (dimensões reais do banco)
# ---------------------------------------------------------------------------

def get_filter_options() -> dict:
    """
    Busca as opções reais para os 3 filtros da página de Produtos
    diretamente das tabelas de dimensão.
    """
    try:
        filiais     = [r["filial"]     for r in fetch_all("SELECT DISTINCT filial     FROM produtos.dim_filial     ORDER BY filial;")]
        categorias  = [r["categoria"]  for r in fetch_all("SELECT DISTINCT categoria  FROM produtos.dim_categoria  ORDER BY categoria;")]
        fornecedores= [r["fornecedor"] for r in fetch_all("SELECT DISTINCT fornecedor FROM produtos.dim_fornecedor ORDER BY fornecedor;")]

        return {"filiais": filiais, "categorias": categorias, "fornecedores": fornecedores}

    except Exception as e:
        return {"filiais": [], "categorias": [], "fornecedores": [], "_erro": str(e)}


# ---------------------------------------------------------------------------
# Helpers para montar cláusula WHERE dinamicamente
# ---------------------------------------------------------------------------

def _build_where(filters: dict) -> tuple[str, dict]:
    """
    Recebe o dicionário de filtros e retorna (cláusula WHERE, params).
    Usa named parameters %(nome)s compatíveis com psycopg3.
    """
    conditions = []
    params = {}

    if filters.get("filial"):
        conditions.append("filial = %(filial)s")
        params["filial"] = filters["filial"]

    if filters.get("categoria"):
        conditions.append("categoria = %(categoria)s")
        params["categoria"] = filters["categoria"]

    if filters.get("fornecedor"):
        conditions.append("fornecedor = %(fornecedor)s")
        params["fornecedor"] = filters["fornecedor"]

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    return where, params


# ---------------------------------------------------------------------------
# KPIs
# ---------------------------------------------------------------------------

def get_kpis(filters: dict) -> dict:
    """
    Retorna os 4 indicadores da área de KPIs da página,
    com os filtros selecionados aplicados.
    Usa apenas colunas disponíveis em produtos_base.sql.
    """
    where, params = _build_where(filters)

    sql = f"""
        SELECT
            SUM(unidades_vendidas)                               AS total_unidades,
            ROUND(AVG(markup_medio_pct)::NUMERIC, 1)             AS markup_medio,
            ROUND(AVG(taxa_lancamento_pct)::NUMERIC, 1)          AS taxa_lancamento_media,
            ROUND(AVG(demanda_media_por_produto)::NUMERIC, 2)    AS demanda_media
        FROM produtos.vm_kpis_produtos_mensal
        {where};
    """

    try:
        rows = fetch_all(sql, params)
        r = rows[0] if rows else {}

        return {
            "total_unidades":    int(r.get("total_unidades") or 0),
            "markup_medio":      float(r.get("markup_medio") or 0.0),
            "taxa_lancamento":   float(r.get("taxa_lancamento_media") or 0.0),
            "demanda_media":     float(r.get("demanda_media") or 0.0),
        }

    except Exception as e:
        return {
            "total_unidades": 0, "markup_medio": 0.0,
            "taxa_lancamento": 0.0, "demanda_media": 0.0,
            "_erro": str(e)
        }


# ---------------------------------------------------------------------------
# Dados dos 4 gráficos
# ---------------------------------------------------------------------------

def get_dashboard_data(filters: dict) -> dict:
    """
    Retorna os dados para os 4 gráficos do dashboard,
    com os filtros selecionados aplicados a todos eles.
    Usa apenas colunas disponíveis em produtos_base.sql.
    """
    where, params = _build_where(filters)

    # Filtros sem categoria (para o gráfico de demanda por categoria)
    params_sem_cat = {k: v for k, v in params.items() if k != "categoria"}
    conds_sem_cat  = [c for c in (where.replace("WHERE ", "").split(" AND ") if where else []) if "categoria" not in c]
    where_sem_cat  = ("WHERE " + " AND ".join(conds_sem_cat)) if conds_sem_cat else ""

    resultado = {
        "unidades_mensal": {
            "titulo": "Unidades Vendidas (Mensal)",
            "filtros_ativos": filters,
            "dados": []
        },
        "markup_mensal": {
            "titulo": "Evolução do Markup Médio (%)",
            "filtros_ativos": filters,
            "dados": []
        },
        "demanda_categoria": {
            "titulo": "Demanda por Categoria",
            "filtros_ativos": filters,
            "dados": []
        },
        "lancamento_descontinuacao": {
            "titulo": "Lançamentos vs. Descontinuações",
            "filtros_ativos": filters,
            "dados": []
        }
    }

    try:
        # Gráfico 1 – Unidades Vendidas por mês
        rows = fetch_all(f"""
            SELECT data_mes, SUM(unidades_vendidas) AS unidades
            FROM produtos.vm_kpis_produtos_mensal
            {where}
            GROUP BY data_mes ORDER BY data_mes;
        """, params)
        resultado["unidades_mensal"]["dados"] = [
            {"mes": str(r["data_mes"]), "valor": int(r["unidades"])} for r in rows
        ]

        # Gráfico 2 – Markup médio por mês
        rows = fetch_all(f"""
            SELECT data_mes, ROUND(AVG(markup_medio_pct)::NUMERIC, 2) AS markup
            FROM produtos.vm_kpis_produtos_mensal
            {where}
            GROUP BY data_mes ORDER BY data_mes;
        """, params)
        resultado["markup_mensal"]["dados"] = [
            {"mes": str(r["data_mes"]), "valor": float(r["markup"])} for r in rows
        ]

        # Gráfico 3 – Demanda por Categoria (ignora filtro de categoria)
        rows = fetch_all(f"""
            SELECT categoria, SUM(unidades_vendidas) AS unidades
            FROM produtos.vm_kpis_produtos_mensal
            {where_sem_cat}
            GROUP BY categoria ORDER BY unidades DESC;
        """, params_sem_cat)
        resultado["demanda_categoria"]["dados"] = [
            {"categoria": r["categoria"], "valor": int(r["unidades"])} for r in rows
        ]

        # Gráfico 4 – Lançamentos vs Descontinuações por mês (taxas %)
        rows = fetch_all(f"""
            SELECT data_mes,
                   ROUND(AVG(taxa_lancamento_pct)::NUMERIC, 2)      AS lancamentos,
                   ROUND(AVG(taxa_descontinuacao_pct)::NUMERIC, 2)  AS descontinuacoes
            FROM produtos.vm_kpis_produtos_mensal
            {where}
            GROUP BY data_mes ORDER BY data_mes;
        """, params)
        resultado["lancamento_descontinuacao"]["dados"] = [
            {"mes": str(r["data_mes"]), "lancamentos": float(r["lancamentos"]), "descontinuacoes": float(r["descontinuacoes"])}
            for r in rows
        ]

    except Exception as e:
        for key in resultado:
            resultado[key]["erro"] = str(e)

    return resultado