import pandas as pd
from pathlib import Path

ARQUIVO_CNES = Path(
    "data/oficiais/cnes/cnes_municipal.csv"
)


def carregar_cnes():
    """
    Carrega a versão municipal agregada do CNES.
    O arquivo foi previamente processado a partir do
    cadastro oficial de estabelecimentos.
    """

    df = pd.read_csv(
        ARQUIVO_CNES,
        sep=";",
        encoding="utf-8-sig"
    )

    df["COD_MUNICIPIO"] = (
        df["COD_MUNICIPIO"]
        .astype(str)
        .str.strip()
        .str.replace(".0", "", regex=False)
        .str.zfill(6)
    )

    return df


def preparar_cnes_municipal(df):
    """
    Mantém compatibilidade com o restante do projeto.
    O arquivo já está agregado por município.
    """
    return df.copy()


def gerar_cnes_municipal():
    """
    Função mantida para compatibilidade.
    O arquivo municipal já foi gerado anteriormente.
    """
    df = carregar_cnes()
    print(f"Municípios CNES: {len(df):,}")
    return df


if __name__ == "__main__":
    gerar_cnes_municipal()
