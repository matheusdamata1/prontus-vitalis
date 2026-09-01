import pandas as pd


# ============================================================
# INDICADORES GERAIS
# ============================================================

def gerar_indicadores_gerais(base_sih, cnes):
    """
    Gera os principais indicadores gerais do SIH/SUS + CNES.
    """

    cnes = cnes.copy()

    # Padroniza nomes das colunas do CNES
    cnes.columns = (
        cnes.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Mantém somente estabelecimentos com atendimento hospitalar
    if "st_atend_hospitalar" in cnes.columns:

        cnes["st_atend_hospitalar"] = pd.to_numeric(
            cnes["st_atend_hospitalar"],
            errors="coerce"
        )

        cnes = cnes[
            cnes["st_atend_hospitalar"] == 1
        ].copy()

    indicadores = {}

    indicadores["internacoes"] = int(
        base_sih["internacoes"].sum()
    )

    indicadores["obitos"] = int(
        base_sih["obitos"].sum()
    )

    indicadores["dias_permanencia"] = int(
        base_sih["dias_permanencia"].sum()
    )

    indicadores["valor_total"] = float(
        base_sih["valor_total"].sum()
    )

    indicadores["municipios"] = int(
        base_sih["municipio"].nunique()
    )

    # Conta somente unidades hospitalares
    if "co_cnes" in cnes.columns:
        indicadores["unidades_hospitalares"] = int(
            cnes["co_cnes"].nunique()
        )
    else:
        indicadores["unidades_hospitalares"] = 0

    return indicadores


# ============================================================
# EVOLUÇÃO MENSAL
# ============================================================

def gerar_evolucao_mensal(base_sih):
    """
    Consolida os dados por mês.
    """

    evolucao = (
        base_sih
        .groupby("periodo_data", as_index=False)
        .agg(
            internacoes=("internacoes", "sum"),
            obitos=("obitos", "sum"),
            dias_permanencia=("dias_permanencia", "sum"),
            valor_total=("valor_total", "sum")
        )
        .sort_values("periodo_data")
    )

    return evolucao


    # ============================================================
# RANKING DE MUNICÍPIOS
# ============================================================

def gerar_ranking_municipios(base_sih, cnes):
    """
    Gera ranking dos municípios por volume de internações
    e cruza com a quantidade de unidades hospitalares.
    """

    # --------------------------------------------------------
    # Cópia e padronização do CNES
    # --------------------------------------------------------

    cnes = cnes.copy()

    cnes.columns = (
        cnes.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # --------------------------------------------------------
    # Mantém somente estabelecimentos com atendimento
    # hospitalar
    # --------------------------------------------------------

    if "st_atend_hospitalar" in cnes.columns:

        cnes["st_atend_hospitalar"] = pd.to_numeric(
            cnes["st_atend_hospitalar"],
            errors="coerce"
        )

        cnes = cnes[
            cnes["st_atend_hospitalar"] == 1
        ].copy()

    # --------------------------------------------------------
    # Ranking dos municípios pelo SIH/SUS
    # --------------------------------------------------------

    ranking = (
        base_sih
        .groupby("municipio", as_index=False)
        .agg(
            internacoes=("internacoes", "sum"),
            obitos=("obitos", "sum"),
            dias_permanencia=("dias_permanencia", "sum"),
            valor_total=("valor_total", "sum")
        )
    )

    # --------------------------------------------------------
    # Extrai código IBGE do município
    # --------------------------------------------------------

    ranking["codigo_ibge"] = (
        ranking["municipio"]
        .astype(str)
        .str.extract(r"^(\d{6})", expand=False)
    )

    # --------------------------------------------------------
    # Remove linhas que não representam municípios
    #
    # Isso elimina textos de observação do DATASUS,
    # como "Notas:" e "Ministério da Saúde..."
    # --------------------------------------------------------

    ranking = ranking[
        ranking["codigo_ibge"].notna()
    ].copy()

    ranking["codigo_ibge"] = (
        ranking["codigo_ibge"]
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------------
    # Quantidade de unidades hospitalares por município
    # --------------------------------------------------------

    if (
        "co_ibge" in cnes.columns
        and "co_cnes" in cnes.columns
    ):

        cnes["co_ibge"] = (
            cnes["co_ibge"]
            .astype(str)
            .str.strip()
        )

        unidades = (
            cnes
            .groupby("co_ibge")
            .agg(
                unidades_hospitalares=(
                    "co_cnes",
                    "nunique"
                )
            )
            .reset_index()
        )

        unidades = unidades.rename(
            columns={
                "co_ibge": "codigo_ibge"
            }
        )

        # ----------------------------------------------------
        # Cruzamento SIH/SUS + CNES
        # ----------------------------------------------------

        ranking = ranking.merge(
            unidades,
            on="codigo_ibge",
            how="left"
        )

    else:

        ranking["unidades_hospitalares"] = 0

    # --------------------------------------------------------
    # Trata municípios sem unidade identificada
    # --------------------------------------------------------

    ranking["unidades_hospitalares"] = (
        pd.to_numeric(
            ranking["unidades_hospitalares"],
            errors="coerce"
        )
        .fillna(0)
        .astype(int)
    )

    # --------------------------------------------------------
    # Internações por unidade hospitalar
    # --------------------------------------------------------

    ranking["internacoes_por_unidade"] = (
        ranking["internacoes"]
        / ranking["unidades_hospitalares"].replace(
            0,
            pd.NA
        )
    )

    # --------------------------------------------------------
    # Ordenação
    # --------------------------------------------------------

    ranking = ranking.sort_values(
        "internacoes",
        ascending=False
    ).reset_index(drop=True)

    return ranking
    
# ============================================================
# ÍNDICE DE PRESSÃO ASSISTENCIAL
# ============================================================

def calcular_pressao_assistencial(ranking):
    """
    Calcula um índice relativo de pressão assistencial.

    Componentes:
    - volume de internações: 40%;
    - dias de permanência: 30%;
    - internações por unidade: 30%.
    """

    df = ranking.copy()

    # --------------------------------------------------------
    # Garante valores numéricos
    # --------------------------------------------------------

    colunas_numericas = [
        "internacoes",
        "dias_permanencia",
        "internacoes_por_unidade"
    ]

    for coluna in colunas_numericas:

        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce"
        )

    # --------------------------------------------------------
    # Função de normalização
    # --------------------------------------------------------

    def normalizar(serie):

        serie = serie.astype(float)

        minimo = serie.min()
        maximo = serie.max()

        if pd.isna(minimo) or pd.isna(maximo):
            return pd.Series(
                0.0,
                index=serie.index
            )

        if maximo == minimo:
            return pd.Series(
                0.0,
                index=serie.index
            )

        return (
            (serie - minimo)
            / (maximo - minimo)
            * 100
        )

    # --------------------------------------------------------
    # Scores
    # --------------------------------------------------------

    df["score_internacoes"] = normalizar(
        df["internacoes"]
    )

    df["score_permanencia"] = normalizar(
        df["dias_permanencia"]
    )

    df["score_internacoes_unidade"] = normalizar(
        df["internacoes_por_unidade"]
    )

    # --------------------------------------------------------
    # Índice de pressão
    #
    # Internações: 40%
    # Permanência: 30%
    # Pressão por unidade: 30%
    # --------------------------------------------------------

    df["indice_pressao"] = (
        df["score_internacoes"] * 0.40
        + df["score_permanencia"] * 0.30
        + df["score_internacoes_unidade"].fillna(0) * 0.30
    )

    # --------------------------------------------------------
    # Classificação
    # --------------------------------------------------------

    def classificar(valor):

        if pd.isna(valor):
            return "Sem dados"

        if valor >= 70:
            return "Crítica"

        elif valor >= 40:
            return "Alta"

        elif valor >= 20:
            return "Moderada"

        else:
            return "Baixa"

    df["classificacao_pressao"] = (
        df["indice_pressao"]
        .apply(classificar)
    )

    return df.sort_values(
        "indice_pressao",
        ascending=False
    )


# ============================================================
# INDICADORES DE PERMANÊNCIA
# ============================================================

def gerar_indicadores_permanencia(base_sih):
    """
    Gera indicadores relacionados à permanência hospitalar.
    """

    total_internacoes = base_sih["internacoes"].sum()

    total_dias = base_sih["dias_permanencia"].sum()

    if total_internacoes > 0:

        permanencia_media_calculada = (
            total_dias / total_internacoes
        )

    else:

        permanencia_media_calculada = 0

    return {
        "dias_permanencia": int(total_dias),
        "permanencia_media": float(
            permanencia_media_calculada
        )
    }


# ============================================================
# INDICADORES DE MORTALIDADE
# ============================================================

def gerar_indicadores_mortalidade(base_sih):
    """
    Gera indicadores relacionados aos óbitos.
    """

    internacoes = base_sih["internacoes"].sum()

    obitos = base_sih["obitos"].sum()

    if internacoes > 0:

        taxa_mortalidade_calculada = (
            obitos / internacoes * 100
        )

    else:

        taxa_mortalidade_calculada = 0

    return {
        "internacoes": int(internacoes),
        "obitos": int(obitos),
        "taxa_mortalidade": float(
            taxa_mortalidade_calculada
        )
    }


# ============================================================
# RESUMO COMPLETO
# ============================================================

def gerar_analise_completa(base_sih, cnes):
    """
    Executa todas as análises necessárias para o dashboard.
    """

    gerais = gerar_indicadores_gerais(
        base_sih,
        cnes
    )

    evolucao = gerar_evolucao_mensal(
        base_sih
    )

    ranking = gerar_ranking_municipios(
        base_sih,
        cnes
    )

    pressao = calcular_pressao_assistencial(
        ranking
    )

    permanencia = gerar_indicadores_permanencia(
        base_sih
    )

    mortalidade = gerar_indicadores_mortalidade(
        base_sih
    )

    return {
        "gerais": gerais,
        "evolucao": evolucao,
        "ranking": ranking,
        "pressao": pressao,
        "permanencia": permanencia,
        "mortalidade": mortalidade
    }
