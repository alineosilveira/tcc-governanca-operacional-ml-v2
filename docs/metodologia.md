# Metodologia

## 1. Coleta (`src/coleta/apache_jira_extract.py`)

Os parâmetros abaixo são os efetivamente usados, conforme `resultados/coleta/manifest.json`.

| Aspecto | Implementação |
|---|---|
| Fonte | `https://issues.apache.org/jira` (Jira Server 10.3.26), REST API v2 (documentação Jira Data Center REST v11002) |
| Acesso | Anônimo, somente `GET`; nenhuma credencial |
| Critério temporal (JQL) | `created >= "2020-01-01" OR updated >= "2020-01-01" OR resolution IS EMPTY` |
| Planejamento | 50 janelas **disjuntas** de `created` (≤ 20.000 issues cada); a soma das janelas foi igual ao total global (561.363 no plano) |
| Paginação | `/rest/api/2/search` com `maxResults=1000`. É o limite real: o servidor devolve no máximo 1000, mesmo pedindo 5000. Uso de `fields=*all` e `expand=changelog`, com `ORDER BY created ASC, key ASC`. Foram 587 páginas. |
| Campos personalizados | Todos preservados (`*all`); o catálogo de 215 campos (173 customizados) está em `fields.json` |
| Changelog | Completo na própria busca: 6.464.445 históricos, igual ao total informado pela API, sem truncamento. O endpoint `/issue/{key}/changelog` não existe nesta versão (HTTP 404). |
| Comentários e worklogs | Vêm na busca (comentários até 1000 por issue; worklogs até 20). Os 9.203 casos truncados foram completados por `/issue/{id}/worklog` e `/issue/{id}/comment`, sem nenhum faltante. |
| Versões | `/rest/api/2/project/{key}/version`, paginado, para os 674 projetos (23.837 versões) |
| Retentativas | Backoff exponencial com jitter (base 2 s, teto 120 s, até 8 tentativas); respeita `Retry-After`; não repete 4xx permanentes; timeouts de 20 s (conexão) e 180 s (leitura); páginas grandes que falham repetidamente são reduzidas até 100 itens |
| Concorrência | Limitador global AIMD: começa em 4, sobe 1 a cada 30 sucessos até 8 e cai pela metade em 429/503/timeout/5xx; no máximo 8 requisições por segundo |
| Retomada | Checkpoint por página (`state/checkpoint.json`, com offsets de bytes dos arquivos parciais e `fsync`); os parciais são truncados ao último checkpoint na retomada. A retomada foi efetivamente exercida uma vez durante a coleta. |
| Duplicidades | Reconciliação por janela (ids únicos × contagem refeita: 50 de 50 coincidentes) e deduplicação final por **id** da issue. Resultado: 0 duplicatas. |
| Data da coleta | 25/10/2026, das 20:22 às 21:57 UTC; 561.369 issues; status `complete` |
| Limitações do acesso anônimo | Agile API (`/rest/agile/1.0/board`) → HTTP 401, sem boards e sprints; `/worklog/updated` → 401; issues e comentários restritos e projetos arquivados não são visíveis |

## 2. Integridade (`src/coleta/quality_report.py` e o próprio coletor)

- **Manifesto:** registra plano, páginas, contagens por unidade, sondagens e estado de conclusão.
- **Totais da API × gravados:** changelog, comentários e worklogs foram conferidos. A única diferença é de 3 worklogs com visibilidade restrita.
- **Erros:** `errors.jsonl` registra cada falha. Na execução foram 34 erros transitórios (desconexões e timeouts), todos resolvidos na retentativa, além dos 401/404 esperados das sondagens.

## 3. Preparação

