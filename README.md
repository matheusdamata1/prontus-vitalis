# 🏥 Prontus Vitalis

### Inteligência de dados para decisões mais rápidas na saúde.

<p align="center">
  <img src="./assets/banner.jpg" alt="Prontus Vitalis">
</p>

<p align="center">
  <strong>Enterprise Challenge · Oracle × FIAP</strong>
</p>

<p align="center">
  <a href="#sobre">Sobre</a> •
  <a href="#solução">Solução</a> •
  <a href="#tecnologias">Tecnologias</a> •
  <a href="#arquitetura">Arquitetura</a> •
  <a href="#equipe">Equipe</a>
</p>

---

## Sobre

O **Prontus Vitalis** é uma solução desenvolvida para apoiar profissionais e gestores da saúde na tomada de decisões durante situações de emergência.

O projeto parte de um problema simples: **informações importantes para o atendimento podem estar espalhadas em diferentes fontes**, dificultando o acesso rápido a dados sobre hospitais, internações e capacidade de atendimento.

A proposta é transformar esses dados em informações mais claras e acessíveis, contribuindo para decisões mais rápidas e melhor distribuição dos pacientes.

---

## 💡 Solução

O Prontus Vitalis organiza dados da rede de saúde e disponibiliza três principais recursos:

### 📊 Dashboard Executivo

Apresenta indicadores de capacidade hospitalar, internações, ocupação e pressão assistencial, oferecendo uma visão geral da situação da rede.

### 🤖 Assistente IA

Permite realizar consultas aos dados utilizando linguagem natural, com apoio do **Oracle Select AI**.

> "Quais hospitais estão menos pressionados na região?"

### 🏥 Encaminhamento Inteligente

Auxilia na identificação de uma unidade hospitalar adequada considerando informações como disponibilidade, ocupação e perfil de atendimento.

---

## 🔄 Como funciona

```text
 SIH/SUS       CNES        CSV
     │           │          │
     └───────────┼──────────┘
                 ▼
        Tratamento dos dados
                 │
                 ▼
    Oracle Autonomous Database
                 │
        ┌────────┼────────┐
        ▼        ▼        ▼
    Dashboard    IA    Encaminhamento
        │        │        │
        └────────┼────────┘
                 ▼
          Apoio à decisão
```

---

## 🧰 Tecnologias

| Área           | Tecnologias                   |
| -------------- | ----------------------------- |
| Banco de dados | Oracle Autonomous Database    |
| Cloud          | Oracle Cloud Infrastructure   |
| IA             | Oracle Select AI              |
| Linguagem      | Python                        |
| Análise        | Pandas · NumPy · Scikit-learn |
| Consultas      | SQL                           |
| Fontes         | SIH/SUS · CNES · CSV · APIs   |

---

## 🏗️ Arquitetura

A arquitetura foi planejada para conectar diferentes fontes de dados a uma camada central de armazenamento e análise, permitindo disponibilizar informações para os diferentes módulos da solução.

<p align="center">
  <img src="./architecture/arquitetura.png" alt="Arquitetura do Prontus Vitalis">
</p>

A documentação técnica da arquitetura está disponível em:

**[→ Ver documentação da arquitetura](./docs/arquitetura.md)**

---

## 📁 Estrutura

```text
prontus-vitalis/
│
├── architecture/               # Arquitetura e fluxo de dados
├── data/                        # Dados e amostras
├── docs/                        # Documentação
├── notebooks/                   # Análises e Data Science
├── src/                         # Código-fonte
├── sql/                         # Scripts SQL
├── dashboard/                   # Dashboard
├── assistente-ia/               # Assistente IA
├── encaminhamento-inteligente/  # Encaminhamento
├── evidence/                    # Evidências e resultados
└── tests/                       # Testes
```

---

## 🎯 Objetivo

Transformar dados da rede pública de saúde em informações que possam ser utilizadas de forma rápida e prática, apoiando profissionais e gestores em decisões relacionadas ao atendimento de emergência.

---

## 👥 Equipe

### Pyxis Data

| Integrante                    | Atuação                    |
| ----------------------------- | -------------------------- |
| Alice Silveira                | Conteúdo e público-alvo    |
| Aline Haniele de Castro Silva | Coordenação e problema     |
| Kátia Ribeiro Bianconi        | Solução e benefícios       |
| Matheus da Mata Lima          | Arquitetura e tecnologias  |
| Vitória Santos Ferreira       | Protótipos e gerenciamento |

---

<p align="center">
  <strong>Enterprise Challenge · Oracle × FIAP</strong><br>
  TSCOA 2026/1
</p>
