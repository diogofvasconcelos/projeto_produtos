from flask import Blueprint, render_template, request, redirect, url_for
from app.services.bi_queries import get_filter_options, get_dashboard_data, get_kpis

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Rota raiz — redireciona para a página de produtos."""
    return redirect(url_for('main.produtos'))


@bp.route('/produtos', methods=['GET'])
def produtos():
    # 1. Capturar filtros enviados pela URL via GET
    filtros = {
        'filial':     request.args.get('filial', ''),
        'categoria':  request.args.get('categoria', ''),
        'fornecedor': request.args.get('fornecedor', ''),
    }

    # 2. Buscar opções de filtro no banco (dimensões reais)
    opcoes_filtros = get_filter_options()

    # 3. Verificar se houve erro de conexão nas opções
    erro_banco = opcoes_filtros.pop('_erro', None)

    # 4. Buscar KPIs com filtros aplicados
    kpis = get_kpis(filtros)
    if '_erro' in kpis:
        erro_banco = kpis.pop('_erro')

    # 5. Buscar dados dos 4 gráficos com filtros aplicados
    charts = get_dashboard_data(filtros)

    # 6. Renderizar o template
    return render_template(
        'produtos.html',
        filtros=filtros,
        opcoes=opcoes_filtros,
        kpis=kpis,
        charts=charts,
        error=erro_banco
    )