1. **Projeção** (`01_projetar_base.py`): uma única passagem em streaming pelos JSONL, gerando CSVs compactos. Pessoas (assignee, reporter, autores) são substituídas por hash SHA-256 truncado, com sal local.
2. **Tipagem e datas:** todas as datas são lidas como UTC (ISO 8601). Datas de criação anteriores a 2000 (2 casos importados, ano 0010) são inválidas e excluídas.
3. **Valores ausentes:** ausência de campo significa "sem dado", nunca zero (ex.: issue sem worklog, release sem bug vinculado). Os percentuais de preenchimento são reportados por projeto.
4. **Relacionamentos:**
   - **Bug × versão:** pelo ID de versão (`fields.versions[].id`), verificado contra `issue_versions.jsonl`, com 100% de coincidência e nenhum vínculo a outro projeto.
   - **Histórico:** vem do changelog (status, resolution, priority, assignee, Fix Version, Version, Component, Link, Project/Key).
5. **Regras validadas** (`05_validar_regras_negocio.py` e `06_validar_pendencias.py`): ver `decisoes_metodologicas.md`.
6. **Bases de modelagem** (`07_bases_modelagem.py`): features em T0 e split cronológico.

## 4. Análises

- **Caracterização por projeto** (unidade primária) e **segunda camada consolidada.** A heterogeneidade é medida pelo η² do projeto (ANOVA de um fator, descritiva).
- **Estatística descritiva:** contagens, percentis, distribuições.
- **Inferência descritiva:** correlação de Spearman por projeto (tamanho da release × bugs) e teste de Kruskal-Wallis entre tipos de versão. São técnicas de associação; não implicam causalidade.
- **Modelagem** (Cap. 9):
  - **Modelo principal (D7):** um por problema, **conjunto**, ensinado no MBA e com efeito fixo de projeto, comparado a um baseline por projeto. Usa split cronológico e só variáveis disponíveis em T0.
  - **Modelos individuais:** são complementares e **exploratórios**, ajustados só quando há observações, classes, convergência e teste válido.
  - **Horizontes (D6):** 180 d (H1) e 90 d (faixas da H2), com acompanhamento completo.
- **Reabertura:** permanece **exploratória e descritiva**; não há modelo preditivo de reabertura nesta versão.

## 5. Decisões metodológicas

As decisões D1–D8 foram aprovadas e estão registradas em `decisoes_metodologicas.md`, com o status de implementação de cada uma. Duas diferenças entre o aprovado e o executado estão declaradas lá, e não foram recalculadas nesta versão:
- **D2:** o limite de 10% de vínculos indeterminados ainda não foi aplicado e excluiria HTTPCORE da H1.
- **D8:** na H2, os projetos sem observações de teste também ficaram fora do treino.

### Técnicas do MBA utilizadas

A seleção foi feita a partir da auditoria dos materiais de aula (`src/analise/02_auditar_mba.py`). Os materiais não são publicados.

| Técnica | Situação nos materiais | Uso nesta versão |
|---|---|---|
| Estatística descritiva, testes de hipóteses, correlação | Ensinada e comprovada (Fundamentos de Estatística) | Cap. 4–8 |
| Regressão logística binária/multinomial, matriz de confusão, ROC | Ensinada e comprovada (Supervised ML – Modelos Logísticos) | Cap. 9.1 (multinomial) |
| Poisson, Binomial Negativa, modelos inflacionados de zeros | Ensinada e comprovada (Supervised ML – Dados de Contagem) | Cap. 9.2 (Binomial Negativa) |
| Modelagem multinível / dummies de efeito fixo | Ensinada e comprovada (Supervised ML – Multinível; Regressão) | Efeito fixo de projeto nos modelos |
| Divisão treino/teste; holdout temporal em séries temporais; MAE/RMSE | Ensinada e comprovada | Split cronológico; métricas |
| Árvores, Random Forest, Boosting | Ensinadas e comprovadas | Não usadas nesta versão (possibilidade futura) |
| Validação temporal para ML (TimeSeriesSplit), balanceamento de classes, importância de variáveis | Mencionadas, sem conteúdo suficiente | Não usadas |
| Análise de sobrevivência, SHAP/LIME | Não encontradas nos materiais examinados | Não usadas (abertos tratados com horizonte fixo) |
