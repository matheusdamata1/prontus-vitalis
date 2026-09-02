from src.sih_sus import carregar_sih_sus


print("=" * 60)
print("TESTE — VALOR TOTAL SIH/SUS")
print("=" * 60)

dados = carregar_sih_sus()

df = dados["valor_total"]

print()
print("Registros:", len(df))

print()
print("Colunas:")
print(df.columns.tolist())

print()
print("Primeiros registros:")
print(
    df[
        [
            "municipio",
            "periodo",
            "valor_total"
        ]
    ].head(10).to_string(index=False)
)

print()
print("Estatísticas:")
print(
    df["valor_total"].describe()
)

print()
print(
    "Soma total: "
    f"R$ {df['valor_total'].sum():,.2f}"
)

print()
print("=" * 60)
