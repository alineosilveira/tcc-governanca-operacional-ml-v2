# Linhagem dos dados

Fluxo: **API Apache Jira → snapshot JSONL → projeção compacta → regras validadas → bases analíticas → notebook → resultados**.

Todos os caminhos são configuráveis por variáveis de ambiente (ver `.env.example`):
- `ALINE_JIRA_DATA_DIR`: snapshot.
- `ALINE_CACHE_DIR`: cache compacto.
- `ALINE_EVIDENCIAS_DIR`: evidências agregadas.
- `ALINE_BASES_DIR`: bases linha a linha.

Somente o código, os resultados agregados e os gráficos são versionados. O motivo está em `reproducao.md`.

## 1. Coleta e integridade

| Fonte | Script | Transformação | Saída | Uso no notebook |
|---|---|---|---|---|
| API REST v2 de `https://issues.apache.org/jira` (anônima, só GET) | `src/coleta/apache_jira_extract.py` | Inspeção (serverInfo, projetos, campos); plano de 50 janelas disjuntas de `created`; busca paginada (`maxResults=1000`, `fields=*all`, `expand=changelog`); complemento de worklogs/comentários truncados; versões por projeto; consolidação e deduplicação por id | `ALINE_JIRA_DATA_DIR/`: `projects.jsonl`, `fields.json`, `issues.jsonl`, `changelog.jsonl`, `comments.jsonl`, `worklogs.jsonl`, `versions.jsonl`, `issue_versions.jsonl`, `manifest.json`, `errors.jsonl`, `metrics.jsonl` | Cap. 2 (cópia de `manifest.json` em `resultados/coleta/`) |
| Snapshot JSONL | `src/coleta/quality_report.py` | Leitura em streaming; cobertura de campos; totais informados pela API × gravados | `data_quality_report.md` | Cap. 2 (cópia em `resultados/coleta/`) |

## 2. Preparação

| Entrada | Script | Transformação | Saída | Uso |
|---|---|---|---|---|
| `issues.jsonl`, `changelog.jsonl`, `worklogs.jsonl`, `comments.jsonl` | `src/preparacao/01_projetar_base.py` | Uma passagem em streaming. Projeção de ~45 atributos por issue; itens de changelog apenas de campos relevantes (status, resolution, priority, assignee, Fix Version, Version, Component, Link, Project, Key…); pessoas substituídas por hash SHA-256 com sal local | `ALINE_CACHE_DIR/issues_c.csv`, `changelog_c.csv`, `worklogs_c.csv`, `comments_c.csv`, `.salt` | Insumo de 03–07 |
| cache + `versions.jsonl` + `issue_versions.jsonl` | `src/preparacao/05_validar_regras_negocio.py --bases` | Regras validadas: associação por Affects Version (classes A/B/C/D), B1/B2/B3, reabertura por categoria de status, ciclos, estabilidade 30/90 d | **Bases B, C, D, E**: `base_releases.csv`, `base_bug_release.csv`, `base_bugs_ciclos.csv`, `base_reaberturas.csv`; evidências `regras_*_por_projeto.csv` | Cap. 5, 6, 7 |
| cache + `versions.jsonl` + `regras_releases_bugs_por_projeto.csv` | `src/preparacao/06_validar_pendencias.py --bases` | Reconstrução reversa de Affects Version; níveis de evidência; cortes temporais; concordância status × Resolution; reaberturas rápidas | `base_vinculos_evidencia.csv`, `base_reaberturas_rapidas.csv`, `base_reaberturas_corroboracao.csv`; evidências `pendencia_*.csv` | Cap. 5, 7 |
| cache + bases de 05/06 + evidências de 04/05 | `src/preparacao/07_bases_modelagem.py` | Features em T0 e alvo com horizonte fixo; split cronológico | `modelo_bugs_faixa.csv`, `modelo_releases.csv` | Cap. 9 |

## 3. Diagnóstico por projeto (evidências agregadas)

| Entrada | Script | Saída | Uso |
|---|---|---|---|
| cache + `versions.jsonl` + `sprints.jsonl` | `src/analise/03_diagnostico_cobertura.py` | Cobertura, períodos, tipos por ano, worklogs automáticos × demais, campos de criticidade (`base_issues_por_ano_criacao.csv`, `obj4_*`, `obj5_*`, `resumo_metricas.json`…) | Cap. 4, 8 |
| cache + evidências de 03 | `src/analise/04_caracterizacao_por_projeto.py` | **Base A**: `projetos_caracterizacao.csv` (1 linha por projeto); `projetos_viabilidade_modelos.csv`; `heterogeneidade_entre_projetos.csv` | Cap. 4, 9 |
| Materiais de aula (privados) | `src/analise/02_auditar_mba.py` | Ocorrências de técnicas por arquivo/página (não publicadas). A síntese manual está em `docs/metodologia.md`. | Cap. 9 (escolha das técnicas) |

O script 03 também produz evidências de sprints, mas elas estão **fora do escopo atual** e não são usadas no notebook.

## 4. Base F (demandas por tipo)

É derivada no notebook (Cap. 8) a partir de `obj4_tipos_issue_por_ano.csv` (03) e `projetos_caracterizacao.csv` (04). É um agregado por projeto × ano × tipo.

## 5. Ordem de execução

`01 → 03 → 04 → 05 → 06 → 07 → notebook`

O 02 é independente. Os comandos estão em `reproducao.md`.
