from src.sih_sus import carregar_sih_sus, consolidar_sih_sus
from pathlib import Path


print("=" * 60)
print("TESTE — SIH/SUS DATASUS")
print("=" * 60)


dados = carregar_sih_sus()


print("\n" + "=" * 60)
print("ARQUIVOS CARREGADOS")
print("=" * 60)

for nome, df in dados.items():

    print(
        f"{nome:25} "
        f"{len(df):>8,} registros"
    )


print("\n" + "=" * 60)
print("CONSOLIDANDO")
print("=" * 60)


base = consolidar_sih_sus(dados)


print(
    f"\nBase consolidada: "
    f"{len(base):,} registros"
)


print("\nColunas:")

for coluna in base.columns:
    print(f" - {coluna}")


print("\nAmostra:")

print(
    base.head().to_string()
)


print("\n" + "=" * 60)
print("PERÍODO")
print("=" * 60)

print(
    "Inicial:",
    base["periodo_data"].min()
)

print(
    "Final:",
    base["periodo_data"].max()
)


# ============================================================
# SALVAR BASE CONSOLIDADA
# ============================================================

arquivo_saida = Path(
    "data/oficiais/sih_sus/sih_sus_consolidado.csv"
)

base.to_csv(
    arquivo_saida,
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

print("\n" + "=" * 60)
print("ARQUIVO CONSOLIDADO")
print("=" * 60)

print(
    f"✓ Arquivo salvo em: {arquivo_saida}"
)

print(
    f"✓ Registros: {len(base):,}"
)

print(
    f"✓ Colunas: {len(base.columns)}"
)
