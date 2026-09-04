# 🏥 Prontus Vitalis

### Inteligência de dados para decisões mais rápidas na saúde
<p align="center">
  <img src="./assets/banner.jpg" alt="Prontus Vitalis">
</p>
              Enterprise Challenge · Oracle × FIAP · 2026/1

O **Prontus Vitalis** é uma solução de análise de dados aplicada à saúde pública, desenvolvida para apoiar gestores na identificação de cenários de maior demanda e pressão assistencial.

A solução integra dados oficiais do **SIH/SUS**, **CNES** e informações territoriais e populacionais do Ministério da Saúde, transformando grandes volumes de dados em indicadores e visualizações que facilitam a análise da situação assistencial.

---

## 🎯 Problema

Gestores e profissionais da saúde precisam tomar decisões com rapidez, mas informações importantes sobre internações, mortalidade, permanência hospitalar e estrutura de atendimento podem estar distribuídas em diferentes fontes de dados.

Essa fragmentação dificulta a identificação de:

* municípios com maior volume de internações;
* períodos de maior demanda hospitalar;
* regiões com maior pressão assistencial;
* relação entre demanda e estrutura hospitalar;
* indicadores que merecem maior atenção da gestão.

O Prontus Vitalis busca transformar esses dados em informações mais acessíveis e úteis para a tomada de decisão.

---

## 💡 Solução

A solução é composta por uma aplicação interativa desenvolvida em **Streamlit**, com processamento e análise de dados oficiais.

### 📊 Dashboard Executivo

O dashboard apresenta uma visão consolidada dos principais indicadores assistenciais e permite explorar os dados por período e município.

Entre os principais recursos estão:

* total de internações;
* número de óbitos;
* dias de permanência;
* permanência média;
* valor total das internações;
* taxa de mortalidade;
* quantidade de unidades hospitalares;
* evolução mensal dos indicadores;
* ranking de municípios;
* detalhamento municipal;
* Índice de Pressão Assistencial (IPA).

### 🚨 Índice de Pressão Assistencial

O **Índice de Pressão Assistencial (IPA)** foi desenvolvido no projeto para identificar municípios que apresentam maior pressão relativa sobre sua estrutura hospitalar.

O indicador considera três componentes:

| Componente                         | Peso |
| ---------------------------------- | ---: |
| Volume de internações              |  40% |
| Dias de permanência                |  30% |
| Internações por unidade hospitalar |  30% |

O resultado é normalizado em uma escala de 0 a 100 e classificado em quatro níveis:

* 🔴 **Crítica**
* 🟠 **Alta**
* 🟡 **Moderada**
* 🟢 **Baixa**

O indicador permite priorizar municípios que apresentam maior pressão assistencial relativa.

---

## 📚 Fontes de dados

O projeto utiliza dados oficiais disponibilizados pelo Ministério da Saúde.

### 1. SIH/SUS — Sistema de Informações Hospitalares do SUS

Utilizado para analisar informações relacionadas a:

* internações;
* óbitos;
* dias de permanência;
* média de permanência;
* taxa de mortalidade;
* valores das internações;
* período e município.

Os dados foram tratados e consolidados para permitir análises mensais e municipais.

### 2. CNES — Cadastro Nacional de Estabelecimentos de Saúde

Utilizado para obter informações sobre a estrutura de estabelecimentos de saúde, incluindo:

* quantidade de estabelecimentos;
* estabelecimentos hospitalares;
* estabelecimentos vinculados ao SUS;
* município;
* localização geográfica.

O cadastro originalmente possui grande volume de registros. Para a aplicação, os dados foram previamente agregados por município, gerando o arquivo `cnes_municipal.csv`.

### 3. Macrorregião e Região de Saúde

Fonte auxiliar utilizada para complementar os dados assistenciais com informações territoriais e populacionais:

* município;
* UF;
* macrorregião de saúde;
* região de saúde;
* população municipal;
* códigos territoriais.

---

## 🔄 Fluxo dos dados

```text
          SIH/SUS
             │
             │
             ▼
     Tratamento e consolidação
             │
             │
CNES ────────┼──────── Dados territoriais
             │
             ▼
       Integração dos dados
             │
             ▼
      Indicadores e análises
             │
             ├───────────────┐
             ▼               ▼
       Dashboard          Índice de
       Streamlit          Pressão
                           Assistencial
             │               │
             └───────┬───────┘
                     ▼
              Apoio à decisão
```

---

## 🗄️ Camada de dados e SQL

Como parte do desenvolvimento da solução, os dados oficiais também foram estruturados em ambiente Oracle para integração e exploração analítica.

Foram desenvolvidas estruturas SQL para:

* armazenamento dos dados do SIH/SUS;
* armazenamento dos dados municipais do CNES;
* armazenamento dos dados territoriais;
* integração entre as fontes;
* consolidação dos indicadores;
* cálculo do Índice de Pressão Assistencial;
* consultas analíticas para apoio à decisão.

