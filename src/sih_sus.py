import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# CONFIGURAÇÃO
# ============================================================

PASTA_SIH = Path("data/oficiais/sih_sus")

DATA_INICIO = pd.Timestamp("2024-07-01")
DATA_FIM = pd.Timestamp("2026-06-30")


# ============================================================
# LEITURA DO CSV DATASUS
# ============================================================

def carregar_csv_bruto(arquivo):
    """
    Lê arquivos CSV exportados pelo DATASUS/TabNet.

    O arquivo possui algumas linhas iniciais de descrição
    antes da tabela propriamente dita.
    """

    encodings = [
        "latin1",
        "cp1252",
        "utf-8"
    ]

    ultimo_erro = None

    for encoding in encodings:

        try:

            df = pd.read_csv(
                arquivo,
                sep=";",
                encoding=encoding,
                skiprows=3,
                dtype=str,
                engine="python"
            )

            if len(df.columns) > 1:

                print(
                    f"CSV carregado: {arquivo.name} | "
                    f"linhas={len(df)} | "
                    f"colunas={len(df.columns)}"
                )

                return df

        except Exception as e:

            ultimo_erro = e

    raise ValueError(
        f"Não foi possível ler {arquivo.name}. "
        f"Erro: {ultimo_erro}"
    )


# ============================================================
# LIMPEZA DOS NOMES
# ============================================================

def limpar_nomes_colunas(df):

    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.strip('"')
        .str.replace("\ufeff", "", regex=False)
    )

    return df


# ============================================================
# NORMALIZAÇÃO DE TEXTO
# ============================================================

def normalizar_texto(valor):

    if pd.isna(valor):
        return ""

    return (
        str(valor)
        .strip()
        .strip('"')
    )


# ============================================================
# CONVERSÃO DE NÚMEROS
# ============================================================

def converter_numero(valor):

    if pd.isna(valor):
        return np.nan

    valor = str(valor).strip()

    # Valores vazios do DATASUS
    if valor in [
        "",
        "-",
        "--",
        "...",
        "..."
    ]:
        return 0.0

    # Remove símbolos monetários
    valor = (
        valor
        .replace("R$", "")
        .replace(" ", "")
    )

    # Número brasileiro:
    # 1.234,56 -> 1234.56
    if "," in valor:

        valor = valor.replace(".", "")
        valor = valor.replace(",", ".")

    else:

        # Número já no padrão 1234.56
        # mantém o ponto decimal
        pass

    try:

        return float(valor)

    except ValueError:

        return np.nan


# ============================================================
# IDENTIFICAÇÃO DAS COLUNAS DE PERÍODO
# ============================================================

def identificar_colunas_periodo(df):

    colunas_periodo = []

    meses = [
        "Jan",
        "Fev",
        "Mar",
        "Abr",
        "Mai",
        "Jun",
        "Jul",
        "Ago",
        "Set",
        "Out",
        "Nov",
        "Dez"
    ]

    for coluna in df.columns:

        nome = normalizar_texto(coluna)

        # Formato DATASUS:
        # 2024/Jul
        partes = nome.split("/")

        if len(partes) == 2:

            ano, mes = partes

            if (
                ano.isdigit()
                and len(ano) == 4
                and mes in meses
            ):

                colunas_periodo.append(coluna)

    return colunas_periodo


# ============================================================
# TRANSFORMAÇÃO WIDE -> LONG
# ============================================================

