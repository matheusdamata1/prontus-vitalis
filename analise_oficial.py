import pandas as pd
import numpy as np


# ============================================================
# PREPARAÇÃO DO CNES
# ============================================================

def preparar_cnes_municipal(cnes):

    df = cnes.copy()

    df["codigo_ibge"] = (
        df["co_ibge"]
        .astype(str)
        .str.strip()
        .str.replace(".0", "", regex=False)
        .str.zfill(6)
    )

    # Garante que o código CNES seja texto
    df["co_cnes"] = (
        df["co_cnes"]
        .astype(str)
        .str.strip()
    )

    # Converte coordenadas
    for coluna in [
        "nu_latitude",
        "nu_longitude"
    ]:

        if coluna in df.columns:

            df[coluna] = pd.to_numeric(
                df[coluna],
                errors="coerce"
            )

    return df


# ============================================================
# INDICADORES MUNICIPAIS
# ============================================================

def gerar_indicadores_municipais(
    sih,
    cnes
):

    # ========================================================
    # SIH/SUS
    # ========================================================

    base = sih.copy()

    base["codigo_ibge"] = (
        base["municipio"]
        .astype(str)
        .str.strip()
        .str[:6]
    )

    # Remove linhas inválidas
    base = base[
        base["codigo_ibge"].str.match(
            r"^\d{6}$",
            na=False
        )
    ].copy()

    # ========================================================
    # AGREGAÇÃO SIH
    # ========================================================

    municipal = (
        base
        .groupby("codigo_ibge", as_index=False)
        .agg(
            internacoes=(
                "internacoes",
                "sum"
            ),

            dias_permanencia=(
                "dias_permanencia",
                "sum"
            ),

            obitos=(
                "obitos",
                "sum"
            ),

            valor_total=(
                "valor_total",
                "sum"
            )
        )
    )

    # ========================================================
    # MÉDIA DE PERMANÊNCIA
    # ========================================================

    if "media_permanencia" in base.columns:

        media = (
            base
            .groupby("codigo_ibge")
            .agg(
                media_permanencia=(
                    "media_permanencia",
                    "mean"
                )
            )
            .reset_index()
        )

        municipal = municipal.merge(
            media,
            on="codigo_ibge",
            how="left"
        )

    else:

        municipal[
            "media_permanencia"
        ] = np.nan

    # ========================================================
    # TAXA DE MORTALIDADE
    # ========================================================

    if "taxa_mortalidade" in base.columns:

        mortalidade = (
            base
            .groupby("codigo_ibge")
            .agg(
                taxa_mortalidade=(
                    "taxa_mortalidade",
                    "mean"
                )
            )
            .reset_index()
        )

        municipal = municipal.merge(
            mortalidade,
            on="codigo_ibge",
            how="left"
        )

    else:

        municipal[
            "taxa_mortalidade"
        ] = np.nan

    # ========================================================
    # CNES
    # ========================================================

    hospitais = preparar_cnes_municipal(cnes)

    estrutura = (
        hospitais
        .groupby("codigo_ibge", as_index=False)
        .agg(

            unidades_hospitalares=(
                "co_cnes",
                "nunique"
            ),

            latitude=(
                "nu_latitude",
                "mean"
            ),

            longitude=(
                "nu_longitude",
                "mean"
            )
        )
    )

    # ========================================================
    # CRUZAMENTO
    # ========================================================

    resultado = municipal.merge(
        estrutura,
        on="codigo_ibge",
        how="left"
    )

    resultado[
        "unidades_hospitalares"
    ] = (
        resultado[
            "unidades_hospitalares"
        ]
        .fillna(0)
    )

    # ========================================================
    # INDICADORES DERIVADOS
    # ========================================================

    resultado[
        "internacoes_por_unidade"
    ] = (
        resultado["internacoes"]
        /
        resultado[
            "unidades_hospitalares"
        ].replace(0, np.nan)
    )

    resultado[
        "obitos_por_1000_internacoes"
    ] = (
        resultado["obitos"]
        /
        resultado["internacoes"].replace(
            0,
            np.nan
        )
        * 1000
    )

    # ========================================================
    # LIMPEZA
    # ========================================================

    resultado = resultado.replace(
        [np.inf, -np.inf],
        np.nan
    )

    return resultado


# ============================================================
# RANKING DE INTERNAÇÕES
# ============================================================

def ranking_internacoes(
    indicadores,
    n=20
):

    return (
        indicadores
        .sort_values(
            "internacoes",
            ascending=False
        )
        .head(n)
        .copy()
    )


# ============================================================
# RANKING DE PRESSÃO
# ============================================================

def calcular_pressao_assistencial(
    indicadores
):

    df = indicadores.copy()

    # --------------------------------------------------------
    # Normalização
    # --------------------------------------------------------

    def normalizar(serie):

        minimo = serie.min()
        maximo = serie.max()

        if pd.isna(minimo) or pd.isna(maximo):
            return pd.Series(
                0,
                index=serie.index
            )

        if maximo == minimo:
            return pd.Series(
                50,
                index=serie.index
            )

        return (
            (serie - minimo)
            /
            (maximo - minimo)
            * 100
        )

    # --------------------------------------------------------
    # Componentes
    # --------------------------------------------------------

    df["pressao_internacoes"] = normalizar(
        df["internacoes"]
    )

    df["pressao_permanencia"] = normalizar(
        df["dias_permanencia"]
    )

    df["pressao_por_unidade"] = normalizar(
        df["internacoes_por_unidade"]
    )

    # --------------------------------------------------------
    # Índice
    # --------------------------------------------------------

    df["indice_pressao"] = (
        df["pressao_internacoes"] * 0.40
        +
        df["pressao_permanencia"] * 0.30
        +
        df["pressao_por_unidade"] * 0.30
    )

    # --------------------------------------------------------
    # Classificação
    # --------------------------------------------------------

    def classificar(valor):

        if valor >= 75:
            return "Crítica"

        if valor >= 50:
            return "Alta"

        if valor >= 25:
            return "Moderada"

        return "Baixa"

    df["classificacao_pressao"] = (
        df["indice_pressao"]
        .apply(classificar)
    )

    return df


# ============================================================
# RANKING DE PRESSÃO
# ============================================================

def ranking_pressao(
    indicadores,
    n=20
):

    df = calcular_pressao_assistencial(
        indicadores
    )

    return (
        df
        .sort_values(
            "indice_pressao",
            ascending=False
        )
        .head(n)
        .copy()
    )
