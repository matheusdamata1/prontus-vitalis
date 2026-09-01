import json
import pandas as pd
from pathlib import Path


ARQUIVO_CNES = Path(
    "data/oficiais/cnes/cnes_estabelecimentos.json"
)

ARQUIVO_SAIDA = Path(
    "data/oficiais/cnes/cnes_municipal.csv"
)


def carregar_cnes():
    with open(
        ARQUIVO_CNES,
        "r",
        encoding="utf-8"
    ) as arquivo:
        dados = json.load(arquivo)

    return pd.DataFrame(dados)


def preparar_cnes_municipal(df):
    df = df.copy()

    # Código IBGE do município
    df["COD_MUNICIPIO"] = (
        df["CO_IBGE"]
        .astype(str)
        .str.strip()
        .str.replace(".0", "", regex=False)
        .str.zfill(6)
    )

    # Coordenadas
    df["NU_LATITUDE"] = pd.to_numeric(
        df["NU_LATITUDE"],
        errors="coerce"
    )

    df["NU_LONGITUDE"] = pd.to_numeric(
        df["NU_LONGITUDE"],
        errors="coerce"
    )

    # Estabelecimento hospitalar
    df["HOSPITALAR"] = (
        df["ST_ATEND_HOSPITALAR"]
        .astype(str)
        .str.strip()
        .eq("1.0")
    )

    # Estabelecimento que atende SUS
    df["SUS"] = (
        df["CO_AMBULATORIAL_SUS"]
        .astype(str)
        .str.strip()
        .str.upper()
        .eq("SIM")
    )

    municipal = (
        df.groupby("COD_MUNICIPIO")
        .agg(
            TOTAL_ESTABELECIMENTOS=(
                "CO_CNES",
                "nunique"
            ),
            ESTABELECIMENTOS_HOSPITALARES=(
                "HOSPITALAR",
                "sum"
            ),
            ESTABELECIMENTOS_SUS=(
                "SUS",
                "sum"
            ),
            LATITUDE_MEDIA=(
                "NU_LATITUDE",
                "mean"
            ),
            LONGITUDE_MEDIA=(
                "NU_LONGITUDE",
                "mean"
            )
        )
        .reset_index()
    )

    return municipal


def gerar_cnes_municipal():
    print("Carregando CNES...")
    df = carregar_cnes()

    print(f"Registros CNES: {len(df):,}")

    municipal = preparar_cnes_municipal(df)

    print(
        f"Municípios encontrados: "
        f"{len(municipal):,}"
    )

    municipal.to_csv(
        ARQUIVO_SAIDA,
        sep=";",
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"Arquivo salvo em: {ARQUIVO_SAIDA}"
    )


if __name__ == "__main__":
    gerar_cnes_municipal()