def transformar_para_long(df, nome_indicador):

    df = limpar_nomes_colunas(df)

    # Primeira coluna = município
    coluna_municipio = df.columns[0]

    colunas_periodo = identificar_colunas_periodo(df)

    if not colunas_periodo:

        raise ValueError(
            f"Nenhuma coluna de período encontrada "
            f"em {nome_indicador}."
        )

    # Mantém município + períodos
    dados = df[
        [coluna_municipio] + colunas_periodo
    ].copy()

    dados = dados.rename(
        columns={
            coluna_municipio: "municipio"
        }
    )

    # Remove linhas de total
    dados["municipio"] = (
        dados["municipio"]
        .astype(str)
        .str.strip()
    )

    dados = dados[
        ~dados["municipio"]
        .str.lower()
        .eq("total")
    ].copy()
    
    # Mantém apenas municípios com código IBGE de 6 dígitos
    dados = dados[
        dados["municipio"]
        .str.match(r"^\d{6}\s+", na=False)
    ].copy()

    # Wide -> Long
    dados = dados.melt(
        id_vars=["municipio"],
        value_vars=colunas_periodo,
        var_name="periodo",
        value_name=nome_indicador
    )

    # Limpeza
    dados["municipio"] = (
        dados["municipio"]
        .astype(str)
        .str.strip()
    )

    dados["periodo"] = (
        dados["periodo"]
        .astype(str)
        .str.strip()
    )

    # Converte período
    dados["periodo_data"] = pd.to_datetime(
        dados["periodo"],
        format="%Y/%b",
        errors="coerce"
    )

    # O pandas pode não reconhecer abreviações portuguesas.
    # Fazemos conversão manual como garantia.

    mapa_meses = {
        "Jan": 1,
        "Fev": 2,
        "Mar": 3,
        "Abr": 4,
        "Mai": 5,
        "Jun": 6,
        "Jul": 7,
        "Ago": 8,
        "Set": 9,
        "Out": 10,
        "Nov": 11,
        "Dez": 12
    }

    def converter_periodo(valor):

        try:

            ano, mes = valor.split("/")

            mes_numero = mapa_meses.get(mes)

            if mes_numero is None:
                return pd.NaT

            return pd.Timestamp(
                year=int(ano),
                month=mes_numero,
                day=1
            )

        except Exception:

            return pd.NaT

    dados["periodo_data"] = (
        dados["periodo"]
        .apply(converter_periodo)
    )

    # Converte indicador para número
    dados[nome_indicador] = (
        dados[nome_indicador]
        .apply(converter_numero)
    )

    # Filtra período oficial escolhido
    dados = dados[
        (dados["periodo_data"] >= DATA_INICIO)
        &
        (dados["periodo_data"] <= DATA_FIM)
    ].copy()

    return dados


# ============================================================
# ARQUIVOS SIH/SUS
# ============================================================

def carregar_sih_sus():

    arquivos = {
        "internacoes": "internacoes.csv",
        "media_permanencia": "media_permanencia.csv",
        "dias_permanencia": "dias_permanencia.csv",
        "obitos": "obitos.csv",
        "taxa_mortalidade": "taxa_mortalidade.csv",
        "valor_total": "valor_total.csv"
    }

    dados = {}

    for nome, arquivo in arquivos.items():

        caminho = PASTA_SIH / arquivo

        print()
        print(
            f"Carregando SIH/SUS: {arquivo}"
        )

        df_bruto = carregar_csv_bruto(
            caminho
        )

        df = transformar_para_long(
            df_bruto,
            nome
        )

        dados[nome] = df

        print(
            f"  ✓ {nome}: "
            f"{len(df):,} registros após filtro"
        )

    return dados


# ============================================================
# CONSOLIDAÇÃO
# ============================================================

def consolidar_sih_sus(dados):

    base = dados["internacoes"].copy()

    indicadores = [
        "media_permanencia",
        "dias_permanencia",
        "obitos",
        "taxa_mortalidade",
        "valor_total"
    ]

    # Chaves da integração
    chaves = [
        "municipio",
        "periodo",
        "periodo_data"
    ]

    for indicador in indicadores:

        df = dados[indicador].copy()

        # Garante uma única linha por município/período
        auxiliar = (
            df
            .groupby(
                chaves,
                as_index=False
            )[indicador]
            .sum()
        )

        base = base.merge(
            auxiliar,
            on=chaves,
            how="left"
        )

    # Preenche ausência como zero
    for coluna in [
        "internacoes",
        "media_permanencia",
        "dias_permanencia",
        "obitos",
        "taxa_mortalidade",
        "valor_total"
    ]:

        if coluna in base.columns:

            base[coluna] = (
                pd.to_numeric(
                    base[coluna],
                    errors="coerce"
                )
                .fillna(0)
            )

    # Ordenação
    base = base.sort_values(
        [
            "periodo_data",
            "municipio"
        ]
    ).reset_index(drop=True)

    return base
