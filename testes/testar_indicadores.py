from src.sih_sus import (
    carregar_sih_sus,
    consolidar_sih_sus
)

from src.cnes import carregar_cnes

from src.indicadores import (
    gerar_analise_completa
)


print("=" * 70)
print("PRONTUS VITALIS — TESTE DOS INDICADORES")
print("=" * 70)


# ============================================================
# 1. SIH/SUS
# ============================================================

print("\n1. CARREGANDO SIH/SUS")

dados_sih = carregar_sih_sus()

base_sih = consolidar_sih_sus(
    dados_sih
)

print(
    f"\nBase SIH consolidada: "
    f"{len(base_sih):,} registros"
)


# ============================================================
# 2. CNES
# ============================================================

print("\n2. CARREGANDO CNES")

cnes = carregar_cnes()

print(
    f"CNES: {len(cnes):,} registros"
)


# ============================================================
# 3. INDICADORES
# ============================================================

print("\n3. GERANDO INDICADORES")

analise = gerar_analise_completa(
    base_sih,
    cnes
)


# ============================================================
# 4. INDICADORES GERAIS
# ============================================================

print("\n" + "=" * 70)
print("INDICADORES GERAIS")
print("=" * 70)

gerais = analise["gerais"]

print(
    f"Internações: "
    f"{gerais['internacoes']:,}"
)

print(
    f"Óbitos: "
    f"{gerais['obitos']:,}"
)

print(
    f"Dias de permanência: "
    f"{gerais['dias_permanencia']:,}"
)

print(
    f"Valor total: "
    f"R$ {gerais['valor_total']:,.2f}"
)

print(
    f"Municípios: "
    f"{gerais['municipios']:,}"
)

print(
    f"Unidades hospitalares: "
    f"{gerais['unidades_hospitalares']:,}"
)


# ============================================================
# 5. PERMANÊNCIA
# ============================================================

print("\n" + "=" * 70)
print("PERMANÊNCIA")
print("=" * 70)

permanencia = analise["permanencia"]

print(
    f"Dias de permanência: "
    f"{permanencia['dias_permanencia']:,}"
)

print(
    f"Permanência média calculada: "
    f"{permanencia['permanencia_media']:.2f} dias"
)


# ============================================================
# 6. MORTALIDADE
# ============================================================

print("\n" + "=" * 70)
print("MORTALIDADE")
print("=" * 70)

mortalidade = analise["mortalidade"]

print(
    f"Internações: "
    f"{mortalidade['internacoes']:,}"
)

print(
    f"Óbitos: "
    f"{mortalidade['obitos']:,}"
)

print(
    f"Taxa de mortalidade calculada: "
    f"{mortalidade['taxa_mortalidade']:.2f}%"
)


# ============================================================
# 7. EVOLUÇÃO MENSAL
# ============================================================

print("\n" + "=" * 70)
print("EVOLUÇÃO MENSAL")
print("=" * 70)

evolucao = analise["evolucao"]

print(
    evolucao[
        [
            "periodo_data",
            "internacoes",
            "obitos",
            "dias_permanencia"
        ]
    ].to_string(index=False)
)


# ============================================================
# 8. TOP 10 INTERNAÇÕES
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 — INTERNAÇÕES")
print("=" * 70)

ranking = analise["ranking"]

print(
    ranking[
        [
            "codigo_ibge",
            "internacoes",
            "obitos",
            "unidades_hospitalares",
            "internacoes_por_unidade"
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# 9. PRESSÃO ASSISTENCIAL
# ============================================================

print("\n" + "=" * 70)
print("ÍNDICE DE PRESSÃO ASSISTENCIAL")
print("=" * 70)

pressao = analise["pressao"]

print(
    pressao[
        "classificacao_pressao"
    ].value_counts()
)


print("\nTOP 10 — PRESSÃO ASSISTENCIAL")

print(
    pressao[
        [
            "codigo_ibge",
            "indice_pressao",
            "classificacao_pressao",
            "internacoes",
            "dias_permanencia",
            "unidades_hospitalares",
            "internacoes_por_unidade"
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# 10. EVOLUÇÃO DO ÍNDICE
# ============================================================

print("\n" + "=" * 70)
print("ANÁLISE FINALIZADA")
print("=" * 70)

print(
    "\n✓ SIH/SUS oficial processado"
)

print(
    "✓ CNES oficial processado"
)

print(
    "✓ Indicadores gerais calculados"
)

print(
    "✓ Evolução mensal calculada"
)

print(
    "✓ Ranking municipal calculado"
)

print(
    "✓ Índice de pressão calculado"
)

print(
    "\nPróxima etapa: integração com o Streamlit."
)
