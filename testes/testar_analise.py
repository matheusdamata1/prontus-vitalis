from src.sih_sus import (
    carregar_sih_sus,
    consolidar_sih_sus
)

from src.cnes import preparar_cnes

from src.analise_oficial import (
    gerar_indicadores_municipais,
    ranking_internacoes,
    ranking_pressao,
    calcular_pressao_assistencial
)


print("=" * 70)
print("PRONTUS VITALIS — ANÁLISE OFICIAL")
print("=" * 70)


# ============================================================
# SIH/SUS
# ============================================================

print()
print("1. CARREGANDO SIH/SUS")

dados_sih = carregar_sih_sus()

sih = consolidar_sih_sus(
    dados_sih
)

print(
    f"\nBase SIH consolidada: "
    f"{len(sih):,} registros"
)


# ============================================================
# CNES
# ============================================================

print()
print("2. CARREGANDO CNES")

cnes = preparar_cnes()


# ============================================================
# INDICADORES
# ============================================================

print()
print("3. GERANDO INDICADORES")

indicadores = gerar_indicadores_municipais(
    sih,
    cnes
)

print(
    f"Municípios analisados: "
    f"{len(indicadores):,}"
)


# ============================================================
# TOTAL
# ============================================================

print()
print("=" * 70)
print("INDICADORES GERAIS")
print("=" * 70)

print(
    f"Internações: "
    f"{indicadores['internacoes'].sum():,.0f}"
)

print(
    f"Óbitos: "
    f"{indicadores['obitos'].sum():,.0f}"
)

print(
    f"Dias de permanência: "
    f"{indicadores['dias_permanencia'].sum():,.0f}"
)

print(
    f"Valor total: "
    f"R$ {indicadores['valor_total'].sum():,.2f}"
)

print(
    f"Unidades hospitalares: "
    f"{indicadores['unidades_hospitalares'].sum():,.0f}"
)


# ============================================================
# RANKING INTERNAÇÕES
# ============================================================

print()
print("=" * 70)
print("TOP 10 — INTERNAÇÕES")
print("=" * 70)

top_internacoes = ranking_internacoes(
    indicadores,
    10
)

print(
    top_internacoes[
        [
            "codigo_ibge",
            "internacoes",
            "obitos",
            "unidades_hospitalares",
            "internacoes_por_unidade"
        ]
    ].to_string(index=False)
)


# ============================================================
# PRESSÃO
# ============================================================

print()
print("=" * 70)
print("4. ÍNDICE DE PRESSÃO ASSISTENCIAL")
print("=" * 70)

indicadores_pressao = (
    calcular_pressao_assistencial(
        indicadores
    )
)

print(
    indicadores_pressao[
        "classificacao_pressao"
    ]
    .value_counts()
)


# ============================================================
# TOP PRESSÃO
# ============================================================

print()
print("=" * 70)
print("TOP 10 — PRESSÃO ASSISTENCIAL")
print("=" * 70)

top_pressao = ranking_pressao(
    indicadores,
    10
)

print(
    top_pressao[
        [
            "codigo_ibge",
            "indice_pressao",
            "classificacao_pressao",
            "internacoes",
            "dias_permanencia",
            "unidades_hospitalares",
            "internacoes_por_unidade"
        ]
    ].to_string(index=False)
)


# ============================================================
# FIM
# ============================================================

print()
print("=" * 70)
print("✓ ANÁLISE CONCLUÍDA")
print("=" * 70)
