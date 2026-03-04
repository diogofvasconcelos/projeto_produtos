SELECT
    data_mes,
    filial,
    cidade,
    uf,
    regiao,
    categoria,
    fornecedor,
    unidades_vendidas,
    markup_medio_pct,
    demanda_media_por_produto,
    taxa_lancamento_pct,
    taxa_descontinuacao_pct,
    crescimento_unidades_pct
FROM produtos.vm_kpis_produtos_mensal
ORDER BY data_mes;
