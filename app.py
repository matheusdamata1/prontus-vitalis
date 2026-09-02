import streamlit as st
import pandas as pd
import plotly.express as px

from src.sih_sus import carregar_sih_sus, consolidar_sih_sus
from src.cnes import carregar_cnes
from src.indicadores import gerar_analise_completa


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Prontus Vitalis",
    page_icon="🏥",
    layout="wide"
)

# ============================================================
# ESTILO VISUAL
# ============================================================

st.markdown(
    """
    <style>

    /* =========================
       CORES PRINCIPAIS
       ========================= */

    :root {
        --azul: #172235;
        --azul-claro: #26364f;
        --vermelho: #e53935;
        --vermelho-claro: #fff1f1;
        --cinza: #f7f8fa;
        --borda: #e5e7eb;
        --texto: #172235;
        --texto-secundario: #64748b;
    }


    /* =========================
       FUNDO
       ========================= */

    .stApp {
        background-color: #f8fafc;
    }

    .main {
        background-color: #f8fafc;
    }


    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
    background-color: var(--azul);
}

section[data-testid="stSidebar"] label {
    color: #e2e8f0 !important;
    font-weight: 500;
}

/* Campos da sidebar */
section[data-testid="stSidebar"] input {
    color: #172235 !important;
    background-color: white !important;
}

section[data-testid="stSidebar"] [data-baseweb="input"] input {
    color: #172235 !important;
    background-color: white !important;
}

section[data-testid="stSidebar"] [data-baseweb="input"] {
    background-color: white !important;
}


    /* =========================
       TÍTULOS
       ========================= */

    h1, h2, h3 {
        color: var(--texto) !important;
    }

    h1 {
        font-weight: 700 !important;
    }

    h2 {
        font-weight: 650 !important;
        margin-top: 2rem !important;
    }

    h3 {
        font-weight: 600 !important;
    }


    /* =========================
       MÉTRICAS
       ========================= */

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid var(--borda);
        border-radius: 10px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    }

    div[data-testid="stMetricLabel"] {
        color: var(--texto-secundario) !important;
        font-size: 0.85rem !important;
    }

    div[data-testid="stMetricValue"] {
        color: var(--azul) !important;
        font-weight: 700 !important;
    }


    /* =========================
       ALERTAS
       ========================= */

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* =========================
       TABELAS
       ========================= */

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--borda);
        border-radius: 10px;
        overflow: hidden;
        background-color: white;
    }


    /* =========================
       EXPANDERS
       ========================= */

    div[data-testid="stExpander"] {
        border: 1px solid var(--borda);
        border-radius: 10px;
        background-color: white;
    }


    /* =========================
       SELECTBOX
       ========================= */

    div[data-baseweb="select"] > div {
        border-radius: 8px;
        border-color: var(--borda);
    }


    /* =========================
       DIVISORES
       ========================= */

    hr {
        border-color: var(--borda);
    }


    /* =========================
       CAPTIONS
       ========================= */

    .stCaption {
        color: var(--texto-secundario);
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def formatar_numero(valor):
    return f"{valor:,.0f}".replace(",", ".")


def formatar_moeda(valor):
    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def formatar_data(data):

    meses = {
        1: "Jan",
        2: "Fev",
        3: "Mar",
        4: "Abr",
        5: "Mai",
        6: "Jun",
        7: "Jul",
        8: "Ago",
        9: "Set",
        10: "Out",
        11: "Nov",
        12: "Dez"
    }

    return f"{meses[data.month]}/{str(data.year)[2:]}"


def extrair_nome_municipio(valor):

    valor = str(valor)

    partes = valor.split(" ", 1)

    if len(partes) == 2:
        return partes[1].strip()

    return valor


# ============================================================
# CABEÇALHO
# ============================================================

st.html(
    """
    <div style="
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 25px;
        padding: 10px 0;
    ">

        <div style="
            background: #e53935;
            color: white;
            width: 46px;
            height: 46px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        ">
            🏥
        </div>

        <div>
            <div style="
                font-size: 28px;
                font-weight: 700;
                color: #172235;
            ">
                Prontus Vitalis
            </div>

            <div style="
                color: #64748b;
                font-size: 14px;
                margin-top: 4px;
            ">
                Painel Inteligente de Acesso Hospitalar e Perfil de Atendimento
            </div>
        </div>

    </div>
    """
)

st.markdown(
    """
    **Fonte dos dados:** SIH/SUS e CNES — DATASUS  
    **Período disponível:** Julho/2024 a Junho/2026
    """
)


# ============================================================
# CARREGAMENTO DOS DADOS
# ============================================================

@st.cache_data
def carregar_dados():

    dados_sih = carregar_sih_sus()

    base_sih = consolidar_sih_sus(
        dados_sih
    )

    cnes = carregar_cnes()

    analise = gerar_analise_completa(
        base_sih,
        cnes
    )

    return analise


with st.spinner(
    "Carregando dados oficiais e calculando indicadores..."
):

    analise = carregar_dados()


gerais = analise["gerais"]
evolucao = analise["evolucao"]
ranking = analise["ranking"]
pressao = analise["pressao"]

# ============================================================
# LIMPEZA DOS MUNICÍPIOS
# ============================================================

def filtrar_municipios_validos(df):

    df = df.copy()

    # Remove registros sem código IBGE
    df = df[df["codigo_ibge"].notna()]

    # Mantém apenas códigos IBGE municipais válidos
    df["codigo_ibge"] = (
        pd.to_numeric(
            df["codigo_ibge"],
            errors="coerce"
        )
    )

    df = df[
        df["codigo_ibge"].notna()
    ]

    # Código IBGE municipal possui 6 dígitos
    df = df[
        df["codigo_ibge"]
        .astype(int)
        .astype(str)
        .str.len()
        == 6
    ]

    return df


ranking = filtrar_municipios_validos(ranking)
pressao = filtrar_municipios_validos(pressao)

# ============================================================
# FILTROS
# ============================================================

st.sidebar.header("🔎 Filtros")

data_min = evolucao["periodo_data"].min().date()
data_max = evolucao["periodo_data"].max().date()

periodo = st.sidebar.date_input(
    "Período de análise",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max
)

if isinstance(periodo, tuple) and len(periodo) == 2:

    data_inicio = pd.Timestamp(periodo[0]).replace(day=1)
    data_fim = pd.Timestamp(periodo[1]).replace(day=1)

else:

    data_inicio = pd.Timestamp(data_min)
    data_fim = pd.Timestamp(data_max)


# ============================================================
# EVOLUÇÃO FILTRADA
# ============================================================

evolucao_filtrada = evolucao[
    (evolucao["periodo_data"] >= data_inicio)
    & (evolucao["periodo_data"] <= data_fim)
].copy()


# ============================================================
# INDICADORES DO PERÍODO
# ============================================================

internacoes_periodo = evolucao_filtrada[
    "internacoes"
].sum()

obitos_periodo = evolucao_filtrada[
    "obitos"
].sum()

dias_periodo = evolucao_filtrada[
    "dias_permanencia"
].sum()

valor_periodo = evolucao_filtrada[
    "valor_total"
].sum()


if internacoes_periodo > 0:

    permanencia_media_periodo = (
        dias_periodo / internacoes_periodo
    )

    mortalidade_periodo = (
        obitos_periodo
        / internacoes_periodo
        * 100
    )

else:

    permanencia_media_periodo = 0
    mortalidade_periodo = 0


# ============================================================
# PERÍODO SELECIONADO
# ============================================================

st.info(
    f"📅 Período selecionado: "
    f"**{formatar_data(data_inicio)} até {formatar_data(data_fim)}**"
)


# ============================================================
# VISÃO GERAL
# ============================================================

st.header("📊 Visão Geral")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Internações",
        formatar_numero(internacoes_periodo)
    )

with col2:

    st.metric(
        "Óbitos",
        formatar_numero(obitos_periodo)
    )

with col3:

    st.metric(
        "Permanência média",
        f"{permanencia_media_periodo:.2f} dias"
    )

with col4:

    st.metric(
        "Valor total",
        formatar_moeda(valor_periodo)
    )


col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Dias de permanência",
        formatar_numero(dias_periodo)
    )

with col2:

    st.metric(
        "Taxa de mortalidade",
        f"{mortalidade_periodo:.2f}%"
    )

with col3:

    st.metric(
        "Unidades hospitalares",
        formatar_numero(
            gerais["unidades_hospitalares"]
        )
    )


# ============================================================
# EVOLUÇÃO MENSAL
# ============================================================

st.header("📈 Evolução Mensal")

st.caption(
    "Acompanhe a evolução dos principais indicadores "
    "assistenciais ao longo do período selecionado."
)

evolucao_grafico = evolucao_filtrada.copy()

evolucao_grafico["mes"] = (
    evolucao_grafico["periodo_data"]
    .apply(formatar_data)
)


# ------------------------------------------------------------
# INTERNAÇÕES
# ------------------------------------------------------------

st.subheader("Internações por mês")

fig = px.line(
    evolucao_grafico,
    x="mes",
    y="internacoes",
    markers=True,
    labels={
        "mes": "",
        "internacoes": "Internações"
    }
)

fig.update_layout(
    height=350,
    margin=dict(l=20, r=20, t=20, b=20),
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ------------------------------------------------------------
# ÓBITOS
# ------------------------------------------------------------

st.subheader("Óbitos por mês")

fig = px.line(
    evolucao_grafico,
    x="mes",
    y="obitos",
    markers=True,
    labels={
        "mes": "",
        "obitos": "Óbitos"
    }
)

fig.update_layout(
    height=350,
    margin=dict(l=20, r=20, t=20, b=20),
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ------------------------------------------------------------
# DIAS DE PERMANÊNCIA
# ------------------------------------------------------------

st.subheader("Dias de permanência por mês")

fig = px.line(
    evolucao_grafico,
    x="mes",
    y="dias_permanencia",
    markers=True,
    labels={
        "mes": "",
        "dias_permanencia": "Dias de permanência"
    }
)

fig.update_layout(
    height=350,
    margin=dict(l=20, r=20, t=20, b=20),
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# DESTAQUES
# ============================================================

st.header("📌 Destaques do período")

if not evolucao_filtrada.empty:

    maior_internacao = evolucao_filtrada.loc[
        evolucao_filtrada["internacoes"].idxmax()
    ]

    maior_obito = evolucao_filtrada.loc[
        evolucao_filtrada["obitos"].idxmax()
    ]

    maior_permanencia = evolucao_filtrada.loc[
        evolucao_filtrada["dias_permanencia"].idxmax()
    ]

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📈 Maior volume de internações",
            formatar_numero(
                maior_internacao["internacoes"]
            ),
            formatar_data(
                maior_internacao["periodo_data"]
            )
        )

    with col2:

        st.metric(
            "⚠️ Maior número de óbitos",
            formatar_numero(
                maior_obito["obitos"]
            ),
            formatar_data(
                maior_obito["periodo_data"]
            )
        )

    with col3:

        st.metric(
            "🛏️ Maior permanência acumulada",
            formatar_numero(
                maior_permanencia["dias_permanencia"]
            ),
            formatar_data(
                maior_permanencia["periodo_data"]
            )
        )


# ============================================================
# RANKING MUNICIPAL
# ============================================================

st.header(
    "🏙️ Municípios com maior volume de internações"
)

st.caption(
    "Ranking dos municípios com maior número acumulado "
    "de internações no período analisado."
)


ranking_exibicao = ranking.head(10).copy()

ranking_exibicao["Município"] = (
    ranking_exibicao["municipio"]
    .apply(extrair_nome_municipio)
)

ranking_exibicao = ranking_exibicao[
    [
        "Município",
        "codigo_ibge",
        "internacoes",
        "obitos",
        "dias_permanencia",
        "unidades_hospitalares",
        "internacoes_por_unidade"
    ]
]

ranking_exibicao.columns = [
    "Município",
    "Código IBGE",
    "Internações",
    "Óbitos",
    "Dias de permanência",
    "Unidades hospitalares",
    "Internações por unidade"
]

ranking_exibicao["Internações"] = (
    ranking_exibicao["Internações"]
    .map(formatar_numero)
)

ranking_exibicao["Óbitos"] = (
    ranking_exibicao["Óbitos"]
    .map(formatar_numero)
)

ranking_exibicao["Dias de permanência"] = (
    ranking_exibicao["Dias de permanência"]
    .map(formatar_numero)
)

ranking_exibicao["Internações por unidade"] = (
    ranking_exibicao["Internações por unidade"]
    .round(2)
)

st.dataframe(
    ranking_exibicao,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DISTRIBUIÇÃO TOP 10
# ============================================================

st.subheader(
    "Distribuição das internações — Top 10"
)

grafico_municipios = ranking.head(10).copy()

grafico_municipios["Município"] = (
    grafico_municipios["municipio"]
    .apply(extrair_nome_municipio)
)

grafico_municipios = grafico_municipios[
    [
        "Município",
        "internacoes"
    ]
].sort_values(
    "internacoes",
    ascending=True
)

grafico_municipios = grafico_municipios.set_index(
    "Município"
)

fig = px.bar(
    grafico_municipios.reset_index(),
    x="internacoes",
    y="Município",
    orientation="h"
)

fig.update_traces(
    marker_color="#d52f2f"
)

fig.update_layout(
    height=430,
    margin=dict(l=20, r=20, t=20, b=20),
    plot_bgcolor="white",
    paper_bgcolor="white",
    xaxis_title="Internações",
    yaxis_title=None
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# PRESSÃO ASSISTENCIAL
# ============================================================

st.header("🚨 Índice de Pressão Assistencial")

st.markdown(
    """
    O **Índice de Pressão Assistencial** é um indicador relativo
    desenvolvido pelo Prontus Vitalis para apoiar a identificação
    de municípios que apresentam maior pressão sobre sua estrutura
    hospitalar.

    O cálculo considera:

    - **40%** — volume de internações
    - **30%** — dias de permanência
    - **30%** — internações por unidade hospitalar

    Quanto maior o índice, maior a pressão assistencial relativa.
    """
)


contagens = pressao[
    "classificacao_pressao"
].value_counts()


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "🔴 Crítica",
        int(contagens.get("Crítica", 0))
    )

with col2:

    st.metric(
        "🟠 Alta",
        int(contagens.get("Alta", 0))
    )

with col3:

    st.metric(
        "🟡 Moderada",
        int(contagens.get("Moderada", 0))
    )

with col4:

    st.metric(
        "🟢 Baixa",
        int(contagens.get("Baixa", 0))
    )


# ============================================================
# ALERTA PRINCIPAL
# ============================================================

criticas = pressao[
    pressao["classificacao_pressao"] == "Crítica"
]


if not criticas.empty:

    principal = criticas.iloc[0]

    nome_principal = extrair_nome_municipio(
        principal["municipio"]
    )

    st.error(
        f"🚨 **Atenção:** {nome_principal} apresenta "
        f"índice de pressão assistencial "
        f"**{principal['indice_pressao']:.2f}**, "
        f"classificado como **Crítico**."
    )

else:

    st.success(
        "Nenhum município foi classificado como crítico "
        "no período analisado."
    )


# ============================================================
# TOP 10 PRESSÃO
# ============================================================

st.subheader(
    "Top 10 — Municípios com maior pressão assistencial"
)

pressao_exibicao = pressao.head(10).copy()

pressao_exibicao["Município"] = (
    pressao_exibicao["municipio"]
    .apply(extrair_nome_municipio)
)

pressao_exibicao = pressao_exibicao[
    [
        "Município",
        "codigo_ibge",
        "indice_pressao",
        "classificacao_pressao",
        "internacoes",
        "dias_permanencia",
        "unidades_hospitalares",
        "internacoes_por_unidade"
    ]
]

pressao_exibicao.columns = [
    "Município",
    "Código IBGE",
    "Índice de pressão",
    "Classificação",
    "Internações",
    "Dias de permanência",
    "Unidades hospitalares",
    "Internações por unidade"
]

pressao_exibicao["Índice de pressão"] = (
    pressao_exibicao["Índice de pressão"]
    .round(2)
)

pressao_exibicao["Internações"] = (
    pressao_exibicao["Internações"]
    .map(formatar_numero)
)

pressao_exibicao["Dias de permanência"] = (
    pressao_exibicao["Dias de permanência"]
    .map(formatar_numero)
)

pressao_exibicao["Internações por unidade"] = (
    pressao_exibicao["Internações por unidade"]
    .round(2)
)

st.dataframe(
    pressao_exibicao,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# GRÁFICO DE PRESSÃO
# ============================================================

st.subheader(
    "Índice de pressão assistencial — Top 10"
)

grafico_pressao = pressao.head(10).copy()

grafico_pressao["Município"] = (
    grafico_pressao["municipio"]
    .apply(extrair_nome_municipio)
)

grafico_pressao = grafico_pressao[
    [
        "Município",
        "indice_pressao"
    ]
].sort_values(
    "indice_pressao",
    ascending=True
)

grafico_pressao = grafico_pressao.set_index(
    "Município"
)

fig = px.bar(
    grafico_pressao.reset_index(),
    x="indice_pressao",
    y="Município",
    orientation="h"
)

fig.update_traces(
    marker_color="#e53935"
)

fig.update_layout(
    height=430,
    margin=dict(l=20, r=20, t=20, b=20),
    plot_bgcolor="white",
    paper_bgcolor="white",
    xaxis_title="Índice de pressão",
    yaxis_title=None
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# DETALHAMENTO MUNICIPAL
# ============================================================

st.header("📋 Detalhamento municipal")

st.caption(
    "Selecione um município para consultar seus principais "
    "indicadores assistenciais."
)


# ------------------------------------------------------------
# MUNICÍPIOS DISPONÍVEIS
# ------------------------------------------------------------

municipios_disponiveis = (
    pressao[
        pressao["codigo_ibge"].notna()
    ]
    .copy()
)

# Garantir que o código IBGE seja válido
municipios_disponiveis = municipios_disponiveis[
    municipios_disponiveis["codigo_ibge"]
    .astype(str)
    .str.fullmatch(r"\d{6}")
]

municipios_disponiveis = (
    municipios_disponiveis["municipio"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

municipios_disponiveis = sorted(
    municipios_disponiveis,
    key=extrair_nome_municipio
)


# ------------------------------------------------------------
# SELEÇÃO DO MUNICÍPIO
# ------------------------------------------------------------

if municipios_disponiveis:

    municipio_selecionado = st.selectbox(
        "Selecione o município",
        municipios_disponiveis
    )

else:

    st.warning(
        "Nenhum município válido foi encontrado."
    )

    municipio_selecionado = None


# ------------------------------------------------------------
# DADOS DO MUNICÍPIO SELECIONADO
# ------------------------------------------------------------

if municipio_selecionado is not None:

    pressao_municipios = pressao[
        pressao["municipio"] == municipio_selecionado
    ].copy()


    if not pressao_municipios.empty:

        municipio_dados = (
            pressao_municipios
            .iloc[0]
        )

        nome_municipio = extrair_nome_municipio(
            municipio_selecionado
        )


        # ====================================================
        # INDICADORES DO MUNICÍPIO
        # ====================================================

        st.subheader(
            f"📍 {nome_municipio}"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Internações",
                formatar_numero(
                    municipio_dados["internacoes"]
                )
            )

        with col2:

            st.metric(
                "Óbitos",
                formatar_numero(
                    municipio_dados["obitos"]
                )
            )

        with col3:

            st.metric(
                "Dias de permanência",
                formatar_numero(
                    municipio_dados["dias_permanencia"]
                )
            )

        with col4:

            st.metric(
                "Unidades hospitalares",
                formatar_numero(
                    municipio_dados["unidades_hospitalares"]
                )
            )


        # ====================================================
        # INDICADORES COMPLEMENTARES
        # ====================================================

        col1, col2, col3 = st.columns(3)

        internacoes_mun = municipio_dados["internacoes"]
        dias_mun = municipio_dados["dias_permanencia"]
        obitos_mun = municipio_dados["obitos"]

        if internacoes_mun > 0:

            media_mun = (
                dias_mun / internacoes_mun
            )

            taxa_mun = (
                obitos_mun
                / internacoes_mun
                * 100
            )

        else:

            media_mun = 0
            taxa_mun = 0


        with col1:

            st.metric(
                "Permanência média",
                f"{media_mun:.2f} dias"
            )


        with col2:

            st.metric(
                "Taxa de mortalidade",
                f"{taxa_mun:.2f}%"
            )


        with col3:

            internacoes_unidade = (
                municipio_dados[
                    "internacoes_por_unidade"
                ]
            )

            if pd.notna(internacoes_unidade):

                st.metric(
                    "Internações por unidade",
                    f"{internacoes_unidade:.2f}"
                )

            else:

                st.metric(
                    "Internações por unidade",
                    "N/A"
                )


        # ====================================================
        # PRESSÃO ASSISTENCIAL
        # ====================================================

        indice_mun = municipio_dados[
            "indice_pressao"
        ]

        classificacao_mun = municipio_dados[
            "classificacao_pressao"
        ]


        st.subheader(
            "🚨 Pressão assistencial"
        )


        if classificacao_mun == "Crítica":

            st.error(
                f"🔴 **Pressão Crítica** — "
                f"Índice: **{indice_mun:.2f}**"
            )

        elif classificacao_mun == "Alta":

            st.warning(
                f"🟠 **Pressão Alta** — "
                f"Índice: **{indice_mun:.2f}**"
            )

        elif classificacao_mun == "Moderada":

            st.warning(
                f"🟡 **Pressão Moderada** — "
                f"Índice: **{indice_mun:.2f}**"
            )

        else:

            st.success(
                f"🟢 **Pressão Baixa** — "
                f"Índice: **{indice_mun:.2f}**"
            )


        # ====================================================
        # INTERPRETAÇÃO
        # ====================================================

        st.subheader(
            "💡 Interpretação"
        )


        if classificacao_mun == "Crítica":

            interpretacao = (
                f"O município de **{nome_municipio}** apresenta "
                f"**pressão assistencial crítica**, com índice de "
                f"**{indice_mun:.2f}**. O resultado indica uma "
                f"concentração elevada dos fatores considerados "
                f"pelo índice."
            )

        elif classificacao_mun == "Alta":

            interpretacao = (
                f"O município de **{nome_municipio}** apresenta "
                f"**pressão assistencial alta**, com índice de "
                f"**{indice_mun:.2f}**. O resultado sugere uma "
                f"demanda relevante sobre a estrutura hospitalar."
            )

        elif classificacao_mun == "Moderada":

            interpretacao = (
                f"O município de **{nome_municipio}** apresenta "
                f"**pressão assistencial moderada**, com índice de "
                f"**{indice_mun:.2f}**. Os indicadores apontam "
                f"para uma demanda intermediária em relação aos "
                f"demais municípios analisados."
            )

        else:

            interpretacao = (
                f"O município de **{nome_municipio}** apresenta "
                f"**pressão assistencial baixa**, com índice de "
                f"**{indice_mun:.2f}** em relação aos demais "
                f"municípios analisados."
            )


        st.info(interpretacao)


    else:

        st.warning(
            "Não foram encontrados indicadores para o município selecionado."
        )


# ============================================================
# TABELA COMPLETA
# ============================================================

with st.expander("📊 Ver tabela completa dos municípios"):

    detalhamento = pressao.copy()

    # Manter somente municípios com código IBGE válido
    detalhamento["codigo_ibge_num"] = pd.to_numeric(
        detalhamento["codigo_ibge"],
        errors="coerce"
    )

    detalhamento = detalhamento[
        detalhamento["codigo_ibge_num"].between(
            100000,
            999999
        )
    ].copy()

    detalhamento["Município"] = (
        detalhamento["municipio"]
        .apply(extrair_nome_municipio)
    )

    detalhamento = detalhamento[
        [
            "Município",
            "codigo_ibge",
            "indice_pressao",
            "classificacao_pressao",
            "internacoes",
            "obitos",
            "dias_permanencia",
            "unidades_hospitalares",
            "internacoes_por_unidade"
        ]
    ]

    detalhamento.columns = [
        "Município",
        "Código IBGE",
        "Índice de pressão",
        "Classificação",
        "Internações",
        "Óbitos",
        "Dias de permanência",
        "Unidades hospitalares",
        "Internações por unidade"
    ]

    detalhamento["Índice de pressão"] = (
        detalhamento["Índice de pressão"]
        .round(2)
    )

    detalhamento["Internações por unidade"] = (
        detalhamento["Internações por unidade"]
        .round(2)
    )

    st.dataframe(
        detalhamento,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "Prontus Vitalis — análise baseada em dados oficiais "
    "do SIH/SUS e CNES (DATASUS)."
)
