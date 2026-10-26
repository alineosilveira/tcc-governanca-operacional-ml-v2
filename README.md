# Aprendizado de Máquina para Suporte à Decisão na Governança Operacional de Equipes de Tecnologia — v2

Trabalho de Conclusão de Curso – MBA em Data Science e Analytics (USP/Esalq)
Autora: Aline Oliveira da Silveira · Orientador: Ricardo Theodoro

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alineosilveira/tcc-governanca-operacional-ml-v2/blob/main/TCC_Analise_e_Modelos_v2.ipynb)

> **Versão 2.** A v2 usa uma **nova fonte de dados**: uma extração própria e completa do Jira público da Apache Software Foundation, de 25/10/2026. A [versão 1](https://github.com/alineosilveira/tcc-governanca-operacional-ml) usou a base TAWOS. Os repositórios são independentes, e nenhum resultado da v1 é reaproveitado aqui.

## Objetivo

O trabalho avalia se, e em que condições, os registros históricos do Jira (releases, bugs, histórico de alterações e reaberturas) permitem descrever e prever indicadores de governança operacional de equipes de tecnologia, usando técnicas ensinadas no MBA.

As hipóteses **H1** e **H2** são confirmatórias:
- **H1:** características da release conhecidas na publicação × bugs vinculados a ela em 180 dias.
- **H2:** previsão, na abertura, da faixa de tempo até a correção do bug.

As análises de retrabalho e de composição das demandas são exploratórias. **Sprints estão fora do escopo** desta versão. Os resultados são associações observacionais, não relações de causa e efeito. O **projeto Apache é a unidade primária** de análise.

## Como visualizar ou executar

| Modo | Como |
|---|---|
| **1. Consulta** | Abra [`TCC_Analise_e_Modelos_v2.ipynb`](TCC_Analise_e_Modelos_v2.ipynb) aqui no GitHub, já salvo com todas as saídas, ou veja `resultados/` |
| **2. Reprodução completa local** | Requer o snapshot JSONL (não publicado); ver [`docs/reproducao.md`](docs/reproducao.md) |
| **3. Colab** | O botão acima abre o notebook executado **para consulta**. A reexecução no Colab não é possível sem as bases locais, que não são publicadas. Se o repositório estiver privado, o Colab exige autorização de acesso ao GitHub. |

Para obter o código e os resultados:

```bash
git clone https://github.com/alineosilveira/tcc-governanca-operacional-ml-v2.git
cd tcc-governanca-operacional-ml-v2
```

## Estrutura

```
TCC_Analise_e_Modelos_v2.ipynb   documento científico principal (executado, com saídas)
src/coleta/                      apache_jira_extract.py (coleta via API) e quality_report.py (integridade)
src/preparacao/                  01 projeção · 05 regras validadas + bases B–E · 06 níveis de evidência · 07 bases de modelagem
src/analise/                     02 auditoria das aulas (materiais não incluídos) · 03 cobertura · 04 caracterização por projeto (base A)
docs/                            metodologia, linhagem, dicionário de dados, decisões metodológicas, reprodução
resultados/tabelas/              resultados agregados por projeto e métricas dos modelos (CSV)
resultados/graficos/             gráficos do notebook (PNG)
resultados/coleta/               manifest.json e relatório de qualidade da coleta
tests/                           verificações mínimas (chaves, joins, cronologia, T0, privacidade)
```

## Dados

- **Fonte:** `https://issues.apache.org/jira` (Jira Server 10.3.26), API REST v2, acesso anônimo e somente leitura.
- **Critério:** `created >= 2020-01-01 OR updated >= 2020-01-01 OR resolution IS EMPTY`.
- **Snapshot:** 25/10/2026 (20:22–21:57 UTC).
- **Conteúdo:** 561.369 issues de 650 projetos, 6.464.445 históricos de alteração, 1.991.188 comentários, 843.975 worklogs e 23.837 versões, sem duplicatas e sem dados associados faltantes.
- **Período principal das análises:** eventos a partir de 2020. Antes disso a coleta é seletiva: só traz issues abertas ou atualizadas depois de 2020.

O snapshot (≈ 21 GB, ou 43 GB com intermediários) **não** é versionado: pelo volume e por conter nomes de exibição e logins de contribuidores e o texto integral de comentários. Apenas resultados agregados por projeto são publicados.

## Pipeline

```
API Apache Jira ─► src/coleta/apache_jira_extract.py ─► snapshot JSONL ─► src/coleta/quality_report.py (integridade)
      ─► src/preparacao/01_projetar_base.py (cache compacto, pessoas pseudonimizadas)
      ─► src/analise/03, 04 (cobertura e caracterização por projeto)
      ─► src/preparacao/05, 06 (regras validadas → bases analíticas)
      ─► src/preparacao/07 (variáveis em T0, split cronológico)
      ─► TCC_Analise_e_Modelos_v2.ipynb ─► resultados/
```

Os detalhes estão em [`docs/linhagem_dados.md`](docs/linhagem_dados.md).

## Instalação e execução

```bash
python -m venv .venv && .venv/Scripts/activate        # Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env                                   # ajuste os caminhos (nenhuma credencial é necessária)

# coleta (opcional; uma nova coleta difere do snapshot porque o Jira continua ativo)
python src/coleta/apache_jira_extract.py
python src/coleta/quality_report.py

# preparação das bases (requer o snapshot)
python src/preparacao/01_projetar_base.py
python src/analise/03_diagnostico_cobertura.py
python src/analise/04_caracterizacao_por_projeto.py
python src/preparacao/05_validar_regras_negocio.py
python src/preparacao/06_validar_pendencias.py
python src/preparacao/07_bases_modelagem.py
python -m pytest tests -q

# notebook
jupyter nbconvert --to notebook --execute --inplace TCC_Analise_e_Modelos_v2.ipynb
```

## Principais resultados desta execução

| Frente | Resultado |
|---|---|
| Releases × bugs | 6.018 releases desde 2020. Dos vínculos por Affects Version, 71,7% são de bugs criados após a release; 133 projetos têm associação verificável. A data do vínculo é comprovada por evento em 15,9% e inferida com corroboração em 76,6%. |
| H1 (Binomial Negativa + efeito de projeto; teste 2024–2026; D2 aplicada) | MAE de 6,75 contra 9,48 do baseline, em 48 projetos (42 no teste). Tamanho da release em T0: IRR 1,41 (IC95% 1,33–1,49), alvo ampliado (D1). A direção do efeito se mantém no alvo conservador (limite inferior) e no máximo, mas as contagens absolutas diferem muito (média de 1,30 × 8,39 × 8,62 bugs por release). Associação significativa por projeto em 19 de 34. Associação, não causalidade. Antes da D2 (com HTTPCORE): IRR 1,40, MAE 6,63. |
| Tempo de correção | Primeira correção Fixed datada em 61,4% dos 114.556 bugs, com mediana de 5,75 dias; 17.463 encerrados sem correção |
| H2 (logística multinomial + efeito de projeto; teste 2024–2025) | F1 macro de 0,29 contra 0,23 do baseline; acurácia de 0,53 contra 0,46. **Desempenho modesto.** O modelo quase não prevê as duas faixas intermediárias (F1 de 0,004 e 0), e a previsão em quatro faixas **não** é sustentada. Com a D8 aplicada (9 projetos e 10.720 bugs a mais no treino; teste idêntico), as métricas não mudaram. Os modelos individuais (22 projetos, exploratórios) superaram o conjunto em só 6. |
| Retrabalho (exploratório, descritivo) | 5,2% dos bugs fechados foram reabertos; estabilidade de 95,5% em 90 dias. Não há modelo de reabertura. |
| Esforço | 99,84% dos worklogs são automáticos, então as horas **não** medem esforço |

## Prevenção de vazamento de informação

- **Estado em T0:** os modelos usam só o que era conhecido no instante da previsão. O changelog reconstrói a prioridade e o responsável na abertura, os componentes e o Affects Version na criação, e a composição da release na data de publicação.
- **Validação:** o treino e o teste são **cronológicos** (treino em 2020–2023, teste a partir de 2024), com o horizonte do desfecho completamente observado.
- **Testes automáticos:** `tests/` verifica a ausência de variáveis de estado final e o respeito à cronologia.

## Limitações

**Dos modelos:**
- **H1 (Binomial Negativa):**
  - **Causalidade:** os resultados são associações, não causas.
  - **Heterogeneidade:** a significância varia entre projetos (19 de 34 com associação significativa).
  - **Dependência do campo:** as contagens dependem do nível de evidência do Affects Version (médias de 1,30 / 8,39 / 8,62 bugs por release).
  - **Validação:** foi feita com uma única divisão cronológica (teste 2024–2026), restrita a 48 projetos verificáveis e não modulares.
- **H2 (logística multinomial):**
  - **Desempenho:** é modesto (F1 macro de 0,29 contra 0,23 do baseline).
  - **Faixas intermediárias:** praticamente não são previstas (8–30 d e 31–90 d). A previsão em quatro faixas **não** é sustentada com os atributos disponíveis na abertura do bug.
  - **Validação:** foi feita com uma única divisão cronológica (teste 2024–2025).
- **Sem modelo de reabertura:** a reabertura é analisada só de forma descritiva.

**Dos dados:**
- **Affects Version:** é opcional e heterogêneo entre projetos. A presença "desde a criação" é inferida, e versões excluídas no Jira somem das issues sem registro.
- **Releases:** `releaseDate` não está demonstrada como data real de publicação.
- **Campos ausentes:** não há severidade nem causa raiz estruturadas, e prioridade ≠ severidade.
- **Censura:** é tratada por horizonte fixo; a análise de sobrevivência não consta dos materiais do MBA.
- **Projetos com série interrompida:** 26 projetos, como ARROW e BEAM, param de registrar bugs no Jira.
- **Decisões metodológicas:** as decisões D1–D8 foram aprovadas e estão registradas em [`docs/decisoes_metodologicas.md`](docs/decisoes_metodologicas.md), com o status de implementação de cada uma.
- **Ajustes aplicados:** D2 (H1) e D8 (H2), com comparação antes × depois no notebook. As tabelas da versão anterior estão em `resultados/tabelas/versao_anterior_852b9c9/`.
- **Ainda não executado:** as sensibilidades da H1 em 90 d, a estabilidade sem reaberturas rápidas, a sinalização de lotes, a exclusão do treino dos projetos com série interrompida e as releases de 2019 (opcional).

## Reprodutibilidade

Os resultados do notebook correspondem ao snapshot de 25/10/2026, identificado pelo `resultados/coleta/manifest.json`. Para reproduzi-los exatamente é necessário esse snapshot; uma nova coleta produz números próximos, mas não idênticos. Ambiente testado: Windows 11, Python 3.13 (versões em [`docs/reproducao.md`](docs/reproducao.md)).