Entre as estruturas desenvolvidas estão:

```text
SIH_SUS_CONSOLIDADO
CNES_MUNICIPAL
FONTE_3_REGIOES

VW_PRONTUS_VITALIS
VW_IPA_MUNICIPAL
VW_IPA_MAXIMOS
VW_IPA_COMPONENTES
VW_IPA_FINAL
VW_RESUMO_MENSAL
VW_RESUMO_REGIAO
```

---

## 🖥️ Aplicação

A aplicação foi desenvolvida em **Python + Streamlit**, utilizando os dados oficiais tratados pelo projeto.

Principais tecnologias utilizadas:

| Área                      | Tecnologias         |
| ------------------------- | ------------------- |
| Linguagem                 | Python              |
| Dashboard                 | Streamlit           |
| Manipulação de dados      | Pandas              |
| Visualizações             | Plotly              |
| Banco de dados            | Oracle              |
| Consultas                 | SQL                 |
| Dados hospitalares        | SIH/SUS             |
| Estabelecimentos de saúde | CNES                |
| Dados territoriais        | Ministério da Saúde |
| Controle de versão        | Git / GitHub        |

---

## 📁 Estrutura do projeto

```text
prontus-vitalis/
│
├── assets/
│   └── banner.jpg
│
├── data/
│   └── oficiais/
│       ├── sih_sus/
│       │   ├── dias_permanencia.csv
│       │   ├── internacoes.csv
│       │   ├── media_permanencia.csv
│       │   ├── obitos.csv
│       │   ├── sih_sus_consolidado.csv
│       │   ├── taxa_mortalidade.csv
│       │   └── valor_total.csv
│       │
│       ├── cnes/
│       │   └── cnes_municipal.csv
│       │
│       └── external/
│           └── fonte3_regioes_saude(1).csv
│
├── docs/
│
├── sql/
│
├── src/
│   ├── analise_oficial.py
│   ├── cnes.py
│   ├── indicadores.py
│   └── sih_sus.py
│
├── testes/
│   ├── testar_analise.py
│   ├── testar_indicadores.py
│   ├── testar_sih.py
│   └── testar_valor.py
│
├── app.py
├── README.md
└── requirements.txt
```

---

## 📊 Principais análises

A aplicação permite analisar:

### Evolução temporal

Acompanhamento mensal de:

* internações;
* óbitos;
* dias de permanência;
* valor total;
* permanência média;
* taxa de mortalidade.

### Distribuição municipal

Identificação dos municípios com:

* maior volume de internações;
* maior pressão assistencial;
* maior número de internações por unidade hospitalar.

### Análise territorial

Os dados podem ser relacionados a:

* UF;
* macrorregião de saúde;
* região de saúde;
* população municipal.

### Detalhamento municipal

Cada município pode ser analisado individualmente, permitindo visualizar seus principais indicadores assistenciais e sua classificação de pressão.

---

## 🤖 Evoluções planejadas

Como evolução da solução, está prevista a integração de recursos de **Inteligência Artificial e linguagem natural**, incluindo o uso do **Oracle Select AI** para permitir consultas aos dados por meio de perguntas em linguagem natural.

Exemplos de consultas planejadas:

> "Quais municípios apresentam maior pressão assistencial?"

> "Qual região de saúde concentrou mais internações?"

> "Quais municípios possuem maior volume de internações por unidade hospitalar?"

Essa evolução busca reduzir a necessidade de conhecimento técnico em SQL para exploração dos dados.

---

## 🚀 Aplicação online

**A aplicação está sendo disponibilizada por meio do Streamlit Community Cloud.**

🔗 **Link da aplicação:**
*será disponibilizado após a publicação*

---

## 👥 Equipe — Pyxis Data

| Integrante                    | Atuação                           |
| ----------------------------- | --------------------------------- |
| Alice Silveira                | Conteúdo e público-alvo           |
| Aline Haniele de Castro Silva | Coordenação e problema            |
| Kátia Ribeiro Bianconi        | Solução e benefícios              |
| Matheus da Mata Lima          | Arquitetura e tecnologias         |
| Vitória Santos Ferreira       | Protótipos, dados e gerenciamento |

---

## 🎓 Projeto acadêmico

**Enterprise Challenge — Oracle × FIAP**

**TSCOA · 2026/1**

Projeto desenvolvido no contexto do curso de **Data Science da FIAP**, utilizando dados públicos oficiais do Ministério da Saúde para aplicação de técnicas de tratamento, integração, análise e visualização de dados.

---

## 📌 Observação

Os dados utilizados na solução são provenientes de fontes oficiais e públicas do Ministério da Saúde.

O Índice de Pressão Assistencial é um **indicador desenvolvido especificamente para o projeto**, com finalidade analítica e de apoio à priorização, não representando um indicador oficial do Ministério da Saúde.
