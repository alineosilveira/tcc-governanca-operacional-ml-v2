# Relatório de qualidade de dados — Apache Jira (extração pública)

- Base: `https://issues.apache.org/jira` — servidor 10.3.26 (Server)
- Extração iniciada (UTC): 2026-10-25T20:22:57Z; manifesto: 2026-10-25T21:57:01Z
- Estado de conclusão: **complete**
- JQL global: `created >= "2020-01-01" OR updated >= "2020-01-01" OR resolution IS EMPTY`

## 1. Volume

| Item | Valor |
|---|---|
| Projetos no inventário (`/project`) | 674 |
| Projetos arquivados retornados | 0 |
| Projetos com issues no recorte | 650 |
| Projetos presentes nos issues mas ausentes do inventário | 0 [] |
| Issues únicas | 561369 |
| Total da JQL no planejamento / ao final | 561363 / 561369 |
| Registros duplicados removidos (mesmo id) | 0 |
| Unidades (janelas) concluídas | 50/50; falhas: [] |
| Páginas de busca processadas | 587 |

Issues por ano de criação: 0010: 2, 2001: 49, 2002: 287, 2003: 595, 2004: 1144, 2005: 3725, 2006: 5529, 2007: 5905, 2008: 6879, 2009: 7360, 2010: 7861, 2011: 9287, 2012: 9923, 2013: 11140, 2014: 15722, 2015: 21421, 2016: 26843, 2017: 29994, 2018: 34889, 2019: 39119, 2020: 63770, 2021: 57837, 2022: 53139, 2023: 42293, 2024: 38440, 2025: 32983, 2026: 35233

## 2. Cobertura de preenchimento (campos padrão)

| Campo | Issues preenchidas | % |
|---|---|---|
| duedate | 3526 | 0.6% |
| resolution | 371132 | 66.1% |
| resolutiondate | 371192 | 66.1% |
| priority | 559647 | 99.7% |
| assignee | 341024 | 60.7% |
| fixVersions | 303645 | 54.1% |
| versions | 245994 | 43.8% |
| components | 386553 | 68.9% |
| labels | 167501 | 29.8% |
| environment | 47111 | 8.4% |
| timeoriginalestimate | 8849 | 1.6% |
| timespent | 89195 | 15.9% |
| issuelinks | 134276 | 23.9% |
| parent | 66627 | 11.9% |

> `duedate` vazio **não** permite classificar a issue como em dia/atrasada; nenhuma inferência de prazo foi feita.

## 3. Campos customizados relevantes encontrados

Classificação por **nome** do campo (heurística); o significado real depende de cada projeto e deve ser validado.

### estimativa/story_points

| id | nome | tipo | issues preenchidas | % |
|---|---|---|---|---|
| customfield_12310060 | Estimated Complexity | option | 14160 | 2.5% |
| customfield_12314523 | Original story points | number | 0 | 0.0% |
| customfield_12310293 | Story Points | number | 2561 | 0.5% |
| customfield_12313821 | Complexity | option | 5791 | 1.0% |
| customfield_12310227 | Level of effort | string | 9 | 0.0% |
| customfield_12314127 | Level of effort | string | 0 | 0.0% |
| customfield_12314121 | Estimated Complexity | option | 0 | 0.0% |

### causa_raiz

| id | nome | tipo | issues preenchidas | % |
|---|---|---|---|---|
| customfield_12313825 | Bug Category | option-with-child | 2926 | 0.5% |
| customfield_12310200 | Bug behavior facts | array | 415 | 0.1% |
| customfield_12314125 | Bug behavior facts | array | 0 | 0.0% |

### ambiente/producao

| id | nome | tipo | issues preenchidas | % |
|---|---|---|---|---|
| customfield_12313921 | Platform | array | 6522 | 1.2% |
| customfield_12310228 | O/S Version | string | 8 | 0.0% |
| customfield_12310223 | Browser Version | string | 8 | 0.0% |
| customfield_12310226 | JDK Version | string | 8 | 0.0% |

### versao

| id | nome | tipo | issues preenchidas | % |
|---|---|---|---|---|
| customfield_12310271 | Backport to Version | array | 25 | 0.0% |
| customfield_12310192 | Release Note | string | 5198 | 0.9% |
| customfield_12312341 | INFRA - Subversion Repository Path | string | 0 | 0.0% |
| customfield_12310172 | Fix version (Component) | option-with-child | 7 | 0.0% |
| customfield_12310171 | Affects version (Component) | option-with-child | 30 | 0.0% |
| customfield_12310300 | Release Version History | version | 0 | 0.0% |
| customfield_12312821 | Target Version | array | 4582 | 0.8% |
| customfield_12314145 | Affects version (Component) | option-with-child | 0 | 0.0% |
| customfield_12314144 | Backport to Version | array | 0 | 0.0% |
| customfield_12314143 | Fix version (Component) | option-with-child | 0 | 0.0% |
| customfield_12310228 | O/S Version | string | 8 | 0.0% |
| customfield_12310223 | Browser Version | string | 8 | 0.0% |
| customfield_12310226 | JDK Version | string | 8 | 0.0% |
| customfield_12314126 | Target Version/s | array | 1565 | 0.3% |
| customfield_12310320 | Target Version/s | array | 14841 | 2.6% |
| customfield_12311420 | Since Version | version | 2231 | 0.4% |
| customfield_12314136 | Since Version | version | 80 | 0.0% |

### sprint/agile

| id | nome | tipo | issues preenchidas | % |
|---|---|---|---|---|
| customfield_12311123 | Epic Colour | string | 1279 | 0.2% |
| customfield_12311121 | Epic Name | string | 1503 | 0.3% |
| customfield_12311122 | Epic Status | option | 1327 | 0.2% |
| customfield_12311120 | Epic Link | any | 14903 | 2.7% |
| customfield_12310921 | Sprint | array | 8356 | 1.5% |
| customfield_12310920 | Rank (Obsolete) | any | 561369 | 100.0% |
| customfield_12314524 | Team | any | 0 | 0.0% |
| customfield_12310291 | Epic/Theme | array | 1 | 0.0% |
| customfield_12311820 | Rank | any | 561369 | 100.0% |
| customfield_12310420 | Global Rank | any | 561369 | 100.0% |
| customfield_12312822 | Epic Color | string | 7855 | 1.4% |

### severidade/criticidade

| id | nome | tipo | issues preenchidas | % |
|---|---|---|---|---|
| customfield_12310250 | Flags | array | 7738 | 1.4% |
| customfield_12311036 | Severity | option | 0 | 0.0% |
| customfield_12311031 | Severity | option | 0 | 0.0% |
| customfield_12311032 | Priority | option | 0 | 0.0% |
| customfield_12311037 | Priority | option | 0 | 0.0% |
| customfield_12310191 | Hadoop Flags | array | 9388 | 1.7% |
| customfield_10023 | Fix priority | option | 19 | 0.0% |
| customfield_12310160 | Severity | option | 233 | 0.0% |
| customfield_12310290 | Flagged | array | 15 | 0.0% |
| customfield_12311022 | Priority | option | 44 | 0.0% |
| customfield_12311021 | Severity | option | 57 | 0.0% |
| customfield_12311026 | Severity | option | 0 | 0.0% |
| customfield_12311027 | Priority | option | 0 | 0.0% |
| customfield_12313820 | Severity | option | 6608 | 1.2% |
| customfield_12310080 | Regression | array | 128 | 0.0% |
| customfield_12313922 | Impacts | array | 6573 | 1.2% |
| customfield_12314140 | Ignite Flags | array | 0 | 0.0% |
| customfield_12313620 | Ignite Flags | array | 7834 | 1.4% |
| customfield_12314120 | Regression | array | 0 | 0.0% |
| customfield_12314134 | Hadoop Flags | array | 0 | 0.0% |

### datas_planejadas

| id | nome | tipo | issues preenchidas | % |
|---|---|---|---|---|
| customfield_12314422 | Start Date | date | 21 | 0.0% |
| customfield_12314521 | Target start | date | 0 | 0.0% |
| customfield_12312521 | Last public comment date | any | 561369 | 100.0% |
| customfield_12314129 | Review Date | date | 0 | 0.0% |

### qa/teste

| id | nome | tipo | issues preenchidas | % |
|---|---|---|---|---|
| customfield_12313422 | Enable Automatic Patch Review | string | 561369 | 100.0% |
| customfield_12311124 | Tester | user | 86 | 0.0% |
| customfield_12313420 | Reviewers | array | 7273 | 1.3% |
| customfield_12312421 | Code Review | string | 111 | 0.0% |
| customfield_12313520 | Review Patch? | array | 32 | 0.0% |
| customfield_10022 | Reviewer | user | 7012 | 1.2% |
| customfield_12312220 | Testcase included | option | 1203 | 0.2% |
| customfield_12314220 | Testers | array | 4 | 0.0% |
| customfield_12313823 | Test and Documentation Plan | string | 4660 | 0.8% |
| customfield_12314141 | Reviewers | array | 0 | 0.0% |
| customfield_12314129 | Review Date | date | 0 | 0.0% |
| customfield_12314135 | Reviewer | user | 0 | 0.0% |
| customfield_12314139 | Tester | user | 0 | 0.0% |

### pessoas

| id | nome | tipo | issues preenchidas | % |
|---|---|---|---|---|
| customfield_12314620 | potential-mentor | array | 27 | 0.0% |
| customfield_12311124 | Tester | user | 86 | 0.0% |
| customfield_12313420 | Reviewers | array | 7273 | 1.3% |
| customfield_12314420 | Mentor | user | 135 | 0.0% |
| customfield_10022 | Reviewer | user | 7012 | 1.2% |
| customfield_12314220 | Testers | array | 4 | 0.0% |
| customfield_12312026 | Initial Confluence Contributors | string | 0 | 0.0% |
| customfield_12311620 | Shepherd | user | 1631 | 0.3% |
| customfield_12314141 | Reviewers | array | 0 | 0.0% |
| customfield_12314135 | Reviewer | user | 0 | 0.0% |
| customfield_12314139 | Tester | user | 0 | 0.0% |

### Todos os campos customizados com algum preenchimento (top 60)

| id | nome | issues | % |
|---|---|---|---|
| customfield_12310420 | Global Rank | 561369 | 100.0% |
| customfield_12313422 | Enable Automatic Patch Review | 561369 | 100.0% |
| customfield_12310310 | Attachment count | 561369 | 100.0% |
| customfield_12310920 | Rank (Obsolete) | 561369 | 100.0% |
| customfield_12314020 | Development | 561369 | 100.0% |
| customfield_12312521 | Last public comment date | 561369 | 100.0% |
| customfield_12311820 | Rank | 561369 | 100.0% |
| customfield_12311020 | External issue URL | 20812 | 3.7% |
| customfield_12311120 | Epic Link | 14903 | 2.7% |
| customfield_12310320 | Target Version/s | 14841 | 2.6% |
| customfield_12310060 | Estimated Complexity | 14160 | 2.5% |
| customfield_12313320 | Lucene Mailing List Info | 10685 | 1.9% |
| customfield_12310120 | Lucene Fields | 9759 | 1.7% |
| customfield_12310191 | Hadoop Flags | 9388 | 1.7% |
| customfield_12313321 | Solr Mailing List Info | 8804 | 1.6% |
| customfield_12310921 | Sprint | 8356 | 1.5% |
| customfield_12312822 | Epic Color | 7855 | 1.4% |
| customfield_12313620 | Ignite Flags | 7834 | 1.4% |
| customfield_12310250 | Flags | 7738 | 1.4% |
| customfield_12313920 | Authors | 7563 | 1.3% |
| customfield_12313420 | Reviewers | 7273 | 1.3% |
| customfield_10022 | Reviewer | 7012 | 1.2% |
| customfield_12313820 | Severity | 6608 | 1.2% |
| customfield_12313922 | Impacts | 6573 | 1.2% |
| customfield_12313921 | Platform | 6522 | 1.2% |
| customfield_12313821 | Complexity | 5791 | 1.0% |
| customfield_12310192 | Release Note | 5198 | 0.9% |
| customfield_12313823 | Test and Documentation Plan | 4660 | 0.8% |
| customfield_12312821 | Target Version | 4582 | 0.8% |
| customfield_12313924 | Source Control Link | 4314 | 0.8% |
| customfield_12314421 | Language | 3818 | 0.7% |
| customfield_12313825 | Bug Category | 2926 | 0.5% |
| customfield_12313822 | Discovered By | 2849 | 0.5% |
| customfield_12313826 | Change Category | 2812 | 0.5% |
| customfield_12310293 | Story Points | 2561 | 0.5% |
| customfield_12311420 | Since Version | 2231 | 0.4% |
| customfield_12311620 | Shepherd | 1631 | 0.3% |
| customfield_12314126 | Target Version/s | 1565 | 0.3% |
| customfield_10010 | Bugzilla Id | 1509 | 0.3% |
| customfield_12311121 | Epic Name | 1503 | 0.3% |
| customfield_12311122 | Epic Status | 1327 | 0.2% |
| customfield_12310041 | Patch Info | 1288 | 0.2% |
| customfield_12311123 | Epic Colour | 1279 | 0.2% |
| customfield_12314320 | Detailed Description | 1226 | 0.2% |
| customfield_12312220 | Testcase included | 1203 | 0.2% |
| customfield_12311024 | External issue ID | 1096 | 0.2% |
| customfield_12310050 | Urgency | 1090 | 0.2% |
| customfield_12313020 | Mailing List | 871 | 0.2% |
| customfield_12310230 | Tags | 719 | 0.1% |
| customfield_12311421 | Reproduced In | 690 | 0.1% |
| customfield_12312720 | Docs Text | 583 | 0.1% |
| customfield_12310200 | Bug behavior facts | 415 | 0.1% |
| customfield_12314621 | difficulty-level | 373 | 0.1% |
| customfield_12310106 | Old Scarab Id | 347 | 0.1% |
| customfield_12310090 | Issue & fix info | 337 | 0.1% |
| customfield_12311034 | External issue ID | 290 | 0.1% |
| customfield_12310160 | Severity | 233 | 0.0% |
| customfield_12310150 | Bugtraq ID | 158 | 0.0% |
| customfield_12314420 | Mentor | 135 | 0.0% |
| customfield_12310051 | Other Info | 129 | 0.0% |

Campos customizados no catálogo: 173; com ≥1 valor no recorte: 118.

## 4. Changelog, comentários e worklogs

| Conjunto | Issues com dados | Registros (total informado pela API) | Registros gravados | Issues truncadas na busca (completadas por endpoint dedicado) |
|---|---|---|---|---|
| Changelog (históricos) | 524684 (93.5%) | 6464445 | 6464445 | 0 |
| Comentários | 413078 (73.6%) | 1991188 | 1991188 | 3 |
| Worklogs | 86244 (15.4%) | 843978 | 843975 | 9200 |

Diferença de 3 worklogs (843.978 informados × 843.975 gravados): em TAVERNA-138 (2→1), HIVE-16674 (1→0) e KAFKA-13349 (4→3) o `total` da busca inclui worklogs que nem a busca nem `/issue/{id}/worklog` devolvem ao acesso anônimo (visibilidade restrita). Não é falha de coleta.

Dados associados faltantes após retentativas: {'changelog': 0, 'comments': 0, 'worklogs': 0}; incompletos: {'changelog': 0, 'comments': 0, 'worklogs': 0}.

Worklogs: 157034.0 horas registradas por 175 autores distintos. Issues **sem worklog = sem dado disponível**, não zero horas trabalhadas; o registro de worklog é raro e opcional na ASF (apenas 15.4% das issues).

Issues atualmente no status 'Reopened': 3539. Reaberturas históricas devem ser medidas pelas transições de status em `changelog.jsonl` (o nome do status de reabertura varia por workflow).

## 5. Versões, sprints e boards

- `versions.jsonl`: 23837 versões de 674 projetos (`/project/{key}/version`). Não-200: {}
- `issue_versions.jsonl`: associação issue → fixVersions/versions (extraída dos campos do issue).
- Agile API (`/rest/agile/1.0/board`): HTTP 401 — INDISPONÍVEL para acesso anônimo; boards/sprints não foram listados pela API.
- `sprints.jsonl`: 523 sprints **derivados** do valor bruto do campo `Sprint` nos issues; `issue_sprints.jsonl`: 13216 associações; `boards.jsonl`: ids de board (`rapidViewId`) derivados, sem nome. Sprints sem nenhuma issue no recorte não aparecem.

## 6. Endpoints indisponíveis, erros e limites observados

- `maxResults` solicitado 5000 → servidor devolveu `maxResults=1000` (limite real por página).
- `expand=changelog` na busca retornou histórico completo (total = obtido) na grande maioria; truncamentos: 0.
- Campo `comment` na busca: até 1000 por issue; campo `worklog`: no máximo 20 por issue (complementado via `/issue/{id}/worklog`).
- `/rest/agile/1.0/board`: HTTP 401; `/worklog/updated`: HTTP 401; `/issue/{key}/changelog`: HTTP 404 (não existe nesta versão do servidor).
- Projetos arquivados: `/project?includeArchived=true` não retornou nenhum projeto arquivado para acesso anônimo; issues de projetos não listados aparecem acima se existirem.
- Campos restritos/privados (issues com security level, comentários restritos) não são visíveis anonimamente e não foram coletados.

| fase | endpoint | status | retentado | ocorrências |
|---|---|---|---|---|
| extras | /rest/api/2 | None | True | 25 |
| issues | /rest/api/2/search | None | True | 8 |
| inspect | /rest/agile/1.0/board | 401 | False | 1 |
| inspect | /rest/api/2/worklog/updated | 401 | False | 1 |
| inspect | /rest/api/2/issue/AAR-1/changelog | 404 | False | 1 |
| versions | /rest/api/2/project/OLIO/version | None | True | 1 |
| boards | /rest/agile/1.0/board | 401 | False | 1 |

## 7. Cautelas de interpretação

- **Incidente de produção**: não há campo padrão; tipo `Bug`, devolução por QA ou existência de `fixVersion` **não** caracterizam incidente de produção. Campos como `Environment`, `Severity`, `Regression`, `Bug Category`, `Flags` existem em poucos projetos e com convenções próprias.
- **Causa raiz**: não há campo de causa raiz amplamente usado; comentários foram guardados como texto bruto e não foram classificados.
- **Criticidade**: `priority` é padrão, mas os esquemas de prioridade (Blocker/Critical/Major… ou P0–P4) variam por projeto; existem vários campos `Severity` distintos (ids diferentes) por projeto.
- **Sprint/estimativa**: o campo `Sprint` e `Story Points` são usados por poucos projetos; ausência ≠ zero.
- **Pessoas**: assignee não é o único recurso envolvido — considere reporter, autores de comentários, autores do changelog, autores de worklog e campos como Tester/Reviewer.
- **Prazos**: só issues com `duedate` permitem avaliar atraso; não houve inferência.
- Todos os significados acima dependem de convenções específicas de cada projeto e precisam ser validados antes de interpretar.

## 8. Tipos de issue e status por projeto

Tipos globais: Bug: 224319, Improvement: 164219, Sub-task: 66076, Task: 41806, New Feature: 36516, Test: 7521, Dependency upgrade: 7437, Wish: 4677, Epic: 1609, Documentation: 1437, Story: 1230, Technical Debt: 1212, Question: 1197, Umbrella: 753, Technical task: 691, Dependency: 191, Brainstorming: 166, Suitable Name Search: 103, Request: 94, IT Help: 22, Project: 18, Proposal: 15, TCK Challenge: 13, Temp: 7, New JIRA Project: 6, Planned Work: 6, Github Integration: 5, Comment: 4, Blog - New Blog Request: 3, Outage: 3, Requirement: 3, RTC: 3, Access: 2, SVN->GIT Migration: 1, Choose from below ...: 1, New Git Repo: 1, Blogs - Access to Existing Blog: 1, Blogs - New Blog User Account Request: 1

Status globais: Resolved: 193897, Closed: 177350, Open: 166943, In Progress: 6652, Patch Available: 6541, Reopened: 3539, To Do: 2405, Triage Needed: 2080, Accepted: 856, Done: 537, Reviewable: 250, In Review: 67, Review In Progress: 49, WontFix: 40, Awaiting Feedback: 32, Needs Committer: 27, Changes Suggested: 23, Continued: 18, For Review: 18, Blocked: 12, Ready to Commit: 10, Started: 9, Unknown: 4, on hold: 4, Verified: 2, In Tests: 2, Requires Porting: 1, Idea: 1

| projeto | issues | criadas ≥2020 | % duedate | % resolução | % assignee | % fixVersion | tipos | status |
|---|---|---|---|---|---|---|---|---|
| SPARK | 41700 | 30092 | 0.1% | 85.0% | 72.6% | 72.0% | Sub-task 13873; Improvement 11542; Bug 11048; New Feature 1518; Task 1098; Test 1043; Documentation 495; Umbrella 408; Question 251; Dependency upgrade 127; Story 111; Wish 78; Epic 63; Brainstorming 15; IT Help 9; Request 8; Planned Work 4; Github Integration 3; RTC 3; New JIRA Project 2; Blog - New Blog Request 1 | Closed 18419; Resolved 17035; Open 4903; In Progress 1217; Reopened 126 |
| FLINK | 29982 | 25717 | 0.2% | 74.5% | 62.0% | 57.1% | Bug 10693; Improvement 8981; Sub-task 7180; New Feature 1921; Technical Debt 1207 | Closed 16972; Open 6898; Resolved 5375; Reopened 463; In Progress 274 |
| IGNITE | 20376 | 16656 | 0.1% | 68.2% | 70.3% | 52.1% | Improvement 8327; Bug 7017; Task 2937; Sub-task 863; New Feature 650; Test 299; Epic 236; Wish 47 | Resolved 13393; Open 6010; Closed 506; In Progress 233; Patch Available 181; Reopened 53 |
| ARROW | 18289 | 10895 | 0.1% | 84.5% | 72.2% | 72.0% | Improvement 7786; Bug 6045; New Feature 1940; Sub-task 1237; Task 928; Wish 228; Test 125 | Resolved 12544; Closed 2910; Open 2686; In Progress 136; Reopened 13 |
| HBASE | 17616 | 6849 | 0.6% | 84.1% | 61.4% | 48.9% | Bug 6300; Improvement 4233; Sub-task 3721; Task 1709; New Feature 834; Test 376; Umbrella 274; Brainstorming 110; Wish 59 | Resolved 7449; Closed 7360; Open 2362; Patch Available 258; In Progress 140; Reopened 47 |
| HIVE | 16250 | 7338 | 1.9% | 50.6% | 68.2% | 43.4% | Bug 7778; Improvement 4336; Sub-task 2341; Task 810; New Feature 650; Test 258; Wish 77 | Open 6829; Closed 5583; Resolved 2647; Patch Available 939; In Progress 186; Reopened 66 |
| HDDS | 15982 | 14601 | 0.1% | 82.2% | 85.2% | 60.8% | Sub-task 6659; Bug 4198; Improvement 3104; Task 1564; New Feature 272; Epic 94; Test 69; Wish 22 | Resolved 13044; Open 2578; Patch Available 129; In Progress 105; Closed 85; Reopened 41 |
| BEAM | 14550 | 5511 | 0.5% | 70.4% | 58.9% | 70.9% | Bug 6007; Improvement 3900; Sub-task 2255; New Feature 1351; Task 587; Test 313; Wish 137 | Resolved 9540; Open 4003; Triage Needed 902; In Progress 105 |
| KAFKA | 13695 | 10726 | 0.6% | 60.9% | 68.7% | 44.8% | Bug 5390; Improvement 3804; Sub-task 2634; Task 746; Test 582; New Feature 430; Wish 109 | Resolved 8153; Open 4641; Patch Available 352; In Progress 294; Closed 182; Reopened 73 |
| CAMEL | 12538 | 11939 | 0.0% | 93.9% | 72.3% | 88.3% | Improvement 4369; Bug 3748; Task 1582; New Feature 1403; Dependency upgrade 564; Test 522; Sub-task 278; Wish 72 | Resolved 11234; Open 654; Closed 544; In Progress 98; Reopened 8 |
| NIFI | 11767 | 9384 | 0.1% | 78.8% | 68.7% | 60.3% | Improvement 5282; Bug 3792; Sub-task 859; Task 845; New Feature 751; Wish 108; Test 71; Epic 59 | Resolved 9186; Open 2236; Patch Available 155; In Progress 89; Closed 87; Reopened 14 |
| LUCENE | 10629 | 1559 | 0.1% | 81.9% | 54.1% | 65.4% | Bug 4215; Improvement 4150; Task 919; New Feature 647; Sub-task 333; Test 231; Wish 134 | Closed 5889; Resolved 2439; Open 1763; Reopened 299; Patch Available 239 |
| CASSANDRA | 10318 | 6219 | 0.1% | 67.7% | 68.1% | 68.3% | Bug 5155; Improvement 3243; Task 927; New Feature 577; Sub-task 369; Epic 47 | Resolved 6985; Open 2041; Triage Needed 881; Patch Available 163; In Progress 128; Review In Progress 41; Awaiting Feedback 27; Needs Committer 26; Changes Suggested 22; Ready to Commit 4 |
| HUDI | 9598 | 9279 | 0.3% | 64.6% | 67.8% | 71.5% | Improvement 3247; Bug 2801; Task 1620; Sub-task 870; New Feature 691; Test 180; Epic 158; Wish 31 | Closed 5598; Open 2753; Resolved 947; In Progress 164; Patch Available 100; Reopened 36 |
| SOLR | 8804 | 4362 | 0.0% | 53.5% | 43.9% | 42.9% | Bug 3223; Improvement 2989; Sub-task 839; New Feature 694; Task 682; Test 275; Wish 102 | Open 3956; Closed 2854; Resolved 1857; Reopened 75; Patch Available 62 |
| IMPALA | 8718 | 6369 | 0.1% | 59.5% | 64.5% | 46.5% | Bug 3646; Improvement 2497; Sub-task 935; Task 633; New Feature 581; Documentation 144; Epic 115; Test 113; Dependency upgrade 19; Question 17; Wish 10; Story 4; Project 1; Umbrella 1; Request 1; Temp 1 | Resolved 4754; Open 3328; Closed 433; In Progress 153; Reopened 50 |
| MNG | 7385 | 1847 | 0.1% | 92.1% | 65.1% | 51.5% | Bug 3908; Improvement 1696; Task 688; New Feature 573; Dependency upgrade 260; Sub-task 124; Wish 123; Test 13 | Closed 6798; Open 516; Reopened 53; In Progress 11; Resolved 7 |
| IOTDB | 6145 | 5943 | 8.4% | 78.1% | 79.0% | 34.2% | Bug 2486; Improvement 2039; New Feature 848; Task 466; Sub-task 180; Wish 73; Epic 38; Test 15 | Closed 4506; Open 1182; Resolved 296; In Progress 133; Reopened 28 |
| HDFS | 6070 | 2832 | 1.4% | 36.7% | 65.9% | 31.0% | Bug 2445; Improvement 2193; Sub-task 851; New Feature 310; Task 109; Test 99; Wish 63 | Open 3000; Resolved 2197; Patch Available 685; In Progress 99; Reopened 56; Closed 33 |
| CALCITE | 6022 | 4227 | 1.5% | 67.7% | 62.5% | 62.6% | Bug 3403; Improvement 1591; New Feature 328; Task 299; Sub-task 251; Wish 108; Test 42 | Closed 3662; Open 1821; Resolved 417; In Progress 91; Reopened 31 |
| HADOOP | 5893 | 3141 | 1.6% | 49.3% | 62.1% | 38.4% | Bug 1992; Improvement 1697; Sub-task 1532; Task 332; New Feature 238; Test 67; Wish 35 | Resolved 2865; Open 2405; Patch Available 487; In Progress 50; Reopened 47; Closed 39 |
| SLING | 5742 | 4435 | 0.0% | 84.0% | 77.3% | 72.4% | Improvement 2543; Bug 1639; Task 833; New Feature 373; Sub-task 307; Test 30; Wish 17 | Closed 3500; Resolved 1337; Open 848; In Progress 48; Reopened 9 |
| NETBEANS | 5448 | 2816 | 7.8% | 41.9% | 26.3% | 24.6% | Bug 4106; Improvement 941; New Feature 193; Task 71; Wish 66; Sub-task 65; Test 6 | Open 3082; Closed 2005; Resolved 275; Reopened 46; In Progress 40 |
| YARN | 4933 | 1959 | 0.3% | 34.8% | 66.6% | 30.0% | Bug 2112; Improvement 1228; Sub-task 1206; New Feature 194; Task 114; Test 64; Wish 15 | Open 2597; Resolved 1700; Patch Available 531; In Progress 58; Reopened 28; Closed 19 |
| OAK | 4783 | 3622 | 0.0% | 72.7% | 69.4% | 63.2% | Improvement 1350; Bug 1280; Task 1131; Technical task 615; New Feature 115; Documentation 76; Sub-task 74; Epic 44; Test 38; Story 35; Wish 25 | Closed 3202; Open 1202; Resolved 274; In Progress 83; Reopened 22 |
| GEODE | 4773 | 3037 | 0.1% | 58.2% | 54.7% | 47.2% | Bug 2115; Improvement 1473; Sub-task 415; Test 254; New Feature 236; Task 211; Wish 69 | Closed 2337; Open 1708; Resolved 427; In Progress 224; Reopened 67; Patch Available 10 |
| GROOVY | 4688 | 3161 | 0.0% | 76.6% | 68.9% | 65.3% | Bug 2569; Improvement 949; Dependency upgrade 683; New Feature 211; Sub-task 118; Task 72; Wish 31; Question 23; Documentation 17; Test 3; Technical Debt 3; Epic 2; Proposal 1; Project 1; Request 1; Access 1; Outage 1; Umbrella 1; Requirement 1 | Closed 3551; Open 1070; Resolved 39; Reopened 21; In Progress 7 |
| ZEPPELIN | 4451 | 2226 | 0.4% | 42.1% | 48.3% | 39.2% | Bug 2014; Improvement 1360; Sub-task 375; Task 294; New Feature 290; Wish 64; Test 47; Epic 7 | Open 2466; Resolved 995; Closed 882; In Progress 91; Reopened 17 |
| ARTEMIS | 4378 | 3623 | 0.0% | 93.1% | 63.9% | 75.4% | Bug 2008; Improvement 863; Dependency upgrade 730; Task 386; New Feature 230; Test 76; Sub-task 52; Wish 33 | Closed 3427; Resolved 647; Open 294; Reopened 9; In Progress 1 |
| OFBIZ | 4314 | 2414 | 0.1% | 69.5% | 77.1% | 34.0% | Improvement 1527; Bug 1393; Sub-task 1104; New Feature 175; Task 101; Wish 9; Test 5 | Closed 3000; Open 933; Patch Available 189; In Progress 131; Reopened 61 |
| STORM | 4093 | 592 | 1.1% | 98.8% | 70.7% | 61.4% | Bug 1811; Improvement 1183; New Feature 358; Dependency upgrade 180; Task 155; Sub-task 151; Documentation 109; Question 45; Story 26; Test 20; Wish 19; Epic 16; Umbrella 9; Request 3; Brainstorming 2; Comment 2; New JIRA Project 1; Temp 1; Requirement 1; Project 1 | Resolved 2308; Closed 1734; Open 48; In Progress 2; Reopened 1 |
| PHOENIX | 4013 | 2359 | 0.4% | 54.5% | 67.1% | 48.0% | Bug 1843; Improvement 1030; Sub-task 530; Task 346; New Feature 172; Test 65; Wish 27 | Resolved 1800; Open 1599; Closed 389; Patch Available 163; In Progress 33; Reopened 29 |
| FLEX | 3841 | 13 | 0.0% | 0.3% | 2.9% | 4.4% | Bug 3157; Improvement 356; New Feature 198; Task 81; Question 12; Wish 12; Documentation 10; Sub-task 9; Story 3; Test 2; Dependency upgrade 1 | Open 3758; Reopened 50; In Progress 21; Closed 7; Resolved 5 |
| DRILL | 3602 | 1028 | 0.3% | 24.7% | 36.7% | 51.4% | Bug 2011; Improvement 996; New Feature 197; Task 166; Sub-task 164; Wish 38; Test 30 | Open 2530; Closed 474; Resolved 416; In Progress 72; Reviewable 54; Reopened 34; Accepted 22 |
| RANGER | 3554 | 3176 | 1.6% | 69.8% | 78.0% | 66.2% | Bug 1701; Improvement 1107; Sub-task 321; Task 206; New Feature 144; Test 54; Wish 21 | Resolved 2397; Open 848; In Progress 115; Patch Available 99; Closed 84; Reopened 11 |
| YUNIKORN | 3512 | 3512 | 0.0% | 90.8% | 94.0% | 79.1% | Sub-task 1085; Improvement 970; Bug 788; Task 470; New Feature 105; Test 86; Wish 8 | Closed 2570; Resolved 619; Open 272; In Progress 48; Reopened 3 |
| AMBARI | 3407 | 1193 | 0.9% | 27.9% | 44.7% | 35.3% | Bug 1966; Improvement 537; Task 271; Story 185; New Feature 161; Sub-task 129; Epic 51; Technical task 49; Documentation 29; Wish 20; Test 9 | Open 2209; Resolved 947; Patch Available 192; In Progress 36; Reopened 21; Closed 2 |
| MESOS | 3284 | 160 | 0.2% | 7.1% | 24.0% | 5.1% | Bug 1346; Improvement 1019; Task 517; Epic 178; Documentation 118; Wish 59; Story 47 | Open 1987; Accepted 819; Resolved 233; Reviewable 173; In Progress 72 |
| HOP | 3145 | 3145 | 0.0% | 99.9% | 42.0% | 92.8% | Bug 1244; Improvement 1007; Task 378; Sub-task 361; New Feature 145; Wish 10 | Resolved 1766; Closed 1377; Open 1; Reopened 1 |
| TIKA | 2941 | 1979 | 0.0% | 57.8% | 19.5% | 52.1% | Bug 1062; Task 903; Improvement 659; New Feature 158; Sub-task 94; Wish 55; Test 10 | Resolved 1543; Open 1200; Closed 156; Reopened 25; In Progress 17 |
| ATLAS | 2799 | 1857 | 1.4% | 61.5% | 67.7% | 43.4% | Bug 1523; Improvement 676; Sub-task 226; Task 207; New Feature 126; Wish 31; Test 10 | Resolved 1659; Open 855; Patch Available 138; In Progress 78; Closed 61; Reopened 8 |
| ZOOKEEPER | 2659 | 1291 | 0.3% | 39.5% | 45.5% | 31.1% | Bug 1303; Improvement 794; New Feature 166; Task 157; Sub-task 151; Test 44; Wish 44 | Open 1470; Resolved 548; Closed 503; Patch Available 96; In Progress 32; Reopened 10 |
| KYLIN | 2611 | 1789 | 6.6% | 71.9% | 74.4% | 65.5% | Bug 1263; Improvement 828; New Feature 185; Sub-task 178; Wish 86; Task 51; Test 20 | Closed 1243; Open 681; Resolved 634; In Progress 26; Reopened 23; In Review 4 |
| AVRO | 2607 | 1686 | 0.0% | 57.4% | 54.9% | 51.0% | Bug 1055; Improvement 1010; Task 178; New Feature 172; Sub-task 110; Test 45; Wish 37 | Resolved 1261; Open 1003; Closed 236; Patch Available 81; In Progress 18; Reopened 8 |
| FINERACT | 2592 | 2157 | 1.1% | 83.1% | 54.7% | 62.6% | Bug 1136; Improvement 851; Sub-task 233; New Feature 217; Task 136; Test 11; Wish 8 | Resolved 1452; Closed 701; Open 322; In Progress 105; Reopened 12 |
| CELEBORN | 2496 | 2496 | 0.0% | 88.9% | 80.1% | 77.2% | Improvement 1246; Bug 481; Sub-task 297; Task 250; New Feature 190; Test 26; Wish 6 | Resolved 1677; Closed 543; Open 273; Reopened 2; In Progress 1 |
| PARQUET | 2485 | 767 | 0.4% | 76.7% | 72.1% | 62.9% | Bug 1019; Improvement 1013; New Feature 200; Task 118; Sub-task 77; Wish 29; Test 29 | Resolved 1842; Open 541; Closed 63; In Progress 18; Patch Available 15; Reopened 6 |
| THRIFT | 2350 | 1396 | 0.6% | 66.5% | 59.3% | 53.6% | Bug 1242; Improvement 664; New Feature 146; Sub-task 105; Task 63; Question 33; Wish 31; Test 25; Documentation 14; Epic 5; Story 5; Brainstorming 5; Request 5; Dependency upgrade 5; Technical Debt 1; Proposal 1 | Closed 1238; Open 747; Resolved 325; Reopened 25; In Progress 15 |
| SUREFIRE | 2280 | 553 | 0.1% | 87.5% | 66.7% | 52.5% | Bug 1434; Improvement 463; New Feature 151; Task 105; Dependency upgrade 58; Wish 38; Sub-task 16; Test 15 | Closed 1994; Open 277; Reopened 5; In Progress 3; Resolved 1 |
| MINIFICPP | 2268 | 1817 | 0.0% | 89.7% | 79.1% | 58.4% | Improvement 910; Bug 751; New Feature 318; Task 125; Test 46; Epic 43; Documentation 25; Sub-task 19; Wish 14; Story 12; Brainstorming 3; Question 1; Proposal 1 | Resolved 1974; Open 209; Closed 60; Patch Available 11; In Progress 8; Reopened 6 |
| AMQ | 2213 | 1392 | 0.0% | 75.8% | 64.4% | 52.5% | Bug 1013; Dependency upgrade 413; Improvement 372; Task 194; New Feature 140; Test 32; Wish 25; Sub-task 24 | Resolved 1121; Closed 556; Open 514; Reopened 12; In Progress 10 |
| SYSTEMDS | 2164 | 1451 | 1.8% | 66.3% | 31.1% | 69.5% | Task 517; Bug 440; Improvement 388; Sub-task 361; New Feature 279; Epic 89; Test 27; Wish 15; Documentation 14; Story 9; Umbrella 6; Dependency 6; Question 4; Dependency upgrade 4; Project 2; Temp 1; Technical task 1; Proposal 1 | Closed 774; Open 694; Resolved 660; In Progress 30; Reopened 6 |
| RATIS | 2161 | 1972 | 0.1% | 88.2% | 84.0% | 65.8% | Improvement 619; Sub-task 598; Bug 567; Task 267; New Feature 66; Test 28; Wish 16 | Resolved 1892; Open 233; Closed 13; In Progress 12; Patch Available 8; Reopened 3 |
| CAUSEWAY | 2126 | 1829 | 0.1% | 86.5% | 84.0% | 84.7% | Improvement 919; Bug 677; New Feature 253; Sub-task 94; Wish 66; Task 59; Documentation 23; Question 10; Dependency upgrade 9; Epic 5; Technical task 5; Project 3; Umbrella 2; Requirement 1 | Closed 1604; Resolved 235; Open 224; In Progress 53; Reopened 10 |
| TOMEE | 2050 | 1550 | 0.0% | 95.7% | 51.1% | 59.1% | Sub-task 596; Dependency upgrade 552; Bug 464; Task 151; Improvement 142; Documentation 70; New Feature 57; Wish 10; Test 8 | Resolved 1153; Closed 808; Open 86; Reopened 2; In Progress 1 |
| PDFBOX | 2049 | 1559 | 0.0% | 82.2% | 61.9% | 60.1% | Bug 1355; Improvement 452; Task 84; New Feature 62; Wish 48; Sub-task 43; Test 5 | Closed 1553; Open 351; Resolved 131; Reopened 12; In Progress 2 |
| ASTERIXDB | 2038 | 1278 | 0.6% | 39.1% | 79.0% | 30.9% | Bug 1246; Improvement 530; Task 138; New Feature 66; Test 18; Wish 17; Epic 16; Sub-task 7 | Open 1155; Resolved 713; Closed 83; In Progress 43; Reopened 12; For Review 12; In Review 11; Started 9 |
| KARAF | 1983 | 1373 | 0.0% | 65.4% | 72.0% | 55.8% | Dependency upgrade 749; Bug 622; Improvement 300; New Feature 152; Task 64; Question 36; Documentation 22; Wish 15; Sub-task 9; Brainstorming 3; Proposal 3; IT Help 3; Test 2; Story 1; Epic 1; Dependency 1 | Resolved 1261; Open 668; Closed 35; Reopened 11; In Progress 8 |
| MAPREDUCE | 1957 | 293 | 1.3% | 11.2% | 41.6% | 10.8% | Bug 1060; Improvement 608; New Feature 128; Sub-task 71; Test 43; Task 37; Wish 10 | Open 1476; Patch Available 219; Resolved 210; Reopened 31; In Progress 11; Closed 10 |
| BIGTOP | 1871 | 1260 | 0.3% | 61.5% | 71.7% | 62.4% | Bug 682; Improvement 463; Task 295; Sub-task 276; New Feature 136; Wish 10; Test 9 | Resolved 1108; Open 660; Closed 43; Patch Available 32; In Progress 23; Reopened 5 |
| ORC | 1863 | 1644 | 0.3% | 86.0% | 87.1% | 82.0% | Improvement 610; Bug 489; Test 367; Sub-task 177; Task 142; New Feature 65; Wish 13 | Closed 1224; Resolved 378; Open 242; Reopened 13; In Progress 6 |
| TEZ | 1758 | 647 | 0.0% | 35.0% | 56.7% | 29.0% | Bug 769; Improvement 571; Sub-task 291; Task 77; New Feature 36; Wish 8; Test 6 | Open 1040; Resolved 565; Patch Available 68; Closed 51; In Progress 22; Reopened 12 |
| LOG4J2 | 1722 | 932 | 0.0% | 51.3% | 29.0% | 32.8% | Bug 937; Improvement 363; New Feature 142; Question 116; Documentation 45; Task 29; Wish 27; Sub-task 21; Epic 11; Dependency upgrade 11; Story 9; Test 4; Request 2; Brainstorming 1; Umbrella 1; Project 1; Comment 1; Proposal 1 | Open 815; Closed 465; Resolved 419; Reopened 18; In Progress 5 |
| KUDU | 1675 | 783 | 0.6% | 39.9% | 33.7% | 39.2% | Bug 693; Improvement 588; Sub-task 134; New Feature 131; Task 93; Test 25; Wish 11 | Open 971; Resolved 630; Closed 38; In Progress 14; Reopened 11; In Review 11 |
| CARBONDATA | 1674 | 702 | 4.0% | 36.1% | 33.6% | 32.5% | Bug 888; Improvement 325; Sub-task 269; New Feature 123; Task 33; Test 25; Wish 11 | Open 1054; Resolved 510; Closed 94; In Progress 9; Reopened 7 |
| JAMES | 1673 | 1222 | 0.1% | 78.8% | 15.6% | 43.5% | Improvement 682; Bug 464; Sub-task 249; New Feature 175; Task 68; Wish 22; Test 13 | Closed 1173; Open 345; Resolved 145; Reopened 7; In Progress 3 |
| GUACAMOLE | 1668 | 1430 | 0.0% | 71.3% | 24.0% | 36.6% | Bug 845; Improvement 489; New Feature 170; Wish 104; Task 52; Test 8 | Closed 981; Open 435; Resolved 209; Reopened 23; In Progress 20 |
| GOBBLIN | 1658 | 1258 | 0.1% | 30.1% | 31.7% | 27.7% | Improvement 685; Bug 628; Task 196; New Feature 119; Sub-task 18; Test 8; Wish 4 | Open 1154; Resolved 408; Closed 91; Reopened 5 |
| SM | 1638 | 1525 | 0.0% | 93.7% | 94.2% | 95.9% | Task 835; Dependency upgrade 609; Bug 135; Improvement 37; New Feature 11; Wish 6; Test 5 | Resolved 1529; Open 101; Closed 5; In Progress 2; Reopened 1 |
| KNOX | 1637 | 1372 | 0.4% | 76.4% | 77.2% | 68.4% | Bug 575; Improvement 484; Task 230; Sub-task 219; New Feature 110; Test 13; Wish 6 | Resolved 1197; Open 367; Closed 53; Patch Available 12; In Progress 5; Reopened 3 |
| CXF | 1613 | 1061 | 0.0% | 78.1% | 57.2% | 53.6% | Bug 880; Improvement 365; Sub-task 165; Task 90; New Feature 54; Test 32; Wish 27 | Closed 852; Resolved 407; Open 338; In Progress 8; Reopened 8 |
| SCB | 1609 | 1197 | 4.2% | 75.7% | 72.2% | 62.3% | Improvement 664; Bug 266; Sub-task 252; New Feature 235; Task 173; Test 12; Wish 7 | Resolved 948; Open 371; Closed 270; In Progress 17; Reopened 3 |
| JCR | 1577 | 727 | 0.0% | 60.3% | 57.0% | 47.5% | Task 616; Bug 539; Improvement 276; New Feature 67; Sub-task 58; Wish 12; Test 9 | Closed 944; Open 558; Patch Available 45; In Progress 13; Reopened 10; Resolved 7 |
| DAFFODIL | 1554 | 841 | 0.0% | 75.7% | 55.1% | 65.8% | Bug 939; Improvement 394; New Feature 183; Task 22; Wish 9; Test 3; Question 2; Documentation 1; Brainstorming 1 | Closed 1001; Open 356; Resolved 175; Reopened 15; In Progress 7 |
| NUTCH | 1488 | 462 | 0.5% | 80.8% | 60.8% | 86.6% | Improvement 593; Bug 546; New Feature 130; Sub-task 110; Task 93; Wish 11; Test 5 | Closed 1046; Open 273; Resolved 157; In Progress 7; Reopened 5 |
| FELIX | 1484 | 661 | 0.0% | 50.1% | 41.2% | 38.8% | Bug 730; Improvement 558; New Feature 115; Task 42; Wish 20; Sub-task 16; Test 3 | Open 725; Closed 502; Resolved 242; In Progress 9; Reopened 6 |
| ARIES | 1468 | 274 | 0.3% | 81.7% | 69.5% | 71.5% | Bug 825; Improvement 340; New Feature 116; Task 76; Dependency upgrade 69; Sub-task 12; Test 11; Question 9; Epic 3; Documentation 2; TCK Challenge 2; Brainstorming 1; Request 1; Wish 1 | Closed 1140; Open 256; Resolved 59; In Progress 8; Reopened 5 |
| MAHOUT | 1462 | 121 | 4.7% | 96.0% | 77.4% | 81.3% | Bug 552; Improvement 483; New Feature 189; Task 79; Sub-task 39; Documentation 36; Question 29; Wish 20; Test 14; Epic 13; Story 2; Dependency 2; New JIRA Project 1; Dependency upgrade 1; Proposal 1; Planned Work 1 | Closed 1181; Resolved 222; Open 48; In Progress 5; Reopened 4; Patch Available 2 |
| WW | 1404 | 764 | 0.0% | 90.2% | 36.1% | 72.9% | Improvement 514; Bug 513; Dependency 179; Task 96; New Feature 83; Sub-task 15; Temp 3; Epic 1 | Closed 1099; Resolved 167; Open 138 |
| DERBY | 1391 | 114 | 0.1% | 4.5% | 6.8% | 3.5% | Bug 663; Improvement 620; Task 80; Sub-task 28 | Open 1297; Closed 56; Reopened 21; In Progress 11; Resolved 6 |
| CB | 1346 | 0 | 0.0% | 33.2% | 19.1% | 7.6% | Bug 909; Improvement 251; Sub-task 71; New Feature 52; Task 42; Wish 16; Test 5 | Open 867; Closed 398; Resolved 50; Reopened 22; In Progress 9 |
| MSHARED | 1284 | 622 | 0.0% | 96.1% | 87.1% | 81.3% | Improvement 412; Dependency upgrade 336; Bug 306; Task 135; New Feature 81; Wish 10; Test 3; Sub-task 1 | Closed 1230; Open 49; Resolved 4; Reopened 1 |
| SLIDER | 1256 | 0 | 1.5% | 100.0% | 80.2% | 70.7% | Bug 625; Sub-task 261; Improvement 190; Task 86; New Feature 60; Test 15; Umbrella 10; Documentation 8; Wish 1 | Closed 1256 |
| PIG | 1184 | 84 | 0.8% | 12.7% | 41.6% | 28.9% | Bug 609; Improvement 372; New Feature 105; Sub-task 58; Task 19; Test 14; Wish 7 | Open 977; Closed 137; Patch Available 39; Resolved 13; Reopened 12; In Progress 6 |
| SAMZA | 1180 | 380 | 0.0% | 22.0% | 49.1% | 24.3% | Bug 535; Improvement 359; Sub-task 120; New Feature 104; Task 40; Test 13; Wish 9 | Open 847; Resolved 184; Closed 78; Patch Available 39; In Progress 23; Reopened 9 |
| SUBMARINE | 1171 | 1088 | 0.2% | 88.2% | 90.4% | 72.2% | Sub-task 398; Improvement 295; Bug 271; New Feature 120; Task 69; Test 12; Wish 6 | Resolved 1027; Open 134; Closed 6; Reopened 2; In Progress 2 |
| MRELEASE | 1130 | 122 | 0.1% | 90.2% | 59.9% | 37.3% | Bug 753; Improvement 210; New Feature 88; Task 38; Dependency upgrade 23; Wish 16; Sub-task 2 | Closed 1017; Open 97; Reopened 13; Resolved 2; In Progress 1 |
| PROTON | 1129 | 825 | 0.0% | 66.3% | 71.9% | 65.4% | Bug 564; Improvement 324; Task 144; New Feature 42; Test 41; Wish 7; Sub-task 7 | Closed 387; Open 372; Resolved 361; Reopened 6; In Progress 3 |
| FLUME | 1123 | 126 | 1.1% | 14.5% | 29.7% | 12.4% | Bug 543; Improvement 283; New Feature 96; Sub-task 58; Question 45; Documentation 35; Task 28; Wish 12; Dependency upgrade 7; Brainstorming 4; Test 3; Umbrella 2; IT Help 2; Request 2; Epic 1; Blog - New Blog Request 1; Choose from below ... 1 | Open 762; Patch Available 184; Closed 87; Resolved 76; In Progress 10; Reopened 4 |
| OOZIE | 1118 | 151 | 0.1% | 15.8% | 31.6% | 14.3% | Bug 562; Improvement 277; Sub-task 119; New Feature 88; Task 57; Test 8; Wish 7 | Open 754; Resolved 150; Patch Available 104; Reopened 71; Closed 28; In Progress 11 |
| MADLIB | 1106 | 117 | 0.0% | 9.0% | 82.6% | 12.8% | Bug 508; Task 184; New Feature 146; Sub-task 110; Improvement 70; Request 61; Question 12; Epic 6; Documentation 4; Wish 3; Test 2 | Closed 578; Open 320; Resolved 196; For Review 6; Blocked 3; Reopened 3 |
| QPID | 1104 | 388 | 0.0% | 75.1% | 32.8% | 53.0% | Bug 530; Improvement 444; Task 56; New Feature 43; Sub-task 16; Test 9; Wish 6 | Closed 765; Open 270; Resolved 64; Reopened 3; Reviewable 1; In Progress 1 |
| TINKERPOP | 1101 | 971 | 0.0% | 83.7% | 57.2% | 59.2% | Improvement 661; Bug 431; New Feature 5; Task 3; Wish 1 | Closed 922; Open 178; Reopened 1 |
| MXNET | 1097 | 14 | 0.0% | 0.4% | 50.9% | 0.0% | Bug 286; Improvement 248; Sub-task 184; New Feature 137; Task 114; Story 87; Epic 31; Test 10 | To Do 672; Done 337; In Progress 56; In Review 32 |
| AXIS | 1094 | 9 | 0.0% | 1.3% | 4.3% | 3.0% | Bug 977; Improvement 73; New Feature 20; Task 10; Wish 9; Test 4; Sub-task 1 | Open 1052; Reopened 27; Closed 8; Resolved 6; In Progress 1 |
| AIRAVATA | 1089 | 458 | 1.2% | 23.4% | 65.4% | 30.5% | Bug 420; Sub-task 244; New Feature 148; Improvement 122; Task 62; Epic 38; Story 35; Project 4; Test 3; Documentation 2; Brainstorming 2; Technical task 2; Wish 2; Question 1; Dependency upgrade 1; IT Help 1; Request 1; New JIRA Project 1 | Open 767; Resolved 212; Closed 43; In Progress 39; Reopened 28 |
| DISPATCH | 1063 | 835 | 0.0% | 100.0% | 72.2% | 75.3% | Bug 575; Improvement 229; Test 153; New Feature 40; Task 39; Sub-task 15; Wish 12 | Closed 985; Resolved 78 |
| OPENJPA | 1036 | 226 | 0.1% | 19.3% | 32.5% | 22.0% | Bug 661; Improvement 147; Sub-task 92; New Feature 59; Task 30; Question 19; Wish 13; Test 6; Documentation 5; Dependency upgrade 3; Epic 1 | Open 807; Closed 108; Resolved 92; Reopened 20; In Progress 9 |
| DATALAB | 1024 | 733 | 0.0% | 74.2% | 88.0% | 71.8% | Task 484; Bug 370; Epic 75; Improvement 65; New Feature 25; Sub-task 5 | Closed 759; Open 213; In Progress 38; Reopened 6; on hold 4; Verified 2; Resolved 1; Blocked 1 |
| FOP | 1021 | 466 | 0.0% | 46.5% | 36.9% | 30.8% | Bug 861; Improvement 124; New Feature 18; Wish 9; Task 7; Test 2 | Open 529; Resolved 339; Closed 136; Reopened 16; In Progress 1 |
| MASSEMBLY | 1017 | 107 | 0.1% | 93.3% | 72.2% | 55.9% | Bug 658; Improvement 191; New Feature 69; Task 46; Dependency upgrade 42; Wish 9; Test 1; Sub-task 1 | Closed 949; Open 64; Reopened 4 |
| SCM | 1012 | 100 | 0.1% | 96.4% | 71.0% | 63.8% | Bug 571; Improvement 225; New Feature 103; Task 59; Dependency upgrade 22; Sub-task 15; Wish 9; Test 8 | Closed 976; Open 34; Reopened 1; In Progress 1 |
| HARMONY | 1005 | 0 | 0.1% | 0.1% | 20.1% | 2.4% | Bug 700; Improvement 151; Sub-task 52; New Feature 42; Task 29; Test 26; Wish 5 | Open 970; Reopened 26; In Progress 8; Resolved 1 |
| AXIS2C | 963 | 6 | 0.1% | 97.9% | 55.3% | 54.5% | Bug 699; Improvement 182; New Feature 37; Task 29; Sub-task 7; Test 6; Wish 3 | Resolved 704; Closed 239; Open 20 |
| MDEP | 949 | 310 | 0.1% | 82.4% | 61.0% | 49.9% | Bug 457; Improvement 234; New Feature 110; Dependency upgrade 93; Task 35; Wish 14; Test 4; Sub-task 2 | Closed 776; Open 157; Reopened 9; Resolved 6; In Progress 1 |
| UNOMI | 935 | 746 | 0.2% | 85.0% | 56.8% | 69.6% | Bug 350; Improvement 242; Task 149; Sub-task 138; New Feature 46; Test 6; Wish 4 | Closed 794; Open 135; In Progress 3; In Tests 2; In Review 1 |
| UIMA | 933 | 324 | 0.0% | 60.6% | 60.6% | 46.4% | Bug 404; Improvement 320; New Feature 100; Task 73; Wish 9; Question 7; Story 5; Brainstorming 4; Test 3; Sub-task 3; Technical task 2; Dependency upgrade 2; Documentation 1 | Resolved 538; Open 355; Closed 27; Reopened 9; In Progress 4 |
| MSITE | 921 | 168 | 0.1% | 97.2% | 75.0% | 57.1% | Bug 532; Improvement 166; Dependency upgrade 80; Task 68; New Feature 50; Wish 18; Sub-task 7 | Closed 894; Open 21; In Progress 3; Reopened 2; Resolved 1 |
| SQOOP | 880 | 28 | 0.0% | 1.2% | 26.0% | 28.6% | Bug 515; Improvement 181; New Feature 67; Sub-task 55; Task 32; Wish 19; Test 11 | Open 788; Patch Available 67; Resolved 11; In Progress 9; Reopened 5 |
| TAVERNA | 874 | 4 | 0.3% | 0.0% | 2.7% | 2.4% | Bug 618; Task 113; New Feature 105; Sub-task 25; Story 13 | To Do 866; In Progress 5; In Review 3 |
| SVN | 871 | 80 | 0.0% | 9.9% | 7.8% | 76.6% | Bug 499; Improvement 234; New Feature 72; Task 46; Sub-task 11; Wish 8; Test 1 | Open 768; Closed 76; Reopened 11; Resolved 10; In Progress 6 |
| CAY | 867 | 419 | 0.0% | 53.9% | 67.7% | 64.8% | Bug 387; Improvement 286; Task 181; Sub-task 13 | Closed 467; Open 388; Reopened 7; In Progress 3; Blocked 2 |
| OPENNLP | 853 | 694 | 1.8% | 89.3% | 83.0% | 78.9% | Improvement 268; Task 200; Dependency upgrade 112; Bug 106; New Feature 49; Sub-task 31; Test 29; Documentation 25; Wish 13; Epic 10; Question 5; Brainstorming 2; Github Integration 2; Planned Work 1 | Closed 403; Resolved 359; Open 85; In Progress 5; Reopened 1 |
| AXIS2 | 843 | 130 | 0.0% | 24.1% | 23.4% | 14.1% | Bug 663; Improvement 120; Task 22; New Feature 20; Wish 9; Test 5; Sub-task 4 | Open 616; Resolved 147; Closed 56; Reopened 23; In Progress 1 |
| TRAFODION | 813 | 5 | 3.0% | 0.5% | 68.4% | 17.7% | Bug 496; Improvement 151; New Feature 56; Sub-task 46; Documentation 38; Wish 11; Umbrella 5; Test 4; Task 4; Question 1; Technical task 1 | Open 746; In Progress 51; Reopened 12; Resolved 4 |
| MJAVADOC | 811 | 191 | 0.2% | 94.9% | 77.6% | 57.2% | Bug 523; Improvement 150; New Feature 43; Task 42; Dependency upgrade 34; Wish 14; Sub-task 4; Test 1 | Closed 766; Open 40; Resolved 4; Reopened 1 |
| INLONG | 802 | 801 | 0.4% | 84.9% | 82.2% | 59.1% | Sub-task 396; Improvement 212; Bug 106; New Feature 43; Task 34; Wish 10; Test 1 | Resolved 544; Closed 137; Open 109; In Progress 12 |
| SEDONA | 756 | 756 | 0.3% | 94.3% | 12.7% | 84.7% | New Feature 236; Improvement 224; Bug 192; Task 72; Test 24; Wish 4; Sub-task 4 | Resolved 673; Open 42; Closed 40; In Progress 1 |
| JENA | 742 | 551 | 0.1% | 80.6% | 70.5% | 64.7% | Improvement 289; Bug 284; Task 85; New Feature 39; Question 25; Wish 10; Dependency upgrade 2; Brainstorming 2; Epic 2; Test 2; Story 1; Comment 1 | Closed 596; Open 141; In Progress 2; Resolved 2; Reopened 1 |
| OPENMEETINGS | 739 | 685 | 0.0% | 90.1% | 98.8% | 59.9% | Bug 421; Improvement 164; Task 68; Test 45; New Feature 29; Wish 8; Sub-task 4 | Closed 379; Resolved 287; Open 66; In Progress 4; Reopened 3 |
| CURATOR | 724 | 173 | 0.0% | 82.9% | 63.7% | 62.7% | Bug 402; Improvement 206; Task 35; New Feature 30; Test 18; Sub-task 18; Wish 15 | Resolved 380; Closed 220; Open 122; Reopened 2 |
| TOBAGO | 722 | 541 | 0.4% | 82.0% | 78.1% | 74.8% | Bug 377; Improvement 131; New Feature 129; Task 78; Wish 7 | Closed 575; Open 121; Resolved 17; In Progress 8; Reopened 1 |
| MRESOLVER | 714 | 620 | 0.0% | 94.1% | 85.7% | 83.5% | Dependency upgrade 202; Improvement 164; Task 151; Bug 125; New Feature 56; Sub-task 10; Wish 4; Test 2 | Closed 672; Open 36; Reopened 5; In Progress 1 |
| METRON | 713 | 25 | 0.1% | 2.8% | 20.1% | 0.6% | Bug 261; Improvement 258; New Feature 79; Sub-task 70; Task 24; Wish 16; Test 5 | To Do 661; In Progress 32; Done 20 |
| DOXIA | 703 | 165 | 0.0% | 98.6% | 84.2% | 72.7% | Bug 352; Improvement 149; Task 93; New Feature 50; Dependency upgrade 38; Wish 10; Sub-task 7; Test 4 | Closed 676; Resolved 17; Open 10 |
| TRINIDAD | 702 | 1 | 0.3% | 0.0% | 13.1% | 2.6% | Bug 466; Improvement 154; New Feature 41; Wish 21; Task 16; Sub-task 3; Test 1 | Open 598; Patch Available 82; Reopened 18; In Progress 4 |
| SENTRY | 701 | 22 | 0.0% | 12.6% | 41.5% | 14.0% | Bug 277; Improvement 199; Sub-task 82; Task 50; New Feature 47; Test 40; Wish 6 | Open 492; Patch Available 101; Resolved 87; In Progress 17; Reopened 3; Closed 1 |
| TS | 695 | 0 | 0.0% | 0.7% | 56.1% | 98.1% | Bug 355; Improvement 246; New Feature 69; Task 11; Test 8; Wish 5; Sub-task 1 | Open 633; Patch Available 36; Reopened 15; In Progress 6; Closed 5 |
| ARCHETYPE | 649 | 107 | 0.0% | 91.5% | 49.6% | 50.5% | Bug 348; Improvement 163; New Feature 54; Dependency upgrade 45; Task 24; Wish 10; Test 3; Sub-task 2 | Closed 593; Open 54; Resolved 1; Reopened 1 |
| STREAMPIPES | 640 | 588 | 0.0% | 88.6% | 67.8% | 75.3% | Improvement 221; Bug 199; New Feature 116; Sub-task 58; Task 42; Test 3; Wish 1 | Closed 524; Open 68; Resolved 43; In Progress 4; Reopened 1 |
| WICKET | 634 | 483 | 0.0% | 74.6% | 67.7% | 61.8% | Bug 281; Improvement 278; Task 36; New Feature 25; Sub-task 8; Wish 6 | Resolved 433; Open 150; Closed 40; Reopened 9; In Progress 2 |
| WAGON | 614 | 68 | 0.0% | 97.6% | 73.5% | 61.7% | Bug 346; Improvement 126; Dependency upgrade 53; Task 52; New Feature 32; Wish 3; Test 2 | Closed 599; Open 14; Reopened 1 |
| JSPWIKI | 609 | 142 | 0.0% | 73.9% | 38.9% | 56.8% | Bug 294; Improvement 218; New Feature 42; Task 29; Wish 21; Test 3; Sub-task 1; Epic 1 | Closed 426; Open 148; Resolved 24; In Progress 6; Reopened 5 |
| YETUS | 597 | 350 | 0.3% | 60.1% | 57.0% | 45.4% | Bug 230; Improvement 206; New Feature 91; Task 58; Sub-task 6; Test 3; Wish 3 | Resolved 351; Open 230; Closed 8; In Progress 3; Patch Available 3; Reopened 2 |
| DIRSTUDIO | 595 | 102 | 0.0% | 62.9% | 35.8% | 48.7% | Bug 310; Improvement 153; New Feature 53; Task 42; Question 13; Sub-task 12; Wish 5; Documentation 2; Brainstorming 2; IT Help 1; Test 1; Dependency upgrade 1 | Closed 367; Open 213; Resolved 7; Reopened 4; In Progress 4 |
| JCLOUDS | 593 | 110 | 0.2% | 20.9% | 23.1% | 15.5% | Bug 292; Improvement 162; New Feature 90; Task 27; Sub-task 9; Wish 7; Test 6 | Open 454; Resolved 101; Closed 23; In Progress 9; Reopened 6 |
| ACCUMULO | 588 | 0 | 0.0% | 76.9% | 12.9% | 1.4% | Improvement 264; Bug 185; Sub-task 46; New Feature 38; Task 37; Test 11; Wish 7 | Resolved 452; Open 134; Reopened 2 |
| JCRVLT | 588 | 470 | 0.0% | 76.5% | 68.7% | 67.3% | Improvement 302; Bug 217; Task 45; New Feature 12; Sub-task 9; Test 3 | Closed 368; Open 129; Resolved 82; In Progress 5; Reopened 2; Patch Available 2 |
| TUSCANY | 586 | 0 | 3.2% | 0.0% | 19.6% | 81.6% | Bug 399; Improvement 91; New Feature 44; Test 19; Wish 16; Sub-task 10; Task 7 | Open 558; Reopened 19; In Progress 9 |
| MCOMPILER | 577 | 193 | 0.2% | 86.7% | 61.7% | 40.0% | Bug 347; Improvement 138; New Feature 34; Dependency upgrade 27; Task 23; Wish 7; Test 1 | Closed 498; Open 75; Reopened 2; Resolved 2 |
| SYNCOPE | 563 | 469 | 0.0% | 96.4% | 91.8% | 91.7% | Bug 238; Improvement 199; New Feature 51; Sub-task 44; Task 29; Wish 2 | Closed 531; Open 20; Resolved 12 |
| FALCON | 541 | 0 | 0.0% | 0.6% | 42.0% | 12.8% | Bug 222; Improvement 139; Sub-task 86; New Feature 48; Task 26; Test 16; Wish 4 | Open 507; In Progress 20; Patch Available 7; Reopened 4; Resolved 3 |
| LIVY | 537 | 256 | 0.4% | 27.2% | 32.6% | 90.5% | Bug 215; Improvement 147; Sub-task 59; New Feature 51; Task 37; Question 14; Wish 3; Documentation 3; Epic 3; Request 1; Test 1; Access 1; IT Help 1; Dependency upgrade 1 | Open 379; Resolved 133; Closed 13; In Progress 10; Reopened 2 |
| USERGRID | 531 | 2 | 0.2% | 0.2% | 12.1% | 9.8% | Story 314; Bug 106; Epic 66; Improvement 39; Technical task 4; Wish 2 | Open 516; In Progress 7; Patch Available 6; Reopened 2 |
| SDAP | 527 | 312 | 0.0% | 68.1% | 51.4% | 19.5% | Improvement 155; Bug 151; Task 98; New Feature 83; Sub-task 35; Wish 4; Test 1 | Closed 352; To Do 111; WontFix 40; In Progress 17; Done 7 |
| MPLUGIN | 526 | 186 | 0.2% | 93.7% | 83.7% | 73.8% | Bug 218; Improvement 150; Task 63; Dependency upgrade 48; New Feature 38; Wish 7; Sub-task 2 | Closed 489; Open 32; Resolved 4; Reopened 1 |
| MYFACES | 526 | 455 | 0.2% | 97.0% | 74.5% | 77.9% | Bug 337; Improvement 128; Task 28; New Feature 17; Sub-task 10; Wish 5; Test 1 | Closed 405; Resolved 105; Open 14; Reopened 2 |
| NLPCRAFT | 526 | 526 | 0.0% | 85.0% | 97.3% | 95.4% | Task 279; Bug 118; Improvement 117; New Feature 9; Test 3 | Closed 445; Open 74; In Progress 5; Resolved 2 |
| SSHD | 522 | 389 | 0.0% | 85.6% | 51.9% | 51.1% | Bug 196; Improvement 153; Question 92; New Feature 59; Task 7; Wish 6; Request 3; Documentation 2; Test 1; Sub-task 1; Dependency upgrade 1; Story 1 | Resolved 352; Closed 95; Open 70; Reopened 4; In Progress 1 |
| MENFORCER | 512 | 172 | 0.0% | 96.5% | 78.7% | 65.0% | Bug 216; Improvement 132; New Feature 79; Dependency upgrade 47; Task 29; Wish 8; Test 1 | Closed 491; Open 18; Resolved 3 |
| CASSSIDECAR | 508 | 498 | 0.0% | 69.3% | 80.5% | 66.1% | Improvement 220; Bug 106; Task 91; New Feature 62; Sub-task 23; Epic 6 | Resolved 352; Triage Needed 121; Patch Available 11; Open 10; In Progress 8; Review In Progress 5; Awaiting Feedback 1 |
| BATIK | 505 | 122 | 0.0% | 11.1% | 56.0% | 9.3% | Bug 437; Improvement 51; New Feature 9; Wish 4; Task 3; Test 1 | Open 419; Resolved 48; In Progress 17; Reopened 13; Closed 8 |
| LANG | 503 | 327 | 0.0% | 66.6% | 12.3% | 59.0% | Bug 219; Improvement 154; New Feature 68; Sub-task 36; Wish 12; Task 9; Test 5 | Resolved 220; Open 158; Closed 115; Reopened 9; In Progress 1 |
| DIRSERVER | 502 | 125 | 0.0% | 20.9% | 12.9% | 51.2% | Bug 291; Improvement 107; New Feature 50; Task 36; Wish 13; Test 4; Sub-task 1 | Open 377; Resolved 84; Closed 21; Reopened 15; In Progress 5 |
| RAT | 501 | 315 | 0.2% | 77.4% | 57.1% | 81.4% | Bug 156; Improvement 154; Sub-task 108; Task 46; New Feature 30; Wish 6; Test 1 | Closed 382; Open 99; In Progress 14; Resolved 6 |
| MNGSITE | 493 | 147 | 0.2% | 92.9% | 70.0% | 0.0% | Bug 263; Improvement 155; Task 47; New Feature 11; Sub-task 10; Wish 6; Dependency upgrade 1 | Closed 454; Open 33; Resolved 4; Reopened 2 |
| TOMAHAWK | 492 | 5 | 0.0% | 1.0% | 23.2% | 1.0% | Bug 339; Improvement 87; New Feature 53; Task 12; Sub-task 1 | Open 429; Patch Available 37; Reopened 15; In Progress 6; Resolved 4; Closed 1 |
| OLINGO | 481 | 228 | 0.0% | 25.6% | 21.8% | 16.2% | Bug 297; Question 55; Improvement 51; New Feature 50; Task 19; Wish 6; Sub-task 3 | Open 346; Closed 78; Resolved 45; In Progress 7; Reopened 5 |
| MSHADE | 478 | 137 | 0.0% | 79.9% | 62.1% | 53.6% | Bug 259; Improvement 106; New Feature 41; Dependency upgrade 34; Task 30; Wish 7; Test 1 | Closed 379; Open 94; Resolved 3; Reopened 2 |
| REEF | 471 | 11 | 0.4% | 2.3% | 36.7% | 2.8% | Improvement 140; Sub-task 121; Bug 88; New Feature 69; Task 38; Test 11; Wish 4 | Open 426; In Progress 26; Reopened 8; Resolved 7; Closed 4 |
| MCHANGES | 465 | 68 | 0.0% | 95.1% | 66.7% | 60.9% | Bug 191; Improvement 130; New Feature 68; Dependency upgrade 29; Task 25; Wish 16; Sub-task 5; Test 1 | Closed 442; Open 22; Reopened 1 |
| MPIR | 460 | 93 | 0.2% | 97.4% | 80.2% | 69.8% | Bug 221; Improvement 133; Task 43; Dependency upgrade 33; New Feature 23; Sub-task 4; Wish 2; Test 1 | Closed 448; Open 12 |
| MWAR | 456 | 41 | 0.2% | 96.1% | 68.4% | 55.0% | Bug 239; Improvement 128; New Feature 32; Task 22; Dependency upgrade 21; Wish 10; Test 4 | Closed 438; Open 16; Reopened 2 |
| IVY | 453 | 57 | 4.4% | 9.1% | 11.0% | 10.2% | Bug 230; Improvement 150; New Feature 45; Question 10; Wish 9; Task 5; Test 1; Documentation 1; Story 1; Dependency upgrade 1 | Open 405; Resolved 39; Reopened 5; In Progress 2; Closed 2 |
| LIBCLOUD | 452 | 0 | 0.4% | 0.0% | 4.0% | 1.5% | Bug 204; Improvement 137; New Feature 79; Task 16; Wish 7; Sub-task 5; Test 4 | Open 449; Reopened 3 |
| HAWQ | 447 | 97 | 0.0% | 33.6% | 99.6% | 74.3% | Bug 182; Sub-task 99; Improvement 76; New Feature 38; Wish 35; Task 13; Test 4 | Open 289; Closed 140; Resolved 10; Reopened 6; In Progress 2 |
| MCHECKSTYLE | 444 | 69 | 0.2% | 92.6% | 69.6% | 56.1% | Bug 216; Improvement 121; Task 42; Dependency upgrade 26; New Feature 24; Wish 13; Test 1; Sub-task 1 | Closed 411; Open 31; Reopened 2 |
| HTTPCLIENT | 439 | 369 | 0.0% | 97.7% | 8.7% | 54.0% | Bug 275; Improvement 117; New Feature 23; Wish 14; Task 7; Sub-task 2; Test 1 | Resolved 336; Closed 93; Open 9; In Progress 1 |
| SHIRO | 437 | 173 | 0.7% | 52.9% | 39.6% | 41.9% | Improvement 153; Bug 136; New Feature 64; Task 30; Dependency upgrade 22; Question 10; Wish 6; Documentation 6; Sub-task 3; Test 3; Temp 1; Brainstorming 1; Dependency 1; Epic 1 | Open 200; Resolved 149; Closed 82; In Progress 3; Reopened 3 |
| MPOM | 434 | 251 | 0.0% | 96.3% | 87.8% | 87.3% | Improvement 155; Dependency upgrade 150; Task 51; Bug 44; Wish 16; New Feature 16; Test 2 | Closed 418; Open 15; Reopened 1 |
| RAVE | 422 | 0 | 0.0% | 0.0% | 11.8% | 2.8% | Sub-task 173; Improvement 67; Bug 63; Story 54; Epic 24; New Feature 17; Task 16; Technical task 5; Umbrella 3 | Open 410; In Progress 8; Reopened 4 |
| CONTINUUM | 415 | 0 | 0.0% | 0.7% | 2.9% | 1.2% | Bug 188; Improvement 123; New Feature 67; Wish 22; Task 12; Test 2; Question 1 | Open 405; Reopened 7; Closed 3 |
| COCOON | 414 | 5 | 0.0% | 1.2% | 5.8% | 2.7% | Bug 252; Improvement 112; New Feature 21; Task 19; Wish 8; Sub-task 2 | Open 369; Reopened 19; Continued 18; Closed 5; Blocked 3 |
| FOR | 410 | 0 | 0.0% | 0.2% | 1.0% | 16.8% | Bug 179; Improvement 99; New Feature 52; Task 45; Sub-task 33; Test 2 | Open 400; Reopened 9; Closed 1 |
| TAP5 | 410 | 224 | 0.0% | 55.9% | 60.2% | 47.1% | Bug 167; Improvement 161; New Feature 29; Task 21; Wish 11; Documentation 9; Dependency upgrade 7; Test 1; Sub-task 1; Request 1; Question 1; Technical Debt 1 | Open 172; Closed 134; Resolved 95; Reopened 6; In Progress 3 |
| IO | 406 | 247 | 0.0% | 77.6% | 11.8% | 53.0% | Bug 232; Improvement 99; New Feature 51; Wish 15; Task 6; Test 3 | Resolved 190; Closed 125; Open 86; Reopened 4; In Progress 1 |
| MPMD | 405 | 116 | 0.2% | 95.6% | 78.0% | 74.6% | Bug 165; Improvement 110; Dependency upgrade 47; New Feature 38; Task 33; Wish 11; Test 1 | Closed 387; Open 18 |
| HELIX | 397 | 46 | 0.0% | 16.4% | 33.8% | 5.5% | Bug 132; Improvement 118; Task 55; Sub-task 54; New Feature 32; Test 5; Wish 1 | Open 326; Closed 61; Reopened 5; Resolved 4; In Progress 1 |
| AURORA | 392 | 0 | 0.3% | 0.0% | 14.3% | 0.8% | Task 169; Story 128; Bug 76; Epic 13; Sub-task 6 | Open 350; Accepted 15; Reviewable 13; Reopened 7; Closed 4; In Progress 3 |
| OPENEJB | 378 | 9 | 7.9% | 1.1% | 19.6% | 51.1% | Sub-task 125; Bug 116; Improvement 61; New Feature 44; Task 18; Wish 8; Test 5; Dependency upgrade 1 | Open 353; Reopened 13; In Progress 8; Closed 2; Resolved 2 |
| TAJO | 377 | 1 | 0.3% | 0.3% | 37.4% | 22.8% | Improvement 140; Bug 76; Sub-task 72; New Feature 55; Task 27; Wish 6; Test 1 | Open 315; In Progress 35; Patch Available 22; Reopened 4; Resolved 1 |
| LENS | 377 | 4 | 0.3% | 2.9% | 44.6% | 6.9% | Improvement 150; Bug 109; Sub-task 39; New Feature 36; Task 28; Wish 8; Test 7 | Open 346; Reopened 9; Patch Available 9; In Progress 7; Resolved 6 |
| NPANDAY | 376 | 0 | 0.0% | 100.0% | 58.2% | 90.7% | Bug 230; Improvement 84; New Feature 29; Sub-task 17; Task 9; Technical task 6; Wish 1 | Closed 376 |
| VFS | 369 | 117 | 0.0% | 26.6% | 6.8% | 26.0% | Bug 250; Improvement 75; New Feature 22; Wish 13; Sub-task 5; Task 4 | Open 265; Resolved 64; Closed 34; Reopened 6 |
| MINVOKER | 369 | 123 | 0.0% | 95.7% | 85.9% | 77.5% | Bug 119; Improvement 113; New Feature 64; Dependency upgrade 42; Task 27; Sub-task 2; Wish 1; Test 1 | Closed 353; Open 16 |
| SIS | 364 | 153 | 0.3% | 60.7% | 64.6% | 56.9% | Improvement 105; Task 80; Sub-task 72; New Feature 53; Bug 47; Wish 5; Test 2 | Closed 214; Open 139; Resolved 7; Reopened 3; In Progress 1 |
| STDCXX | 352 | 0 | 0.0% | 0.3% | 23.6% | 64.2% | Bug 236; Improvement 60; Sub-task 27; New Feature 24; Task 3; Wish 1; Test 1 | Open 330; In Progress 11; Reopened 10; Closed 1 |
| DOXIASITETOOLS | 348 | 140 | 0.0% | 96.8% | 89.7% | 85.1% | Improvement 97; Dependency upgrade 80; Bug 72; Task 65; New Feature 22; Wish 10; Test 1; Sub-task 1 | Closed 335; Open 10; Resolved 2; In Progress 1 |
| TORQUEOLD | 347 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Bug 219; Improvement 117; New Feature 7; Task 4 | Closed 251; Open 89; Resolved 7 |
| XERCESJ | 345 | 79 | 0.0% | 21.4% | 22.3% | 5.8% | Bug 250; Improvement 50; Task 21; New Feature 18; Wish 6 | Open 251; Closed 44; Resolved 30; Reopened 14; In Progress 6 |
| MNEMONIC | 345 | 305 | 66.4% | 81.2% | 94.2% | 83.8% | Sub-task 126; Improvement 80; Task 54; Bug 48; New Feature 29; Test 6; Wish 2 | Closed 220; Resolved 60; Open 41; In Progress 23; Reopened 1 |
| APEXMALHAR | 344 | 0 | 1.2% | 0.0% | 47.1% | 1.5% | Bug 105; Improvement 79; Task 77; New Feature 47; Sub-task 19; Documentation 12; Test 2; Dependency upgrade 2; Wish 1 | Open 328; In Progress 13; Reopened 3 |
| GIRAPH | 341 | 25 | 0.0% | 43.4% | 32.8% | 31.4% | Improvement 137; Bug 137; New Feature 31; Task 23; Wish 8; Sub-task 3; Test 2 | Resolved 148; Open 143; Patch Available 45; Reopened 3; In Progress 2 |
| GSOC | 332 | 206 | 0.0% | 32.5% | 0.0% | 0.0% | New Feature 145; Improvement 71; Task 63; Wish 30; Bug 23 | Open 224; Closed 101; Resolved 7 |
| COMPRESS | 329 | 226 | 0.0% | 71.4% | 19.1% | 56.2% | Bug 194; Improvement 78; New Feature 30; Wish 12; Sub-task 8; Task 5; Test 2 | Resolved 195; Open 93; Closed 40; Reopened 1 |
| MATH | 322 | 185 | 0.3% | 41.9% | 11.5% | 54.7% | Bug 108; Improvement 86; Sub-task 48; Task 29; New Feature 26; Wish 15; Test 10 | Open 182; Resolved 123; Closed 12; Reopened 5 |
| MEAR | 320 | 51 | 0.3% | 97.2% | 87.2% | 68.4% | Bug 129; Improvement 95; New Feature 36; Dependency upgrade 35; Task 19; Wish 5; Test 1 | Closed 311; Open 9 |
| CLEREZZA | 319 | 16 | 0.6% | 75.9% | 33.9% | 4.1% | Bug 115; Improvement 80; Sub-task 56; Task 32; New Feature 26; Question 4; Wish 2; Proposal 2; Brainstorming 1; Umbrella 1 | Closed 241; Open 76; Resolved 1; Reopened 1 |
| XMLBEANS | 307 | 130 | 0.0% | 46.6% | 34.2% | 50.2% | Bug 186; Improvement 63; Task 31; New Feature 22; Wish 5 | Open 160; Resolved 91; Closed 52; Reopened 4 |
| BROOKLYN | 307 | 12 | 0.0% | 2.3% | 3.9% | 8.8% | Bug 200; Improvement 69; New Feature 13; Sub-task 12; Task 4; Story 3; Documentation 2; Question 1; Project 1; Test 1; Dependency 1 | Open 294; In Progress 5; Resolved 4; Closed 3; Reopened 1 |
| JEXL | 302 | 155 | 0.0% | 98.7% | 87.7% | 94.7% | Bug 161; Improvement 94; New Feature 33; Wish 8; Task 5; Test 1 | Closed 220; Resolved 78; Open 4 |
| MJAR | 301 | 52 | 0.0% | 96.0% | 69.8% | 57.8% | Bug 140; Improvement 83; New Feature 29; Task 27; Dependency upgrade 17; Wish 2; Sub-task 2; Test 1 | Closed 288; Open 11; Resolved 1; Reopened 1 |
| MDEPLOY | 299 | 58 | 0.0% | 96.0% | 71.2% | 41.8% | Bug 165; Improvement 57; New Feature 32; Dependency upgrade 20; Task 19; Wish 4; Test 1; Sub-task 1 | Closed 287; Open 12 |
| MRESOURCES | 288 | 53 | 0.3% | 92.7% | 64.2% | 51.4% | Bug 145; Improvement 83; New Feature 23; Dependency upgrade 18; Task 15; Wish 3; Test 1 | Closed 266; Open 20; Reopened 1; Resolved 1 |
| XAP | 288 | 0 | 0.0% | 0.0% | 14.9% | 0.0% | Bug 264; Improvement 16; Wish 5; Task 1; New Feature 1; Test 1 | Open 274; Reopened 14 |
| STRATOS | 283 | 0 | 0.7% | 0.0% | 31.1% | 53.7% | Bug 123; Improvement 110; Task 23; New Feature 19; Sub-task 8 | Open 266; In Progress 12; Reopened 5 |
| EAGLE | 282 | 4 | 8.2% | 1.4% | 68.4% | 45.0% | Bug 98; Improvement 96; New Feature 51; Sub-task 21; Task 15; Test 1 | Open 258; In Progress 14; Reopened 6; Closed 4 |
| IMAGING | 281 | 143 | 0.0% | 60.9% | 38.1% | 60.9% | Bug 144; Improvement 90; New Feature 20; Sub-task 14; Task 6; Wish 5; Test 2 | Closed 154; Open 107; Resolved 17; Reopened 2; In Progress 1 |
| CONNECTORS | 279 | 157 | 0.0% | 59.5% | 81.0% | 68.5% | Improvement 115; Bug 101; New Feature 29; Task 23; Test 6; Wish 4; Sub-task 1 | Resolved 164; Open 107; Patch Available 4; Closed 2; Reopened 1; In Progress 1 |
| NETBEANSINFRA | 277 | 119 | 0.7% | 70.4% | 42.6% | 75.5% | Sub-task 217; Bug 38; Task 11; Improvement 8; New Feature 2; Wish 1 | Resolved 101; Closed 94; Open 78; In Progress 4 |
| NEMO | 275 | 55 | 0.4% | 34.9% | 31.3% | 29.5% | Improvement 133; Bug 40; Task 31; New Feature 26; Sub-task 22; Umbrella 19; Test 2; Wish 2 | Open 178; Resolved 86; Closed 10; Reopened 1 |
| RIVER | 274 | 2 | 0.7% | 0.0% | 5.1% | 0.0% | Improvement 126; Bug 78; New Feature 26; Story 14; Sub-task 9; Task 7; Wish 6; Test 4; Question 2; Brainstorming 1; Epic 1 | Open 264; In Progress 6; Reopened 4 |
| LOG4NET | 271 | 56 | 0.4% | 22.1% | 9.6% | 33.2% | Bug 157; Improvement 56; New Feature 35; Wish 15; Task 7; Sub-task 1 | Open 201; Closed 44; Resolved 16; Reopened 7; In Progress 3 |
| LEGAL | 269 | 228 | 0.0% | 98.1% | 4.5% | 0.0% | Question 208; Task 61 | Closed 192; Resolved 72; Open 5 |
| PLC4X | 261 | 187 | 0.4% | 73.2% | 52.5% | 34.1% | Bug 144; Improvement 48; New Feature 37; Task 16; Sub-task 10; Wish 5; Test 1 | Resolved 97; Closed 94; Open 66; In Progress 3; Reopened 1 |
| FINCN | 258 | 158 | 0.8% | 10.9% | 12.0% | 0.0% | Improvement 119; Bug 71; New Feature 40; Task 16; Sub-task 11; Test 1 | Open 229; Resolved 18; Closed 10; In Progress 1 |
| XALANJ | 257 | 0 | 0.0% | 2.7% | 21.8% | 9.3% | Bug 201; Improvement 32; New Feature 18; Wish 2; Test 2; Task 2 | Open 241; Reopened 9; Resolved 5; Closed 2 |
| MINDEXER | 255 | 133 | 0.0% | 95.3% | 78.0% | 82.4% | Improvement 71; Bug 63; Dependency upgrade 57; Task 47; New Feature 13; Sub-task 2; Test 2 | Closed 243; Open 11; In Progress 1 |
| SINGA | 253 | 71 | 1.6% | 20.2% | 22.1% | 0.0% | Improvement 126; New Feature 62; Bug 49; Task 10; Test 4; Wish 2 | Open 202; Closed 44; Resolved 7 |
| MRM | 248 | 46 | 0.0% | 12.5% | 32.3% | 84.3% | Bug 98; Improvement 74; New Feature 41; Task 15; Wish 7; Sub-task 3; Question 3; Test 2; Dependency upgrade 2; Documentation 1; Project 1; Outage 1 | Open 209; Resolved 19; Closed 12; Reopened 4; In Progress 4 |
| STR | 246 | 0 | 0.0% | 0.8% | 7.3% | 58.9% | Improvement 178; Bug 48; New Feature 15; Task 5 | Open 215; Reopened 27; Closed 2; In Progress 2 |
| WHIMSY | 246 | 121 | 0.4% | 34.6% | 18.3% | 0.0% | Bug 110; Improvement 56; New Feature 53; Task 21; Wish 6 | Open 155; Resolved 64; Closed 21; Reopened 5; In Progress 1 |
| APEXCORE | 246 | 1 | 0.0% | 0.0% | 32.9% | 1.6% | Improvement 103; Bug 74; Task 24; Sub-task 19; New Feature 19; Documentation 4; Dependency upgrade 2; Wish 1 | Open 237; In Progress 7; Reopened 2 |
| SMXCOMP | 242 | 14 | 0.0% | 0.8% | 15.3% | 90.9% | Bug 124; Improvement 52; New Feature 36; Test 14; Wish 8; Task 7; Sub-task 1 | Open 228; Reopened 7; In Progress 5; Resolved 2 |
| ODE | 240 | 1 | 0.0% | 0.0% | 26.7% | 77.1% | Bug 131; Improvement 53; New Feature 30; Task 10; Wish 6; Sub-task 6; Test 4 | Open 233; Reopened 6; In Progress 1 |
| GORA | 238 | 71 | 0.4% | 44.5% | 48.7% | 79.8% | Improvement 116; Bug 51; New Feature 40; Task 20; Sub-task 6; Test 4; Wish 1 | Open 125; Resolved 83; Closed 23; In Progress 5; Patch Available 2 |
| COLLECTIONS | 234 | 157 | 0.0% | 63.2% | 24.8% | 58.5% | Improvement 89; Bug 73; New Feature 36; Sub-task 17; Wish 8; Test 6; Task 5 | Resolved 114; Open 77; Closed 34; Reopened 7; In Progress 2 |
| XERCESC | 233 | 80 | 0.0% | 31.8% | 31.3% | 32.6% | Bug 184; Improvement 34; Wish 7; New Feature 3; Task 3; Test 2 | Open 153; Closed 60; Resolved 14; Reopened 3; In Progress 3 |
| WEEX | 233 | 1 | 0.0% | 0.0% | 100.0% | 14.2% | Bug 143; Improvement 61; New Feature 15; Task 8; Wish 4; Sub-task 2 | Open 228; Reopened 3; In Progress 2 |
| CTAKES | 232 | 27 | 0.0% | 31.5% | 36.6% | 40.1% | Bug 93; Improvement 79; New Feature 26; Task 22; Wish 5; Test 4; Sub-task 3 | Open 153; Closed 63; Resolved 10; In Progress 3; Reopened 3 |
| SHINDIG | 231 | 0 | 0.0% | 1.7% | 13.4% | 13.4% | Bug 118; Improvement 58; New Feature 23; Sub-task 21; Question 6; Task 3; Wish 1; Test 1 | Open 207; Patch Available 11; Reopened 6; In Progress 4; Resolved 3 |
| MSKINS | 229 | 100 | 0.0% | 92.1% | 84.3% | 78.2% | Bug 75; Improvement 69; Task 32; New Feature 21; Dependency upgrade 20; Sub-task 8; Wish 4 | Closed 211; Open 16; Reopened 2 |
| TC | 227 | 0 | 0.4% | 0.0% | 25.6% | 33.5% | Improvement 115; Bug 76; New Feature 30; Task 3; Wish 2; Test 1 | Open 213; In Progress 14 |
| ANY23 | 225 | 136 | 0.4% | 80.0% | 65.3% | 95.6% | Improvement 136; Task 32; Bug 25; New Feature 15; Sub-task 12; Wish 4; Test 1 | Closed 115; Resolved 65; Open 44; In Progress 1 |
| PIVOT | 218 | 21 | 1.4% | 10.6% | 71.1% | 83.5% | Improvement 102; New Feature 48; Bug 40; Wish 21; Task 4; Sub-task 1; Brainstorming 1; Test 1 | Open 190; Resolved 13; Closed 10; Reopened 4; In Progress 1 |
| BEANUTILS | 215 | 49 | 0.0% | 23.7% | 14.4% | 65.6% | Bug 99; Improvement 86; New Feature 17; Wish 7; Task 5; Test 1 | Open 157; Resolved 33; Closed 18; Reopened 7 |
| EMPIREDB | 214 | 175 | 0.0% | 98.6% | 70.1% | 46.3% | Improvement 124; Bug 65; New Feature 21; Task 4 | Resolved 139; Closed 72; Open 3 |
| RYA | 214 | 15 | 3.7% | 9.8% | 50.9% | 15.9% | Bug 70; Improvement 70; New Feature 25; Task 21; Sub-task 20; Wish 5; Test 3 | Open 167; In Progress 24; Resolved 14; Closed 7; Reopened 2 |
| MANTRUN | 213 | 24 | 0.5% | 99.5% | 73.7% | 45.5% | Bug 126; Improvement 37; Dependency upgrade 18; New Feature 17; Task 11; Wish 3; Test 1 | Closed 211; Reopened 1; Resolved 1 |
| AWF | 213 | 38 | 0.0% | 46.9% | 29.6% | 0.0% | Bug 155; Improvement 26; Task 26; Brainstorming 2; Test 2; Story 2 | Closed 213 |
| CASSANALYTICS | 213 | 213 | 0.0% | 60.1% | 72.3% | 55.4% | Bug 67; Improvement 62; Task 42; New Feature 32; Epic 6; Sub-task 4 | Resolved 128; Triage Needed 62; Patch Available 7; Open 7; Ready to Commit 4; Awaiting Feedback 3; In Progress 1; Review In Progress 1 |
| WHIRR | 210 | 0 | 0.0% | 0.0% | 29.5% | 29.0% | Improvement 69; Bug 60; New Feature 58; Sub-task 15; Test 3; Wish 3; Task 2 | Open 187; Patch Available 19; In Progress 3; Reopened 1 |
| IBATIS | 208 | 0 | 0.0% | 0.0% | 1.9% | 0.5% | New Feature 122; Bug 78; Task 6; Test 2 | Open 203; Reopened 5 |
| NUMBERS | 208 | 77 | 0.0% | 90.9% | 24.5% | 80.3% | Improvement 64; Bug 53; Task 49; New Feature 26; Sub-task 7; Wish 7; Test 2 | Closed 179; Open 18; Resolved 10; Reopened 1 |
| MPH | 207 | 57 | 0.5% | 92.3% | 74.9% | 63.3% | Bug 69; Improvement 53; Dependency upgrade 37; Task 25; New Feature 19; Wish 3; Test 1 | Closed 190; Open 16; Resolved 1 |
| MINSTALL | 202 | 41 | 0.5% | 94.6% | 79.7% | 59.4% | Bug 84; Improvement 49; Dependency upgrade 28; Task 23; New Feature 15; Wish 2; Test 1 | Closed 190; Open 11; Resolved 1 |
| HTTPCORE | 197 | 175 | 0.0% | 97.5% | 8.6% | 60.4% | Bug 114; Improvement 64; New Feature 11; Task 3; Wish 3; Test 2 | Resolved 151; Closed 41; Open 5 |
| OWB | 196 | 164 | 0.0% | 91.8% | 71.4% | 80.1% | Bug 72; Task 52; Improvement 41; New Feature 9; Dependency upgrade 8; Sub-task 7; TCK Challenge 5; Question 1; Epic 1 | Closed 92; Resolved 88; Open 14; Reopened 2 |
| OMID | 193 | 168 | 0.0% | 66.3% | 82.9% | 57.5% | Bug 76; Improvement 54; Task 29; Sub-task 23; Wish 6; New Feature 3; Test 2 | Closed 79; Open 62; Resolved 49; Reopened 2; In Progress 1 |
| JXR | 192 | 51 | 0.5% | 97.4% | 81.8% | 75.0% | Bug 78; Improvement 51; Dependency upgrade 31; New Feature 17; Task 12; Wish 3 | Closed 187; Open 5 |
| TOREE | 192 | 64 | 0.0% | 34.4% | 30.7% | 35.9% | Bug 100; Improvement 42; Task 32; New Feature 11; Wish 4; Test 2; Sub-task 1 | Open 122; Resolved 56; Closed 7; In Progress 4; Reopened 3 |
| SPOT | 189 | 12 | 1.6% | 33.3% | 21.2% | 2.6% | Task 84; Bug 47; Improvement 32; New Feature 10; Epic 9; Wish 3; Sub-task 2; Test 2 | Open 122; Closed 51; Resolved 12; Reopened 2; In Progress 2 |
| ARIA | 178 | 0 | 0.0% | 0.0% | 7.9% | 0.0% | Story 111; Task 32; Bug 30; Sub-task 3; Epic 2 | Open 172; In Progress 6 |
| QPIDJMS | 177 | 151 | 0.0% | 83.6% | 68.4% | 70.1% | Task 82; Bug 59; Improvement 21; New Feature 11; Wish 2; Test 2 | Closed 140; Open 29; Resolved 8 |
| CONFIGURATION | 176 | 83 | 0.0% | 39.8% | 13.1% | 55.7% | Bug 95; Improvement 48; New Feature 16; Task 7; Sub-task 6; Wish 4 | Open 103; Resolved 38; Closed 32; Reopened 3 |
| OPENOFFICE | 175 | 22 | 0.0% | 16.6% | 89.7% | 0.0% | Sub-task 118; Task 48; Bug 8; Improvement 1 | Open 133; Closed 25; In Progress 13; Resolved 4 |
| TAPESTRY | 174 | 0 | 0.0% | 0.0% | 12.1% | 61.5% | Bug 107; Improvement 49; New Feature 9; Wish 8; Task 1 | Open 168; Reopened 4; In Progress 2 |
| JOHNZON | 174 | 143 | 0.0% | 85.1% | 51.7% | 87.4% | Bug 78; Improvement 41; Task 37; New Feature 8; Sub-task 8; Test 1; Wish 1 | Resolved 131; Open 24; Closed 17; In Progress 1; Reopened 1 |
| DIRAPI | 173 | 139 | 0.0% | 78.0% | 8.1% | 86.7% | Bug 113; Improvement 35; Task 11; New Feature 6; Question 4; Test 1; Documentation 1; Wish 1; Dependency upgrade 1 | Resolved 68; Closed 67; Open 38 |
| S4 | 172 | 34 | 0.6% | 100.0% | 41.9% | 65.7% | Bug 68; Improvement 46; New Feature 35; Task 14; Sub-task 6; Test 2; Wish 1 | Closed 172 |
| JDO | 165 | 77 | 0.0% | 69.1% | 68.5% | 63.0% | Improvement 55; Task 54; New Feature 28; Bug 25; Test 2; Wish 1 | Closed 71; Open 47; Resolved 43; In Progress 3; Reopened 1 |
| FTPSERVER | 162 | 25 | 0.0% | 11.7% | 15.4% | 37.0% | Bug 84; Improvement 38; New Feature 20; Wish 11; Task 9 | Open 141; Resolved 10; Closed 9; In Progress 1; Reopened 1 |
| VCL | 160 | 23 | 0.6% | 14.4% | 28.1% | 30.6% | Improvement 92; New Feature 32; Bug 15; Sub-task 8; Documentation 6; Task 4; Test 1; Question 1; Epic 1 | Open 128; Resolved 23; In Progress 8; Reopened 1 |
| BCEL | 159 | 36 | 0.0% | 56.6% | 47.8% | 45.9% | Bug 124; Improvement 23; Task 6; New Feature 3; Wish 2; Test 1 | Open 60; Resolved 49; Closed 41; Reopened 5; In Progress 4 |
| HCATALOG | 158 | 0 | 0.0% | 0.0% | 30.4% | 15.2% | Bug 82; Improvement 39; Sub-task 16; New Feature 10; Task 5; Test 4; Documentation 2 | Open 151; Reopened 4; Patch Available 2; In Progress 1 |
| FREEMARKER | 158 | 109 | 0.0% | 57.6% | 32.9% | 15.2% | Bug 72; Improvement 31; Task 31; New Feature 17; Wish 7 | Open 63; Closed 59; Resolved 32; In Progress 4 |
| MWRAPPER | 158 | 157 | 0.0% | 72.8% | 65.2% | 62.0% | Bug 81; Improvement 38; Task 14; Dependency upgrade 12; New Feature 9; Wish 4 | Closed 114; Open 40; Reopened 2; In Progress 1; Resolved 1 |
| STANBOL | 157 | 0 | 0.6% | 0.6% | 51.0% | 7.0% | Improvement 48; Bug 46; New Feature 27; Sub-task 11; Task 9; Wish 4; Test 3; Question 3; Story 2; Epic 2; Suitable Name Search 1; Documentation 1 | Open 150; In Progress 3; Reopened 3; Resolved 1 |
| LOGCXX | 155 | 65 | 0.6% | 97.4% | 61.9% | 48.4% | Bug 95; Improvement 41; New Feature 9; Wish 5; Task 4; Test 1 | Resolved 139; Closed 12; Open 4 |
| DIRKRB | 155 | 38 | 6.5% | 27.7% | 62.6% | 43.9% | Bug 45; New Feature 35; Improvement 34; Sub-task 24; Test 11; Task 5; Wish 1 | Open 106; Closed 24; Resolved 19; In Progress 5; Reopened 1 |
| DTACLOUD | 155 | 2 | 3.9% | 0.0% | 60.6% | 0.0% | Bug 114; Improvement 24; New Feature 5; Test 4; Task 3; Question 2; Dependency upgrade 1; Wish 1; New Git Repo 1 | Open 147; Reopened 7; In Progress 1 |
| STREAMS | 155 | 31 | 0.0% | 35.5% | 65.2% | 21.9% | Improvement 65; Task 32; Bug 28; New Feature 23; Story 4; Sub-task 2; Test 1 | Open 91; Resolved 50; In Progress 6; Closed 5; Reopened 3 |
| MRRESOURCES | 152 | 41 | 0.0% | 95.4% | 88.2% | 82.9% | Bug 58; Improvement 35; Dependency upgrade 30; New Feature 13; Task 13; Wish 3 | Closed 145; Open 4; Reopened 3 |
| LOG4PHP | 151 | 0 | 0.0% | 59.6% | 20.5% | 58.9% | Bug 63; Improvement 44; New Feature 23; Task 12; Wish 4; Question 3; Test 1; Documentation 1 | Closed 90; Open 61 |
| MCHANGELOG | 150 | 11 | 0.7% | 98.0% | 64.7% | 56.0% | Bug 76; Improvement 44; New Feature 12; Dependency upgrade 10; Task 6; Test 1; Wish 1 | Closed 147; Open 3 |
| BEEHIVE | 149 | 0 | 0.0% | 0.0% | 18.8% | 7.4% | Improvement 59; Bug 57; New Feature 20; Wish 6; Task 4; Test 3 | Open 145; Reopened 3; In Progress 1 |
| MYRIAD | 149 | 0 | 0.0% | 0.0% | 19.5% | 7.4% | Bug 78; Improvement 48; New Feature 13; Task 6; Sub-task 2; Test 2 | Open 104; Closed 37; In Progress 8 |
| BAHIR | 148 | 102 | 0.0% | 43.9% | 43.9% | 52.0% | Improvement 57; Bug 33; New Feature 22; Sub-task 12; Task 10; Wish 8; Test 6 | Open 83; Resolved 50; Closed 15 |
| SMX4 | 147 | 7 | 0.0% | 0.0% | 15.0% | 19.0% | Bug 51; Sub-task 31; Improvement 27; New Feature 25; Task 11; Wish 2 | Open 146; In Progress 1 |
| MGPG | 145 | 71 | 0.0% | 93.1% | 75.2% | 70.3% | Bug 56; Improvement 37; Dependency upgrade 24; New Feature 15; Task 7; Wish 5; Sub-task 1 | Closed 135; Open 8; In Progress 2 |
| CHUKWA | 145 | 0 | 1.4% | 0.0% | 28.3% | 0.7% | Improvement 58; New Feature 39; Bug 33; Sub-task 9; Task 3; Wish 2; Test 1 | Open 138; Reopened 4; Closed 1; In Progress 1; Patch Available 1 |
| SANTUARIO | 145 | 115 | 0.0% | 76.6% | 97.9% | 65.5% | Bug 71; Improvement 49; New Feature 14; Wish 5; Task 5; Test 1 | Closed 101; Open 34; Resolved 10 |
| ROCKETMQ | 144 | 0 | 0.0% | 0.0% | 95.8% | 32.6% | Bug 53; Improvement 47; New Feature 30; Wish 11; Task 3 | Open 124; In Progress 11; Reopened 9 |
| MSOURCES | 143 | 24 | 0.7% | 93.0% | 77.6% | 68.5% | Bug 52; Improvement 50; Dependency upgrade 15; New Feature 14; Task 8; Wish 4 | Closed 133; Open 9; In Progress 1 |
| METAMODEL | 143 | 16 | 0.7% | 2.1% | 8.4% | 0.7% | Bug 62; Improvement 41; New Feature 24; Task 8; Wish 6; Test 2 | Open 140; Resolved 3 |
| GRIFFIN | 142 | 61 | 0.0% | 22.5% | 34.5% | 24.6% | Bug 56; Improvement 42; Task 19; New Feature 10; Sub-task 6; Test 5; Wish 4 | Open 108; Resolved 23; Closed 9; In Progress 1; Reopened 1 |
| CSV | 141 | 75 | 0.0% | 61.0% | 8.5% | 62.4% | Bug 69; Improvement 51; New Feature 12; Wish 4; Task 2; Sub-task 2; Test 1 | Resolved 60; Open 53; Closed 26; Reopened 2 |
| SYNAPSE | 140 | 23 | 0.0% | 6.4% | 68.6% | 34.3% | Improvement 59; Bug 36; New Feature 24; Sub-task 9; Task 6; Test 3; Wish 3 | Open 125; Resolved 7; Reopened 3; In Progress 3; Closed 2 |
| HAMA | 140 | 0 | 0.7% | 0.7% | 27.9% | 10.7% | Improvement 38; New Feature 34; Sub-task 29; Bug 18; Task 9; Umbrella 6; Documentation 4; Question 1; Wish 1 | Open 130; Reopened 5; Patch Available 3; Resolved 1; In Progress 1 |
| GEARPUMP | 140 | 0 | 0.7% | 0.0% | 47.9% | 7.9% | Improvement 47; New Feature 41; Bug 21; Sub-task 18; Task 9; Test 2; Wish 2 | Open 135; In Progress 5 |
| PLUTO | 139 | 24 | 0.0% | 87.1% | 97.8% | 85.6% | Bug 82; Task 36; Improvement 16; Test 2; New Feature 2; Wish 1 | Closed 120; Open 18; Resolved 1 |
| FLAGON | 138 | 12 | 27.5% | 13.8% | 65.9% | 60.1% | Task 41; Improvement 28; Bug 18; New Feature 16; Wish 15; Sub-task 14; Test 6 | Open 103; In Progress 14; Resolved 10; Closed 9; Reopened 2 |
| ODFTOOLKIT | 137 | 0 | 0.0% | 0.0% | 54.7% | 3.6% | Bug 89; Improvement 42; New Feature 3; Wish 2; Task 1 | Open 130; In Progress 4; Reopened 3 |
| MARMOTTA | 137 | 2 | 8.0% | 0.0% | 53.3% | 33.6% | Improvement 44; Bug 40; New Feature 19; Task 18; Wish 12; Sub-task 2; Test 2 | Open 130; In Progress 4; Reopened 3 |
| COMDEV | 137 | 102 | 0.0% | 84.7% | 9.5% | 0.0% | Bug 58; Improvement 32; Task 20; New Feature 7; Wish 5; Question 5; IT Help 2; Proposal 2; Project 2; SVN->GIT Migration 1; Umbrella 1; Documentation 1; Outage 1 | Resolved 60; Closed 56; Open 21 |
| CASSJAVA | 136 | 136 | 0.0% | 52.9% | 58.8% | 39.0% | Improvement 59; Bug 50; Task 15; Sub-task 6; New Feature 5; Epic 1 | Resolved 72; Triage Needed 54; Open 7; In Progress 1; Awaiting Feedback 1; Patch Available 1 |
| CASSGO | 136 | 136 | 0.0% | 69.1% | 55.1% | 77.2% | Improvement 50; Bug 42; New Feature 21; Task 16; Sub-task 7 | Resolved 94; Triage Needed 16; Patch Available 9; Open 9; In Progress 2; Review In Progress 2; Ready to Commit 2; Needs Committer 1; Changes Suggested 1 |
| NET | 135 | 69 | 0.0% | 59.3% | 3.0% | 38.5% | Bug 86; Improvement 33; Wish 6; New Feature 5; Task 4; Test 1 | Open 55; Resolved 42; Closed 38 |
| DUBBO | 133 | 108 | 0.0% | 47.4% | 0.8% | 0.0% | Task 75; Improvement 42; New Feature 9; Bug 4; Wish 2; Test 1 | Open 70; Closed 62; Resolved 1 |
| GEOMETRY | 130 | 70 | 0.0% | 83.1% | 11.5% | 31.5% | Improvement 45; Task 30; New Feature 30; Bug 18; Wish 6; Test 1 | Closed 104; Open 21; Resolved 4; Reopened 1 |
| CLI | 129 | 54 | 0.0% | 34.9% | 17.8% | 41.1% | Bug 63; Improvement 46; New Feature 12; Task 5; Wish 3 | Open 74; Resolved 33; Closed 12; Reopened 9; In Progress 1 |
| VALIDATOR | 129 | 50 | 0.0% | 84.5% | 7.0% | 55.8% | Bug 59; Improvement 43; New Feature 13; Task 11; Wish 3 | Resolved 66; Closed 43; Open 19; Reopened 1 |
| MEJB | 128 | 13 | 0.8% | 98.4% | 83.6% | 75.8% | Improvement 52; Bug 36; Task 17; Dependency upgrade 12; New Feature 10; Test 1 | Closed 126; Reopened 2 |
| DIRMINA | 126 | 82 | 0.0% | 64.3% | 38.1% | 45.2% | Bug 86; Improvement 23; Wish 7; Task 6; New Feature 3; Test 1 | Resolved 59; Open 43; Closed 22; In Progress 1; Reopened 1 |
| TEPHRA | 126 | 16 | 0.0% | 17.5% | 100.0% | 19.8% | Improvement 59; Bug 28; New Feature 14; Task 13; Sub-task 11; Wish 1 | Open 103; Closed 17; Resolved 5; Reopened 1 |
| MEECROWAVE | 126 | 122 | 0.0% | 98.4% | 88.1% | 95.2% | Task 88; Improvement 19; Bug 17; New Feature 1; Wish 1 | Resolved 121; Closed 3; Open 2 |
| MBUILDCACHE | 124 | 124 | 0.0% | 58.1% | 41.1% | 50.0% | Bug 54; Improvement 28; Sub-task 15; New Feature 13; Task 6; Dependency upgrade 5; Wish 3 | Closed 72; Open 52 |
| DDLUTILS | 122 | 0 | 0.0% | 0.0% | 100.0% | 46.7% | Bug 51; Improvement 35; New Feature 28; Sub-task 3; Wish 3; Task 2 | Open 121; In Progress 1 |
| XW | 121 | 0 | 0.0% | 0.0% | 16.5% | 53.7% | Bug 50; Improvement 44; New Feature 19; Task 7; Question 1 | Open 117; Reopened 2; In Progress 2 |
| MCLEAN | 120 | 40 | 0.0% | 99.2% | 85.0% | 75.8% | Improvement 42; Bug 37; Dependency upgrade 16; Task 14; New Feature 10; Sub-task 1 | Closed 117; Resolved 2; Open 1 |
| JUNEAU | 119 | 95 | 0.0% | 97.5% | 53.8% | 60.5% | Improvement 64; Bug 30; Task 14; New Feature 11 | Closed 106; Resolved 10; Open 3 |
| MIME4J | 117 | 43 | 0.0% | 49.6% | 4.3% | 59.8% | Bug 49; Improvement 36; New Feature 13; Task 11; Wish 7; Test 1 | Open 56; Closed 55; Resolved 3; Reopened 3 |
| CLIMATE | 117 | 3 | 12.0% | 0.9% | 74.4% | 93.2% | Improvement 52; Bug 37; New Feature 12; Task 5; Sub-task 5; Dependency upgrade 2; Umbrella 1; Wish 1; Documentation 1; Test 1 | Open 110; In Progress 5; Reopened 1; Closed 1 |
| SHALE | 116 | 0 | 0.0% | 0.0% | 12.9% | 55.2% | Improvement 51; Bug 31; New Feature 23; Task 10; Sub-task 1 | Open 114; Reopened 1; In Progress 1 |
| JS1 | 112 | 4 | 0.0% | 0.0% | 12.5% | 0.9% | Bug 105; Improvement 3; New Feature 2; Test 1; Wish 1 | Open 109; Reopened 3 |
| FILEUPLOAD | 112 | 64 | 0.9% | 67.9% | 16.1% | 26.8% | Bug 51; Improvement 28; Sub-task 19; Wish 8; New Feature 3; Task 2; Test 1 | Resolved 43; Open 35; Closed 33; Reopened 1 |
| FC | 112 | 63 | 0.9% | 59.8% | 63.4% | 59.8% | Improvement 69; Bug 30; New Feature 6; Task 4; Test 1; Sub-task 1; Wish 1 | Open 45; Resolved 41; Closed 26 |
| GERONIMODEVTOOLS | 110 | 0 | 0.0% | 0.0% | 59.1% | 42.7% | Bug 47; Improvement 26; Sub-task 23; Task 5; New Feature 4; Wish 4; Test 1 | Open 101; In Progress 5; Reopened 4 |
| RAMPART | 110 | 14 | 0.0% | 40.0% | 42.7% | 45.5% | Bug 71; Improvement 17; New Feature 10; Question 6; Request 2; Wish 1; Sub-task 1; Documentation 1; Task 1 | Open 66; Resolved 44 |
| WAVE | 109 | 0 | 0.0% | 0.0% | 14.7% | 1.8% | Bug 67; Improvement 26; New Feature 8; Task 5; Wish 1; Epic 1; Dependency upgrade 1 | Open 101; Reopened 5; In Progress 3 |
| VXQUERY | 108 | 1 | 0.0% | 0.9% | 51.9% | 1.9% | Bug 53; Task 20; Improvement 16; Sub-task 11; New Feature 6; Test 2 | Open 105; Reopened 1; In Progress 1; Resolved 1 |
| ZETACOMP | 108 | 2 | 0.0% | 100.0% | 19.4% | 0.0% | Bug 63; Improvement 22; New Feature 11; Sub-task 5; Task 4; Wish 2; Question 1 | Closed 108 |
| JS2 | 105 | 4 | 1.9% | 2.9% | 35.2% | 21.0% | Bug 44; Improvement 26; New Feature 21; Task 6; Sub-task 4; Wish 4 | Open 97; In Progress 5; Closed 2; Resolved 1 |
| CRUNCH | 104 | 7 | 0.0% | 4.8% | 53.8% | 9.6% | Bug 48; Improvement 40; Task 5; New Feature 4; Wish 4; Sub-task 2; Test 1 | Open 95; Resolved 4; Reopened 2; In Progress 2; Closed 1 |
| CMIS | 103 | 16 | 0.0% | 2.9% | 29.1% | 14.6% | Bug 42; Improvement 29; New Feature 9; Wish 9; Task 7; Sub-task 6; Test 1 | Open 90; In Progress 5; Patch Available 3; Resolved 3; Reopened 2 |
| AMQNET | 103 | 63 | 0.0% | 34.0% | 26.2% | 35.9% | Bug 56; New Feature 20; Improvement 18; Task 5; Wish 2; Test 1; Dependency upgrade 1 | Open 63; Resolved 29; Closed 6; In Progress 3; Reopened 2 |
| JELLY | 102 | 0 | 0.0% | 0.0% | 13.7% | 10.8% | Bug 49; Improvement 27; New Feature 21; Wish 3; Task 2 | Open 100; Reopened 2 |
| XALANC | 102 | 31 | 5.9% | 32.4% | 87.3% | 43.1% | Bug 81; Improvement 12; Task 5; New Feature 2; Wish 2 | Open 67; Resolved 29; Closed 4; In Progress 2 |
| CODEC | 102 | 69 | 0.0% | 72.5% | 17.6% | 56.9% | Bug 49; Improvement 33; New Feature 11; Wish 5; Sub-task 3; Task 1 | Resolved 53; Open 24; Closed 21; Reopened 4 |
| PODLINGNAMESEARCH | 101 | 84 | 0.0% | 100.0% | 3.0% | 0.0% | Suitable Name Search 101 | Resolved 93; Closed 8 |
| LIMINAL | 100 | 100 | 0.0% | 51.0% | 60.0% | 84.0% | New Feature 33; Improvement 30; Bug 23; Task 5; Test 4; Sub-task 4; Wish 1 | Open 48; Closed 38; Resolved 13; In Progress 1 |
| AGE2 | 98 | 98 | 3.1% | 64.3% | 55.1% | 29.6% | Task 43; New Feature 22; Improvement 16; Bug 10; Epic 6; Sub-task 1 | Done 63; To Do 30; In Progress 4; In Review 1 |
| RNG | 97 | 76 | 0.0% | 88.7% | 37.1% | 82.5% | Improvement 35; New Feature 31; Bug 18; Task 6; Wish 4; Sub-task 3 | Closed 77; Open 11; Resolved 9 |
| WSS | 96 | 70 | 0.0% | 88.5% | 97.9% | 65.6% | Bug 41; Improvement 36; Task 11; New Feature 6; Wish 2 | Closed 44; Resolved 41; Open 11 |
| CACTUS | 95 | 0 | 0.0% | 0.0% | 16.8% | 4.2% | Bug 39; Improvement 36; New Feature 12; Wish 4; Task 4 | Open 91; Reopened 2; In Progress 2 |
| SCIMPLE | 95 | 12 | 0.0% | 49.5% | 13.7% | 0.0% | Bug 87; Improvement 4; New Feature 3; Task 1 | Open 48; Closed 40; Resolved 7 |
| TEXT | 94 | 66 | 0.0% | 57.4% | 24.5% | 68.1% | Bug 38; Improvement 28; Sub-task 13; New Feature 10; Wish 3; Task 2 | Resolved 40; Open 37; Closed 14; In Progress 2; Reopened 1 |
| BLUR | 94 | 0 | 0.0% | 1.1% | 6.4% | 11.7% | Improvement 47; Bug 17; New Feature 16; Sub-task 9; Task 2; Test 2; Wish 1 | Open 93; Resolved 1 |
| SANDBOX | 93 | 4 | 0.0% | 2.2% | 10.8% | 4.3% | Improvement 30; Bug 20; Task 17; New Feature 13; Sub-task 11; Wish 2 | Open 89; Reopened 2; Resolved 2 |
| AXISCPP | 92 | 0 | 0.0% | 1.1% | 3.3% | 7.6% | Bug 45; Improvement 19; New Feature 16; Test 5; Wish 4; Sub-task 2; Task 1 | Open 88; Reopened 3; Closed 1 |
| MPLUGINTESTING | 92 | 31 | 0.0% | 94.6% | 67.4% | 59.8% | Bug 37; Improvement 23; Dependency upgrade 13; Task 12; New Feature 6; Wish 1 | Closed 86; Open 5; Resolved 1 |
| MJLINK | 91 | 50 | 0.0% | 95.6% | 80.2% | 80.2% | Dependency upgrade 32; Improvement 27; Bug 18; New Feature 9; Task 5 | Closed 85; Open 4; Resolved 2 |
| MRAR | 89 | 10 | 1.1% | 97.8% | 88.8% | 77.5% | Dependency upgrade 37; Improvement 22; Bug 16; New Feature 9; Task 3; Test 1; Wish 1 | Closed 87; Open 2 |
| XBEAN | 89 | 43 | 0.0% | 51.7% | 39.3% | 51.7% | Bug 44; Improvement 25; Task 11; New Feature 4; Wish 3; Sub-task 1; Test 1 | Open 42; Closed 37; Resolved 9; Patch Available 1 |
| STATISTICS | 89 | 67 | 0.0% | 89.9% | 21.3% | 80.9% | New Feature 22; Improvement 21; Sub-task 18; Bug 13; Task 12; Wish 2; Test 1 | Closed 74; Open 9; Resolved 6 |
| VELOCITY | 88 | 77 | 0.0% | 90.9% | 64.8% | 51.1% | Bug 54; Improvement 16; Task 10; Wish 5; New Feature 3 | Closed 67; Resolved 13; Open 8 |
| HIVEMALL | 88 | 29 | 0.0% | 25.0% | 61.4% | 54.5% | Improvement 23; Wish 19; New Feature 15; Bug 14; Sub-task 8; Task 8; Test 1 | Open 62; Closed 21; In Progress 4; Resolved 1 |
| NIFIREG | 88 | 59 | 0.0% | 97.7% | 89.8% | 86.4% | Improvement 43; Bug 23; Task 16; Test 3; New Feature 2; Wish 1 | Resolved 82; Closed 4; Open 2 |
| S2GRAPH | 87 | 4 | 36.8% | 100.0% | 60.9% | 17.2% | Improvement 29; Bug 16; New Feature 13; Sub-task 13; Task 11; Wish 4; Test 1 | Done 87 |
| EDGENT | 87 | 0 | 1.1% | 100.0% | 24.1% | 3.4% | Improvement 31; Bug 21; Task 14; New Feature 13; Wish 5; Test 3 | Closed 87 |
| ROL | 85 | 23 | 0.0% | 58.8% | 58.8% | 5.9% | Bug 43; Improvement 26; New Feature 5; Task 5; Wish 5; Documentation 1 | Closed 42; Open 34; Resolved 8; Reopened 1 |
| VYSPER | 85 | 1 | 0.0% | 0.0% | 34.1% | 8.2% | Sub-task 23; Bug 21; New Feature 17; Improvement 17; Task 3; Question 2; Wish 1; Dependency upgrade 1 | Open 79; In Progress 5; Reopened 1 |
| BATCHEE | 85 | 65 | 0.0% | 81.2% | 32.9% | 69.4% | Task 46; Bug 21; Improvement 9; New Feature 7; Wish 2 | Resolved 67; Open 16; Closed 2 |
| DAEMON | 84 | 65 | 1.2% | 83.3% | 8.3% | 52.4% | Bug 55; Improvement 18; New Feature 8; Task 3 | Resolved 63; Open 14; Closed 7 |
| JCS | 84 | 49 | 0.0% | 100.0% | 84.5% | 91.7% | Bug 48; Sub-task 17; Improvement 13; Question 3; Task 2; Dependency upgrade 1 | Closed 70; Resolved 14 |
| ATTIC | 83 | 75 | 0.0% | 92.8% | 45.8% | 0.0% | Task 63; Bug 7; Improvement 6; New Feature 4; Wish 1; Project 1; Question 1 | Closed 67; Resolved 10; Open 6 |
| MARTIFACT | 83 | 83 | 0.0% | 85.5% | 78.3% | 81.9% | Improvement 25; New Feature 19; Bug 19; Task 10; Wish 6; Dependency upgrade 4 | Closed 70; Open 12; Resolved 1 |
| HIVEMIND | 81 | 0 | 0.0% | 0.0% | 1.2% | 6.2% | Bug 34; New Feature 21; Improvement 21; Wish 2; Task 2; Test 1 | Open 80; Reopened 1 |
| MODPYTHON | 81 | 0 | 0.0% | 0.0% | 19.8% | 8.6% | Bug 40; Improvement 18; New Feature 13; Task 8; Wish 2 | Open 72; In Progress 6; Reopened 3 |
| MTOMCAT | 81 | 10 | 1.2% | 17.3% | 69.1% | 35.8% | Bug 55; Improvement 12; New Feature 4; Wish 3; Dependency upgrade 2; Question 2; Task 1; Documentation 1; Request 1 | Open 67; Resolved 8; Closed 6 |
| TWILL | 81 | 2 | 0.0% | 12.3% | 34.6% | 14.8% | Bug 31; Improvement 31; New Feature 8; Task 8; Story 2; Sub-task 1 | Open 69; Resolved 10; In Progress 2 |
| DELTASPIKE | 80 | 1 | 0.0% | 58.8% | 67.5% | 21.2% | Improvement 29; Bug 22; New Feature 15; Task 10; Sub-task 2; Test 1; Wish 1 | Closed 34; Open 30; Resolved 13; In Progress 2; Reopened 1 |
| MARCHETYPES | 78 | 21 | 0.0% | 92.3% | 61.5% | 48.7% | Improvement 26; Bug 25; Task 14; Sub-task 7; New Feature 2; Wish 2; Dependency upgrade 2 | Closed 72; Open 6 |
| OGNL | 77 | 1 | 0.0% | 20.8% | 44.2% | 35.1% | Bug 43; Improvement 16; Sub-task 8; Task 6; New Feature 4 | Open 57; Resolved 9; Closed 7; Reopened 4 |
| APLO | 77 | 6 | 0.0% | 100.0% | 7.8% | 40.3% | Bug 45; Improvement 13; New Feature 8; Wish 4; Question 4; Task 1; Dependency upgrade 1; Test 1 | Closed 77 |
| CLK | 74 | 0 | 0.0% | 0.0% | 64.9% | 64.9% | Improvement 42; New Feature 21; Bug 9; Task 1; Brainstorming 1 | Open 64; In Progress 5; Reopened 5 |
| ETCH | 74 | 0 | 2.7% | 0.0% | 9.5% | 27.0% | Task 24; Bug 20; New Feature 18; Improvement 12 | Open 72; In Progress 2 |
| WINK | 74 | 0 | 0.0% | 0.0% | 12.2% | 18.9% | Bug 43; Improvement 16; New Feature 6; Test 3; Question 2; Wish 1; Task 1; Story 1; Dependency upgrade 1 | Open 73; In Progress 1 |
| MJARSIGNER | 73 | 18 | 0.0% | 93.2% | 74.0% | 69.9% | Improvement 20; Bug 19; New Feature 14; Dependency upgrade 11; Task 8; Wish 1 | Closed 67; Open 5; Resolved 1 |
| BOOKKEEPER | 73 | 0 | 1.4% | 0.0% | 65.8% | 19.2% | Improvement 31; Bug 24; New Feature 8; Sub-task 3; Documentation 3; Task 2; Wish 1; Test 1 | Open 64; Reopened 3; In Progress 3; Patch Available 2; Closed 1 |
| QPIDIT | 73 | 8 | 0.0% | 42.5% | 97.3% | 34.2% | Bug 28; Task 22; Improvement 17; New Feature 5; Test 1 | Open 41; Closed 23; Resolved 8; In Progress 1 |
| HTTPDRAFT | 71 | 0 | 0.0% | 0.0% | 100.0% | 0.0% | Bug 47; Improvement 24 | Open 71 |
| OODT | 71 | 7 | 0.0% | 8.5% | 66.2% | 47.9% | Improvement 25; Bug 22; Sub-task 18; Task 2; Umbrella 1; Epic 1; New Feature 1; Question 1 | Open 64; Resolved 4; Closed 2; Reopened 1 |
| STEVE | 71 | 29 | 0.0% | 0.0% | 1.4% | 0.0% | Bug 42; Improvement 25; New Feature 3; Wish 1 | Open 70; In Progress 1 |
| INCUBATOR | 70 | 44 | 0.0% | 62.9% | 20.0% | 0.0% | Task 32; Bug 21; Improvement 14; New Feature 2; Wish 1 | Closed 40; Open 26; Resolved 4 |
| POOL | 70 | 46 | 0.0% | 65.7% | 11.4% | 70.0% | Improvement 31; Bug 30; New Feature 4; Task 4; Test 1 | Closed 28; Open 24; Resolved 18 |
| MSCMPUB | 70 | 28 | 0.0% | 94.3% | 74.3% | 75.7% | Improvement 26; Bug 19; Dependency upgrade 16; New Feature 5; Task 4 | Closed 65; Open 4; Resolved 1 |
| ESME | 69 | 0 | 1.4% | 0.0% | 27.5% | 97.1% | New Feature 23; Improvement 18; Bug 14; Task 7; Sub-task 4; Test 2; Wish 1 | Open 67; In Progress 2 |
| HTRACE | 69 | 0 | 0.0% | 0.0% | 39.1% | 1.4% | Improvement 31; Bug 20; New Feature 8; Task 8; Sub-task 1; Test 1 | Open 63; In Progress 6 |
| DL | 68 | 0 | 0.0% | 0.0% | 32.4% | 35.3% | New Feature 18; Task 16; Improvement 13; Bug 11; Sub-task 9; Test 1 | Open 60; In Progress 8 |
| DATAFU | 66 | 38 | 0.0% | 86.4% | 62.1% | 42.4% | Improvement 26; New Feature 18; Bug 12; Task 7; Test 3 | Closed 49; Open 9; Resolved 8 |
| MDOAP | 65 | 13 | 0.0% | 93.8% | 83.1% | 84.6% | Bug 21; Improvement 19; Dependency upgrade 13; Task 7; New Feature 4; Wish 1 | Closed 60; Open 4; Resolved 1 |
| DMAP | 65 | 0 | 1.5% | 100.0% | 60.0% | 23.1% | Improvement 34; Bug 15; Task 6; Epic 3; Sub-task 2; New Feature 1; Story 1; Test 1; Question 1; Technical task 1 | Closed 65 |
| IVYDE | 64 | 5 | 0.0% | 0.0% | 10.9% | 7.8% | Bug 43; Improvement 10; New Feature 10; Proposal 1 | Open 63; Reopened 1 |
| MUSE | 64 | 0 | 3.1% | 0.0% | 100.0% | 53.1% | Bug 48; New Feature 8; Improvement 4; Task 2; Sub-task 2 | Open 63; Reopened 1 |
| DBCP | 64 | 39 | 0.0% | 67.2% | 9.4% | 48.4% | Bug 38; Improvement 16; New Feature 4; Sub-task 4; Task 1; Wish 1 | Closed 22; Resolved 21; Open 20; Reopened 1 |
| AGEOLD | 64 | 64 | 1.6% | 34.4% | 0.0% | 0.0% | Bug 18; Sub-task 15; Task 14; Test 9; Improvement 6; New Feature 2 | Open 42; Closed 20; Resolved 2 |
| DOXIATOOLS | 63 | 27 | 0.0% | 92.1% | 52.4% | 52.4% | Bug 25; Improvement 18; Dependency upgrade 12; New Feature 5; Task 3 | Closed 52; Resolved 6; Open 3; In Progress 2 |
| MAILBOX | 63 | 15 | 0.0% | 54.0% | 27.0% | 15.9% | Bug 24; Improvement 22; New Feature 10; Sub-task 4; Task 3 | Closed 33; Open 26; In Progress 3; Resolved 1 |
| TST | 61 | 10 | 0.0% | 86.9% | 14.8% | 24.6% | Bug 43; Test 4; Improvement 4; Task 3; Wish 2; New Feature 2; Sub-task 2; Proposal 1 | Open 34; Resolved 20; Triage Needed 6; Idea 1 |
| SERF | 61 | 16 | 0.0% | 68.9% | 8.2% | 36.1% | Bug 55; Improvement 4; Task 2 | Closed 34; Open 17; Resolved 8; In Progress 1; Reopened 1 |
| COMMONSSITE | 61 | 36 | 0.0% | 42.6% | 11.5% | 8.2% | Bug 26; Improvement 17; New Feature 13; Task 4; Wish 1 | Open 32; Closed 15; Resolved 11; Reopened 3 |
| POLYGENE | 61 | 0 | 0.0% | 0.0% | 13.1% | 24.6% | New Feature 21; Bug 14; Improvement 13; Task 6; Wish 4; Sub-task 3 | Open 58; Reopened 2; In Progress 1 |
| MINIFI | 61 | 20 | 0.0% | 98.4% | 83.6% | 82.0% | Improvement 30; Bug 18; New Feature 6; Task 6; Test 1 | Resolved 57; Closed 3; Open 1 |
| MTOOLCHAINS | 60 | 34 | 0.0% | 75.0% | 63.3% | 55.0% | Improvement 20; Bug 19; Task 10; Dependency upgrade 8; New Feature 2; Wish 1 | Closed 45; Open 14; In Progress 1 |
| MASFRES | 60 | 39 | 0.0% | 100.0% | 46.7% | 38.3% | Bug 22; Improvement 18; Sub-task 7; Task 4; Dependency upgrade 3; Wish 2; New Feature 2; Test 2 | Closed 58; Resolved 2 |
| JOSHUA | 60 | 2 | 0.0% | 0.0% | 26.7% | 88.3% | Bug 31; Improvement 19; New Feature 6; Task 4 | Open 31; Reopened 28; In Progress 1 |
| LABS | 59 | 2 | 0.0% | 1.7% | 93.2% | 89.8% | Improvement 20; New Feature 14; Task 10; Bug 10; Wish 4; Story 1 | Open 52; Reopened 4; In Progress 2; Closed 1 |
| WODEN | 58 | 1 | 1.7% | 0.0% | 62.1% | 41.4% | Bug 33; Improvement 17; New Feature 5; Test 1; Wish 1; Task 1 | Open 54; Reopened 2; In Progress 2 |
| RIPPLE | 58 | 0 | 0.0% | 1.7% | 12.1% | 0.0% | Bug 39; Improvement 8; Question 4; Task 3; New Feature 2; Sub-task 1; Wish 1 | Open 55; In Progress 2; Closed 1 |
| HORN | 57 | 22 | 0.0% | 100.0% | 43.9% | 0.0% | Bug 13; Improvement 12; New Feature 11; Wish 10; Task 8; Sub-task 3 | Closed 57 |
| MACR | 56 | 6 | 0.0% | 98.2% | 96.4% | 94.6% | Improvement 22; Dependency upgrade 21; Task 7; Bug 4; New Feature 2 | Closed 55; Reopened 1 |
| WAYANG | 56 | 56 | 0.0% | 48.2% | 58.9% | 0.0% | Improvement 13; New Feature 12; Sub-task 11; Task 10; Bug 9; Test 1 | Open 27; Resolved 15; Closed 12; In Progress 2 |
| QUICKSTEP | 55 | 0 | 3.6% | 0.0% | 20.0% | 0.0% | Improvement 29; Bug 10; New Feature 7; Task 3; Test 2; Sub-task 2; Wish 2 | Open 55 |
| IBATISNET | 54 | 0 | 5.6% | 0.0% | 13.0% | 11.1% | Bug 28; Improvement 16; New Feature 5; Wish 3; Task 1; Test 1 | Open 50; In Progress 4 |
| SIRONA | 54 | 0 | 0.0% | 100.0% | 81.5% | 79.6% | Bug 26; New Feature 18; Improvement 7; Task 2; Wish 1 | Closed 54 |
| XGC | 53 | 28 | 0.0% | 34.0% | 47.2% | 34.0% | Bug 40; Improvement 7; Task 4; New Feature 2 | Open 33; Resolved 16; Reopened 2; Closed 2 |
| JUDDI | 53 | 21 | 0.0% | 52.8% | 77.4% | 73.6% | Improvement 22; Bug 22; New Feature 4; Wish 2; Sub-task 2; Task 1 | Open 23; Closed 20; Resolved 8; In Progress 2 |
| SANDESHA2 | 52 | 0 | 0.0% | 0.0% | 1.9% | 3.8% | Bug 34; Improvement 16; New Feature 2 | Open 52 |
| AMQCPP | 52 | 29 | 0.0% | 11.5% | 92.3% | 7.7% | Bug 35; Improvement 11; New Feature 4; Test 1; Task 1 | Open 44; Closed 4; Resolved 2; Reopened 2 |
| CRYPTO | 52 | 37 | 0.0% | 84.6% | 13.5% | 28.8% | Bug 25; Improvement 14; New Feature 7; Task 3; Sub-task 2; Wish 1 | Resolved 39; Open 8; Closed 5 |
| ABDERA | 51 | 0 | 0.0% | 0.0% | 9.8% | 13.7% | Bug 35; Improvement 12; Question 2; New Feature 1; Dependency upgrade 1 | Open 49; Reopened 2 |
| PIO | 51 | 1 | 0.0% | 3.9% | 29.4% | 3.9% | Improvement 23; Bug 13; New Feature 7; Task 6; Sub-task 1; Wish 1 | Open 49; Closed 2 |
| PORTLETBRIDGE | 50 | 0 | 0.0% | 44.0% | 90.0% | 10.0% | New Feature 20; Bug 17; TCK Challenge 6; Improvement 4; Question 2; Task 1 | Open 26; Closed 16; Resolved 6; Patch Available 2 |
| WSIF | 49 | 0 | 0.0% | 0.0% | 16.3% | 20.4% | Bug 42; New Feature 3; Improvement 3; Task 1 | Open 48; Reopened 1 |
| EXEC | 49 | 14 | 0.0% | 30.6% | 30.6% | 26.5% | Bug 31; Improvement 9; Sub-task 4; New Feature 3; Wish 2 | Open 28; Closed 11; Resolved 4; In Progress 3; Reopened 3 |
| WOOKIE | 49 | 0 | 0.0% | 2.0% | 10.2% | 61.2% | Improvement 23; Bug 14; New Feature 8; Task 3; Sub-task 1 | Open 20; Closed 11; Reviewable 7; In Progress 4; Blocked 3; Patch Available 3; Resolved 1 |
| MARVIN | 49 | 11 | 0.0% | 6.1% | 18.4% | 36.7% | New Feature 15; Improvement 15; Bug 12; Task 4; Wish 2; Sub-task 1 | To Do 38; In Progress 4; In Review 4; Done 3 |
| JXPATH | 48 | 11 | 0.0% | 2.1% | 2.1% | 18.8% | Bug 31; Improvement 14; New Feature 1; Wish 1; Task 1 | Open 41; Reopened 6; Resolved 1 |
| ACE | 47 | 0 | 0.0% | 0.0% | 14.9% | 8.5% | Improvement 22; Bug 15; Task 3; New Feature 2; Documentation 2; Question 2; IT Help 1 | Open 47 |
| DIRECTMEMORY | 47 | 0 | 0.0% | 0.0% | 21.3% | 31.9% | Improvement 18; Task 11; New Feature 11; Bug 6; Wish 1 | Open 42; In Progress 5 |
| LUCENENET | 47 | 13 | 0.0% | 97.9% | 17.0% | 21.3% | Improvement 16; Task 14; Bug 13; Wish 2; Sub-task 1; Test 1 | Closed 29; Resolved 17; Open 1 |
| FEDIZ | 47 | 16 | 0.0% | 38.3% | 38.3% | 40.4% | Improvement 17; New Feature 10; Bug 10; Task 5; Test 2; Dependency upgrade 2; Wish 1 | Open 29; Closed 15; Resolved 3 |
| CLOUDSTACK | 47 | 28 | 0.0% | 6.4% | 4.3% | 6.4% | New Feature 26; Improvement 9; Wish 7; Bug 4; Sub-task 1 | Open 44; Closed 2; Resolved 1 |
| PNIX | 46 | 0 | 0.0% | 0.0% | 4.3% | 32.6% | New Feature 28; Improvement 11; Bug 4; Task 2; Wish 1 | Open 46 |
| CHAINSAW | 46 | 11 | 0.0% | 13.0% | 10.9% | 8.7% | Bug 28; Improvement 12; Test 4; Task 1; New Feature 1 | Open 39; Closed 6; Reopened 1 |
| OCM | 45 | 2 | 0.0% | 0.0% | 13.3% | 13.3% | Bug 25; Improvement 8; Task 5; New Feature 5; Wish 2 | Open 38; Patch Available 7 |
| NIP | 45 | 45 | 0.0% | 64.4% | 82.2% | 0.0% | Improvement 26; New Feature 19 | Resolved 28; Open 12; In Progress 4; Closed 1 |
| AXIOM | 44 | 28 | 0.0% | 52.3% | 36.4% | 29.5% | Bug 24; Improvement 11; New Feature 3; Task 3; Question 2; Dependency upgrade 1 | Open 20; Resolved 18; Closed 5; Reopened 1 |
| DROIDS | 44 | 1 | 0.0% | 0.0% | 20.5% | 50.0% | Improvement 22; New Feature 8; Bug 7; Question 3; Wish 2; Task 1; Sub-task 1 | Open 42; Reopened 1; In Progress 1 |
| CELIX | 44 | 0 | 0.0% | 0.0% | 43.2% | 50.0% | Improvement 23; Bug 17; New Feature 3; Wish 1 | Open 44 |
| XMLCOMMONS | 43 | 7 | 0.0% | 41.9% | 2.3% | 0.0% | Bug 31; Improvement 5; New Feature 4; Task 2; Wish 1 | Open 24; Closed 16; Resolved 2; Reopened 1 |
| LOGGING | 42 | 30 | 0.0% | 61.9% | 9.5% | 64.3% | Bug 18; Improvement 15; Sub-task 5; New Feature 3; Task 1 | Open 16; Resolved 14; Closed 12 |
| RAMPARTC | 41 | 0 | 0.0% | 0.0% | 97.6% | 31.7% | Bug 26; New Feature 11; Improvement 3; Wish 1 | Open 41 |
| MVERIFIER | 40 | 10 | 0.0% | 87.5% | 67.5% | 65.0% | Improvement 13; Dependency upgrade 9; Bug 8; New Feature 5; Task 4; Wish 1 | Closed 35; Open 5 |
| MLINKCHECK | 40 | 5 | 0.0% | 72.5% | 65.0% | 65.0% | Bug 14; Improvement 13; Dependency upgrade 8; New Feature 3; Task 2 | Closed 29; Open 11 |
| CRAIL | 40 | 5 | 0.0% | 2.5% | 27.5% | 7.5% | Bug 18; Improvement 18; New Feature 2; Wish 2 | Open 37; Reopened 2; Closed 1 |
| APISIX | 40 | 40 | 0.0% | 25.0% | 0.0% | 0.0% | Task 13; New Feature 11; Wish 6; Improvement 4; Bug 4; Test 2 | Open 30; Closed 7; Resolved 3 |
| WSRP4J | 39 | 0 | 0.0% | 0.0% | 5.1% | 33.3% | Bug 24; Improvement 13; Wish 1; New Feature 1 | Open 39 |
| EMAIL | 39 | 20 | 2.6% | 43.6% | 23.1% | 38.5% | Bug 17; Improvement 14; New Feature 4; Task 3; Wish 1 | Open 21; Closed 9; Resolved 8; Reopened 1 |
| VELTOOLS | 39 | 35 | 0.0% | 97.4% | 92.3% | 89.7% | Bug 21; Task 12; Improvement 5; New Feature 1 | Resolved 23; Closed 15; Open 1 |
| GUMP | 38 | 1 | 0.0% | 2.6% | 5.3% | 36.8% | New Feature 13; Improvement 10; Bug 9; Task 5; Wish 1 | Open 37; Resolved 1 |
| CHAIN | 37 | 1 | 0.0% | 0.0% | 2.7% | 45.9% | Improvement 16; Bug 8; New Feature 4; Task 4; Sub-task 4; Wish 1 | Open 37 |
| OJB | 36 | 0 | 0.0% | 0.0% | 30.6% | 8.3% | Bug 17; New Feature 12; Improvement 4; Wish 2; Test 1 | Open 35; In Progress 1 |
| SMX4NMR | 36 | 0 | 0.0% | 0.0% | 13.9% | 30.6% | Improvement 20; Bug 8; New Feature 7; Task 1 | Open 35; Reopened 1 |
| SMX4KNL | 36 | 0 | 0.0% | 0.0% | 27.8% | 44.4% | Bug 12; Improvement 10; New Feature 5; Sub-task 5; Task 4 | Open 32; In Progress 4 |
| IMAP | 36 | 0 | 0.0% | 47.2% | 47.2% | 16.7% | Bug 16; Improvement 9; New Feature 8; Task 2; Wish 1 | Open 18; Closed 13; Resolved 4; Reopened 1 |
| HUPA | 36 | 0 | 0.0% | 0.0% | 83.3% | 5.6% | New Feature 11; Improvement 10; Bug 9; Task 4; Dependency upgrade 1; Story 1 | Open 36 |
| TAMAYA | 36 | 2 | 2.8% | 2.8% | 58.3% | 5.6% | Task 13; Sub-task 9; Improvement 6; Bug 5; New Feature 3 | Open 24; In Progress 10; Reopened 1; Resolved 1 |
| MAILET | 35 | 6 | 0.0% | 28.6% | 17.1% | 25.7% | Improvement 13; Bug 10; Task 7; New Feature 5 | Open 24; Closed 10; In Progress 1 |
| MRUNIT | 35 | 0 | 0.0% | 0.0% | 34.3% | 8.6% | Bug 17; Improvement 6; Task 5; Sub-task 3; Question 2; Umbrella 1; New Feature 1 | Open 30; In Progress 4; Reopened 1 |
| AMATERASU | 35 | 0 | 0.0% | 0.0% | 40.0% | 42.9% | Improvement 12; Sub-task 8; New Feature 7; Bug 5; Task 3 | Open 34; In Progress 1 |
| DIGESTER | 34 | 8 | 0.0% | 14.7% | 11.8% | 23.5% | Bug 17; Improvement 13; Task 2; New Feature 1; Wish 1 | Open 28; Resolved 3; Closed 2; Reopened 1 |
| TILES | 33 | 0 | 0.0% | 0.0% | 9.1% | 6.1% | Bug 20; Improvement 7; New Feature 3; Task 2; Dependency 1 | Open 28; Reopened 3; In Progress 2 |
| MPDF | 33 | 20 | 0.0% | 100.0% | 63.6% | 63.6% | Dependency upgrade 12; New Feature 7; Task 7; Improvement 4; Bug 3 | Closed 30; Resolved 3 |
| KALUMET | 33 | 0 | 0.0% | 0.0% | 36.4% | 78.8% | New Feature 14; Improvement 11; Bug 4; Task 3; Wish 1 | Open 33 |
| COR | 33 | 0 | 0.0% | 0.0% | 45.5% | 42.4% | Improvement 16; Bug 6; New Feature 5; Task 4; Test 1; Wish 1 | Open 33 |
| MJMOD | 33 | 8 | 0.0% | 78.8% | 75.8% | 90.9% | Dependency upgrade 13; Improvement 9; Bug 6; Task 3; New Feature 2 | Closed 21; Open 7; Resolved 5 |
| ADDR | 32 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Bug 15; Improvement 10; New Feature 3; Task 2; Test 1; Wish 1 | Open 32 |
| PYLUCENE | 32 | 19 | 0.0% | 56.2% | 6.2% | 0.0% | Bug 19; Improvement 8; Task 2; Wish 1; Blog - New Blog Request 1; Question 1 | Open 14; Resolved 10; Closed 8 |
| MJDEPS | 32 | 9 | 0.0% | 68.8% | 65.6% | 56.2% | Improvement 10; Bug 8; New Feature 6; Dependency upgrade 6; Test 1; Task 1 | Closed 21; Open 10; Resolved 1 |
| CASSPYTHON | 32 | 32 | 0.0% | 50.0% | 56.2% | 71.9% | Improvement 14; Bug 11; Task 4; New Feature 3 | Resolved 16; Triage Needed 10; Open 4; In Progress 2 |
| DBUTILS | 31 | 10 | 0.0% | 41.9% | 38.7% | 41.9% | Bug 15; Improvement 13; New Feature 2; Wish 1 | Open 17; Resolved 12; Closed 1; In Progress 1 |
| DORMANT | 30 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Bug 15; Improvement 14; Task 1 | Open 30 |
| GERONIMO | 30 | 0 | 0.0% | 100.0% | 20.0% | 96.7% | New Feature 8; Improvement 8; Bug 7; Task 5; Wish 1; Sub-task 1 | Closed 30 |
| JAXME | 30 | 0 | 0.0% | 6.7% | 20.0% | 10.0% | Bug 23; Improvement 4; New Feature 2; Sub-task 1 | Open 28; Resolved 2 |
| GRFT | 30 | 0 | 0.0% | 0.0% | 20.0% | 53.3% | Improvement 12; Bug 8; Task 6; New Feature 4 | Open 27; In Progress 3 |
| AGILA | 30 | 0 | 0.0% | 0.0% | 56.7% | 23.3% | New Feature 17; Improvement 12; Bug 1 | Open 29; Reopened 1 |
| MYNEWTDOC | 30 | 0 | 16.7% | 0.0% | 36.7% | 0.0% | Task 26; Improvement 3; Sub-task 1 | Open 29; In Progress 1 |
| MSTAGE | 29 | 8 | 0.0% | 100.0% | 55.2% | 48.3% | Bug 14; Improvement 7; Task 4; Dependency upgrade 4 | Closed 29 |
| OLIO | 29 | 0 | 13.8% | 0.0% | 100.0% | 20.7% | Bug 14; Improvement 10; New Feature 2; Sub-task 1; New JIRA Project 1; Suitable Name Search 1 | Open 25; Reopened 2; In Progress 2 |
| PHOTARK | 29 | 0 | 0.0% | 0.0% | 10.3% | 58.6% | Improvement 10; Bug 9; New Feature 9; Question 1 | Open 29 |
| BVAL | 29 | 23 | 0.0% | 93.1% | 41.4% | 65.5% | Bug 15; Improvement 9; New Feature 4; Task 1 | Resolved 17; Closed 10; Open 2 |
| CLOWNFISH | 29 | 1 | 0.0% | 0.0% | 17.2% | 3.4% | Bug 12; Improvement 11; New Feature 5; Test 1 | Open 29 |
| SOAP | 28 | 0 | 0.0% | 0.0% | 71.4% | 0.0% | Bug 26; Improvement 2 | Open 28 |
| WHISKER | 28 | 17 | 0.0% | 64.3% | 53.6% | 67.9% | Bug 10; Improvement 9; Task 8; Sub-task 1 | Closed 16; Open 9; Resolved 2; In Progress 1 |
| APOLLO | 27 | 0 | 0.0% | 0.0% | 11.1% | 0.0% | Bug 8; Task 7; Improvement 6; New Feature 6 | Open 27 |
| OLTU | 27 | 0 | 0.0% | 0.0% | 44.4% | 3.7% | Bug 16; Improvement 7; Sub-task 2; New Feature 1; Dependency upgrade 1 | Open 23; In Progress 3; Reopened 1 |
| GOSSIP | 27 | 0 | 0.0% | 0.0% | 55.6% | 14.8% | New Feature 13; Bug 6; Sub-task 5; Improvement 3 | Open 27 |
| IMPERIUS | 26 | 0 | 0.0% | 0.0% | 100.0% | 0.0% | Bug 24; New Feature 1; Improvement 1 | Open 25; Reopened 1 |
| SAMOA | 26 | 3 | 0.0% | 0.0% | 7.7% | 0.0% | Bug 13; New Feature 8; Task 5 | To Do 26 |
| NUTTX | 26 | 25 | 0.0% | 19.2% | 0.0% | 0.0% | New Feature 15; Improvement 5; Task 3; Bug 3 | Open 21; Closed 5 |
| COCOON3 | 25 | 0 | 0.0% | 0.0% | 8.0% | 96.0% | Improvement 12; Bug 8; Task 3; New Feature 2 | Open 24; Reopened 1 |
| HISE | 25 | 0 | 0.0% | 0.0% | 28.0% | 64.0% | New Feature 9; Bug 6; Improvement 6; Wish 2; Task 2 | Open 23; In Progress 1; Reopened 1 |
| WSCOMMONS | 24 | 0 | 0.0% | 0.0% | 0.0% | 4.2% | Bug 18; Improvement 4; New Feature 1; Wish 1 | Open 23; Reopened 1 |
| JSPF | 24 | 10 | 0.0% | 29.2% | 20.8% | 62.5% | Bug 9; Improvement 6; Task 5; New Feature 3; Request 1 | Open 17; Closed 4; Resolved 3 |
| KITTY | 24 | 1 | 0.0% | 100.0% | 33.3% | 0.0% | Bug 7; Improvement 6; Sub-task 4; New Feature 2; Task 2; Wish 1; Brainstorming 1; Test 1 | Closed 24 |
| ASFSITE | 24 | 16 | 0.0% | 100.0% | 70.8% | 0.0% | Bug 19; Improvement 3; Test 1; Task 1 | Closed 17; Resolved 7 |
| CASSCPP | 24 | 24 | 0.0% | 29.2% | 25.0% | 58.3% | Improvement 15; Task 5; Bug 4 | Triage Needed 16; Resolved 7; Open 1 |
| BETWIXT | 23 | 0 | 0.0% | 4.3% | 4.3% | 0.0% | Bug 17; Improvement 4; Test 1; Task 1 | Open 22; Resolved 1 |
| JCRSITE | 23 | 6 | 0.0% | 30.4% | 13.0% | 4.3% | Improvement 9; Bug 7; Task 6; New Feature 1 | Open 16; Resolved 6; Closed 1 |
| XMLSCHEMA | 23 | 12 | 0.0% | 60.9% | 47.8% | 47.8% | Bug 10; Question 4; Improvement 3; Task 3; New Feature 2; IT Help 1 | Open 9; Resolved 9; Closed 5 |
| OPENWIRE | 23 | 16 | 0.0% | 52.2% | 60.9% | 65.2% | Task 10; Bug 7; Improvement 4; New Feature 2 | Open 10; Resolved 9; Closed 3; In Progress 1 |
| CORAL | 23 | 21 | 8.7% | 0.0% | 8.7% | 0.0% | Bug 19; Test 1; Task 1; Improvement 1; Wish 1 | Open 23 |
| CXFXJC | 22 | 17 | 0.0% | 68.2% | 31.8% | 68.2% | Bug 10; Improvement 8; Task 3; New Feature 1 | Resolved 12; Open 7; Closed 3 |
| TRAINING | 22 | 13 | 0.0% | 50.0% | 50.0% | 0.0% | Improvement 8; Bug 6; Task 4; New Feature 3; Wish 1 | Closed 11; Open 7; Triage Needed 4 |
| PULSAR | 22 | 21 | 0.0% | 18.2% | 0.0% | 0.0% | Bug 10; Improvement 6; New Feature 5; Task 1 | Open 17; Resolved 3; Reopened 1; Closed 1 |
| COMMONSXML | 22 | 22 | 0.0% | 68.2% | 0.0% | 63.6% | Improvement 11; Bug 7; New Feature 2; Wish 1; Task 1 | Resolved 12; Open 6; Closed 3; Reopened 1 |
| TRANSACTION | 21 | 0 | 0.0% | 0.0% | 4.8% | 42.9% | Bug 12; Improvement 5; New Feature 3; Task 1 | Open 19; Reopened 1; In Progress 1 |
| IOTA | 21 | 1 | 9.5% | 100.0% | 85.7% | 33.3% | Task 7; Improvement 7; New Feature 3; Bug 3; Test 1 | Closed 21 |
| GBUILD | 20 | 6 | 0.0% | 0.0% | 20.0% | 20.0% | New Feature 13; Improvement 3; Bug 2; Task 2 | Open 19; Patch Available 1 |
| TENTACLES | 20 | 14 | 0.0% | 65.0% | 95.0% | 55.0% | Task 7; Improvement 6; Bug 5; New Feature 2 | Closed 11; Open 4; Resolved 2; In Progress 2; Reopened 1 |
| COMMONSRDF | 20 | 1 | 0.0% | 5.0% | 35.0% | 20.0% | New Feature 5; Improvement 4; Wish 3; Task 3; Bug 3; Test 2 | Open 15; In Progress 3; Reopened 1; Closed 1 |
| OPENAZ | 20 | 0 | 0.0% | 100.0% | 15.0% | 0.0% | Task 18; New Feature 2 | Done 20 |
| EASYANT | 19 | 0 | 0.0% | 0.0% | 5.3% | 0.0% | New Feature 9; Task 4; Bug 3; Improvement 2; Wish 1 | Open 19 |
| XERCESP | 18 | 2 | 0.0% | 0.0% | 44.4% | 0.0% | Bug 16; Improvement 1; New Feature 1 | Open 18 |
| HTTPASYNC | 18 | 10 | 0.0% | 100.0% | 5.6% | 16.7% | Bug 17; Improvement 1 | Resolved 15; Closed 3 |
| PIRK | 18 | 0 | 0.0% | 0.0% | 77.8% | 27.8% | Improvement 11; Bug 5; Sub-task 1; Task 1 | Open 13; In Progress 4; Reopened 1 |
| TORQUE | 18 | 16 | 0.0% | 77.8% | 44.4% | 88.9% | Bug 9; Improvement 7; Task 2 | Resolved 10; Open 4; Closed 4 |
| PB | 17 | 2 | 0.0% | 5.9% | 11.8% | 5.9% | Bug 12; Improvement 3; New Feature 1; Task 1 | Open 14; In Progress 2; Closed 1 |
| XMLRPC | 17 | 0 | 0.0% | 0.0% | 5.9% | 5.9% | Bug 11; Improvement 4; New Feature 1; Task 1 | Open 16; Reopened 1 |
| ASYNCWEB | 17 | 0 | 0.0% | 0.0% | 17.6% | 0.0% | Bug 13; Task 3; Improvement 1 | Open 16; Reopened 1 |
| BUILDR | 17 | 0 | 0.0% | 11.8% | 41.2% | 82.4% | Bug 10; New Feature 3; Improvement 3; Task 1 | Open 13; Closed 2; Reopened 2 |
| ORCHESTRA | 17 | 0 | 0.0% | 0.0% | 29.4% | 5.9% | Bug 8; New Feature 3; Improvement 3; Wish 2; Task 1 | Open 14; Patch Available 2; Reopened 1 |
| TASHI | 17 | 0 | 0.0% | 100.0% | 76.5% | 0.0% | Bug 7; Improvement 5; New Feature 4; Wish 1 | Closed 17 |
| JSIEVE | 17 | 4 | 0.0% | 11.8% | 35.3% | 47.1% | Task 5; New Feature 4; Bug 4; Improvement 3; Sub-task 1 | Open 13; In Progress 2; Resolved 1; Closed 1 |
| HDT | 17 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Improvement 6; Bug 5; New Feature 3; Task 2; Documentation 1 | Open 17 |
| PROVISIONR | 17 | 0 | 0.0% | 0.0% | 41.2% | 41.2% | Improvement 6; New Feature 4; Bug 2; Task 2; Dependency upgrade 2; Umbrella 1 | Open 17 |
| MSCRIPTING | 17 | 14 | 0.0% | 94.1% | 94.1% | 64.7% | Dependency upgrade 6; Improvement 4; Bug 3; Task 3; New Feature 1 | Closed 8; Resolved 8; Open 1 |
| DIR | 16 | 6 | 0.0% | 25.0% | 87.5% | 0.0% | Bug 7; Improvement 5; New Feature 2; Task 1; Wish 1 | Open 12; Resolved 2; Closed 2 |
| STONEHENGE | 16 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Bug 7; Wish 4; Task 2; Improvement 2; New Feature 1 | Open 16 |
| SCXML | 16 | 4 | 0.0% | 6.2% | 6.2% | 18.8% | Improvement 6; Bug 5; New Feature 4; Sub-task 1 | Open 15; Closed 1 |
| LUCY | 16 | 0 | 0.0% | 0.0% | 25.0% | 18.8% | Improvement 7; Bug 5; Sub-task 1; Task 1; Brainstorming 1; Documentation 1 | Open 16 |
| CASSNODEJS | 16 | 16 | 0.0% | 43.8% | 68.8% | 43.8% | Improvement 9; Task 3; Bug 3; Epic 1 | Triage Needed 8; Resolved 7; Open 1 |
| SAND | 15 | 0 | 0.0% | 0.0% | 26.7% | 0.0% | Bug 11; Improvement 3; New Feature 1 | Open 15 |
| JCRRMI | 15 | 0 | 0.0% | 0.0% | 6.7% | 13.3% | New Feature 5; Improvement 4; Bug 4; Sub-task 2 | Open 12; Patch Available 2; Reopened 1 |
| JCI | 15 | 2 | 0.0% | 0.0% | 53.3% | 53.3% | Improvement 6; Bug 5; New Feature 2; Wish 1; Test 1 | Open 13; Reopened 2 |
| BSF | 15 | 3 | 0.0% | 6.7% | 6.7% | 0.0% | Improvement 6; Bug 5; New Feature 2; Task 2 | Open 14; Resolved 1 |
| MFHTML5 | 15 | 2 | 0.0% | 6.7% | 46.7% | 60.0% | New Feature 6; Task 3; Improvement 3; Bug 3 | Open 11; In Progress 2; Patch Available 1; Closed 1 |
| ECHARTS | 15 | 7 | 0.0% | 20.0% | 0.0% | 0.0% | Bug 6; Improvement 5; Task 4 | Open 12; Closed 2; Resolved 1 |
| EL | 14 | 0 | 0.0% | 0.0% | 0.0% | 28.6% | Bug 12; Improvement 2 | Open 13; Reopened 1 |
| MECLIPSE | 14 | 0 | 0.0% | 100.0% | 42.9% | 14.3% | Bug 9; Improvement 4; New Feature 1 | Closed 14 |
| JCRTCK | 14 | 0 | 0.0% | 0.0% | 21.4% | 0.0% | Bug 13; Test 1 | Open 10; In Progress 2; Patch Available 1; Reopened 1 |
| OEP | 14 | 0 | 0.0% | 0.0% | 42.9% | 0.0% | New Feature 6; Improvement 4; Bug 4 | Open 14 |
| KATO | 14 | 0 | 0.0% | 0.0% | 7.1% | 7.1% | New Feature 8; Task 3; Improvement 2; Bug 1 | Open 14 |
| COTTON | 14 | 0 | 0.0% | 0.0% | 14.3% | 0.0% | Task 7; Bug 6; Epic 1 | Open 12; Reviewable 2 |
| CONCERTED | 14 | 0 | 0.0% | 0.0% | 71.4% | 0.0% | Bug 5; Task 3; New Feature 3; Improvement 3 | Open 12; In Progress 2 |
| PINOT | 14 | 8 | 0.0% | 7.1% | 14.3% | 0.0% | Bug 11; Improvement 1; New Feature 1; Task 1 | Open 12; Reopened 1; Closed 1 |
| TUWENI | 14 | 2 | 0.0% | 35.7% | 35.7% | 78.6% | Improvement 6; Bug 5; Task 2; New Feature 1 | Open 9; Resolved 5 |
| TRB | 13 | 3 | 0.0% | 7.7% | 30.8% | 7.7% | Bug 6; Improvement 3; New Feature 2; Task 2 | Open 12; Resolved 1 |
| SANDESHA2C | 13 | 0 | 0.0% | 0.0% | 23.1% | 0.0% | Bug 7; Improvement 3; Task 2; Test 1 | Open 12; Reopened 1 |
| EXTVAL | 13 | 0 | 0.0% | 0.0% | 30.8% | 0.0% | Task 5; Bug 4; New Feature 2; Improvement 2 | Open 12; Patch Available 1 |
| NUVEM | 13 | 0 | 0.0% | 0.0% | 7.7% | 23.1% | New Feature 6; Improvement 5; Test 1; Bug 1 | Open 13 |
| ONAMI | 13 | 0 | 0.0% | 23.1% | 46.2% | 30.8% | Improvement 5; New Feature 2; Task 2; Bug 2; Test 1; Question 1 | Open 10; Closed 3 |
| BRAND | 13 | 0 | 0.0% | 100.0% | 69.2% | 0.0% | Bug 9; Task 4 | Closed 11; Resolved 2 |
| MJDEPRSCAN | 13 | 12 | 0.0% | 92.3% | 84.6% | 92.3% | Dependency upgrade 7; Improvement 3; Task 2; Bug 1 | Closed 12; Open 1 |
| CS | 13 | 11 | 7.7% | 53.8% | 38.5% | 0.0% | Task 6; New Feature 3; Bug 3; Improvement 1 | Resolved 7; Open 6 |
| TEXEN | 12 | 0 | 0.0% | 0.0% | 0.0% | 25.0% | Bug 7; Improvement 3; Sub-task 1; New Feature 1 | Open 12 |
| DBF | 12 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Improvement 4; Bug 4; New Feature 3; Task 1 | Open 12 |
| PRC | 12 | 0 | 0.0% | 0.0% | 0.0% | 8.3% | Bug 7; Question 2; Task 2; Sub-task 1 | Open 11; Reopened 1 |
| ALOIS | 12 | 0 | 0.0% | 0.0% | 50.0% | 0.0% | Task 7; Improvement 3; Test 1; Wish 1 | Open 12 |
| TESTING | 12 | 6 | 16.7% | 0.0% | 8.3% | 0.0% | Bug 7; Task 2; Improvement 1; Wish 1; Test 1 | Open 12 |
| CLKE | 11 | 0 | 9.1% | 0.0% | 100.0% | 0.0% | Improvement 6; New Feature 4; Bug 1 | Open 9; In Progress 2 |
| DOSGI | 11 | 2 | 0.0% | 0.0% | 0.0% | 36.4% | Bug 9; Improvement 1; New Feature 1 | Open 11 |
| JDKIM | 11 | 6 | 0.0% | 54.5% | 18.2% | 18.2% | Improvement 3; Bug 3; New Feature 3; Question 1; Wish 1 | Open 5; Closed 4; Resolved 2 |
| SUPERSET | 11 | 6 | 0.0% | 36.4% | 0.0% | 0.0% | Bug 6; Task 4; Improvement 1 | Open 7; Closed 3; Resolved 1 |
| PEGASUS | 11 | 11 | 0.0% | 18.2% | 0.0% | 0.0% | Sub-task 9; Task 1; Bug 1 | Open 9; Resolved 1; Closed 1 |
| PRIMITIVES | 10 | 0 | 0.0% | 0.0% | 0.0% | 10.0% | Improvement 6; Bug 3; New Feature 1 | Open 10 |
| WADI | 10 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Task 7; Test 2; Bug 1 | Open 10 |
| DIRTSEC | 10 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Bug 8; New Feature 1; Task 1 | Open 10 |
| SAVAN | 10 | 0 | 0.0% | 0.0% | 10.0% | 0.0% | Bug 7; Improvement 2; Question 1 | Open 10 |
| PROTOCOLS | 10 | 1 | 0.0% | 50.0% | 90.0% | 30.0% | Bug 4; New Feature 3; Improvement 2; Task 1 | Open 5; Closed 4; Resolved 1 |
| CMDA | 10 | 0 | 10.0% | 0.0% | 60.0% | 0.0% | Improvement 2; Task 2; New Feature 2; Bug 2; Test 1; Sub-task 1 | Open 10 |
| DATASKETCHES | 10 | 10 | 0.0% | 90.0% | 70.0% | 0.0% | Bug 3; Improvement 3; Task 2; Wish 1; New Feature 1 | Closed 9; Open 1 |
| LAUNCHER | 9 | 0 | 0.0% | 0.0% | 0.0% | 11.1% | Bug 5; Improvement 4 | Open 9 |
| LCN4C | 9 | 2 | 0.0% | 22.2% | 11.1% | 0.0% | Bug 5; New Feature 2; Task 2 | Open 7; Closed 2 |
| SITE | 9 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Improvement 4; Task 3; New Feature 2 | Open 8; Reopened 1 |
| MFCOMMONS | 9 | 0 | 0.0% | 0.0% | 44.4% | 11.1% | Bug 4; Improvement 3; New Feature 1; Task 1 | Open 7; Patch Available 1; Reopened 1 |
| BLAZE | 9 | 0 | 0.0% | 100.0% | 77.8% | 55.6% | New Feature 9 | Closed 9 |
| APA | 9 | 5 | 0.0% | 11.1% | 100.0% | 0.0% | Task 4; Bug 2; New Feature 1; Improvement 1; IT Help 1 | Open 8; Closed 1 |
| BLUEMARLIN | 9 | 9 | 0.0% | 55.6% | 11.1% | 0.0% | Task 3; Bug 2; Improvement 2; New Feature 1; Test 1 | Closed 5; Open 4 |
| EVENTMESH | 9 | 9 | 0.0% | 44.4% | 0.0% | 0.0% | Bug 5; Task 2; Wish 2 | Open 5; Closed 4 |
| MIRAE | 8 | 0 | 12.5% | 0.0% | 12.5% | 0.0% | Bug 4; Task 2; Test 1; New Feature 1 | Open 8 |
| POSTAGE | 8 | 0 | 0.0% | 0.0% | 12.5% | 12.5% | Improvement 5; New Feature 2; Bug 1 | Open 8 |
| MODELER | 8 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Bug 7; Improvement 1 | Open 8 |
| ORP | 8 | 6 | 0.0% | 0.0% | 0.0% | 0.0% | Bug 3; New Feature 2; Blogs - Access to Existing Blog 1; Task 1; Blogs - New Blog User Account Request 1 | Open 8 |
| MPATCH | 8 | 5 | 0.0% | 62.5% | 50.0% | 62.5% | Bug 4; New Feature 1; Improvement 1; Dependency upgrade 1; Task 1 | Closed 5; Open 3 |
| DI | 8 | 3 | 0.0% | 12.5% | 37.5% | 0.0% | Task 4; Bug 2; New Feature 1; Wish 1 | Open 6; In Progress 1; Closed 1 |
| KAND | 7 | 0 | 0.0% | 0.0% | 14.3% | 0.0% | Bug 5; Improvement 2 | Open 7 |
| RESOURCES | 7 | 0 | 0.0% | 0.0% | 28.6% | 14.3% | Bug 4; Improvement 3 | Open 7 |
| PORTALS | 7 | 3 | 0.0% | 28.6% | 14.3% | 0.0% | Bug 4; Task 3 | Open 5; Closed 2 |
| LOKAHI | 7 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Improvement 4; Bug 3 | Open 6; Reopened 1 |
| MYFACESTEST | 7 | 0 | 0.0% | 0.0% | 14.3% | 0.0% | Improvement 5; New Feature 2 | Open 7 |
| EXTCDI | 7 | 0 | 0.0% | 0.0% | 85.7% | 14.3% | Bug 4; Improvement 2; Task 1 | Open 6; Reopened 1 |
| MAVIBOT | 7 | 0 | 0.0% | 0.0% | 100.0% | 100.0% | Improvement 4; Bug 2; New Feature 1 | Open 7 |
| AAR | 7 | 7 | 0.0% | 85.7% | 0.0% | 0.0% | Improvement 4; Bug 3 | Closed 6; Open 1 |
| ANAKIA | 6 | 0 | 0.0% | 0.0% | 0.0% | 33.3% | New Feature 3; Improvement 1; Task 1; Bug 1 | Open 6 |
| ARMI | 6 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Bug 4; New Feature 1; Improvement 1 | Open 6 |
| HERMES | 6 | 0 | 0.0% | 0.0% | 50.0% | 0.0% | Bug 3; New Feature 2; Improvement 1 | Open 4; In Progress 2 |
| DIRGROOVY | 6 | 0 | 0.0% | 0.0% | 100.0% | 0.0% | Task 3; Bug 3 | Open 5; In Progress 1 |
| MPT | 6 | 0 | 0.0% | 16.7% | 16.7% | 0.0% | New Feature 3; Bug 3 | Open 5; Closed 1 |
| MDOCCK | 6 | 6 | 0.0% | 100.0% | 66.7% | 66.7% | Improvement 2; Dependency upgrade 2; New Feature 1; Task 1 | Closed 6 |
| EWS | 5 | 0 | 0.0% | 0.0% | 80.0% | 60.0% | Improvement 4; Bug 1 | Open 5 |
| MANTTASKS | 5 | 0 | 0.0% | 100.0% | 80.0% | 60.0% | Bug 4; Improvement 1 | Closed 5 |
| TILESSHOW | 5 | 0 | 0.0% | 0.0% | 0.0% | 80.0% | Sub-task 3; Bug 2 | Open 5 |
| EXTSCRIPT | 5 | 0 | 0.0% | 0.0% | 80.0% | 40.0% | Improvement 2; Bug 1; Sub-task 1; Task 1 | Open 5 |
| TM | 5 | 2 | 0.0% | 100.0% | 100.0% | 0.0% | Task 3; Question 1; Bug 1 | Closed 3; Resolved 2 |
| AUTOTAG | 5 | 0 | 20.0% | 0.0% | 0.0% | 0.0% | Bug 2; Improvement 2; Task 1 | Open 4; Reopened 1 |
| TATPI | 5 | 0 | 0.0% | 0.0% | 100.0% | 0.0% | Test 5 | Unknown 4; Requires Porting 1 |
| JACOB | 5 | 2 | 0.0% | 0.0% | 60.0% | 60.0% | Improvement 3; New Feature 1; Bug 1 | Open 5 |
| FORTRESS | 4 | 0 | 0.0% | 0.0% | 50.0% | 75.0% | New Feature 2; Wish 1; Bug 1 | Open 4 |
| AVNSHARP | 4 | 0 | 0.0% | 0.0% | 50.0% | 50.0% | Task 2; New Feature 1; Bug 1 | Open 4 |
| SCOUT | 4 | 1 | 0.0% | 25.0% | 100.0% | 0.0% | Bug 3; Task 1 | Open 3; Closed 1 |
| DAYTRADER | 4 | 0 | 0.0% | 0.0% | 0.0% | 25.0% | New Feature 2; Bug 2 | Open 4 |
| JCRSERVLET | 4 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Bug 2; New Feature 1; Improvement 1 | Open 4 |
| BLUESKY | 4 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Improvement 4 | Open 4 |
| TRANSPORTS | 4 | 0 | 0.0% | 0.0% | 25.0% | 50.0% | New Feature 2; Bug 1; Improvement 1 | Open 3; In Progress 1 |
| COUCHDB | 4 | 0 | 0.0% | 100.0% | 25.0% | 0.0% | Bug 3; Test 1 | Closed 4 |
| AMQCLI | 4 | 3 | 0.0% | 75.0% | 75.0% | 100.0% | New Feature 2; Bug 2 | Resolved 3; Open 1 |
| NIFILIBS | 4 | 0 | 0.0% | 50.0% | 25.0% | 50.0% | Task 4 | Open 2; Resolved 1; Closed 1 |
| NEETHI | 4 | 4 | 0.0% | 100.0% | 100.0% | 25.0% | Task 2; Improvement 1; Question 1 | Resolved 3; Closed 1 |
| DORIS | 4 | 4 | 0.0% | 0.0% | 0.0% | 0.0% | Improvement 2; New Feature 1; Bug 1 | Open 4 |
| GLUTEN | 4 | 4 | 0.0% | 50.0% | 25.0% | 0.0% | Task 2; Improvement 1; Bug 1 | Open 2; Resolved 1; Closed 1 |
| EXLBR | 3 | 0 | 0.0% | 0.0% | 33.3% | 66.7% | Bug 1; Improvement 1; New Feature 1 | Open 3 |
| TILESSHARED | 3 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Improvement 1; New Feature 1; Bug 1 | Open 3 |
| ECS | 3 | 0 | 0.0% | 0.0% | 33.3% | 0.0% | Bug 3 | Open 2; Reopened 1 |
| FUNCTOR | 3 | 0 | 0.0% | 0.0% | 0.0% | 33.3% | Improvement 1; Wish 1; New Feature 1 | Open 3 |
| FEEDPARSER | 3 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Bug 1; Improvement 1; Task 1 | Open 3 |
| DISCOVERY | 3 | 0 | 0.0% | 0.0% | 100.0% | 33.3% | Improvement 3 | Open 2; Reopened 1 |
| TREQ | 3 | 0 | 0.0% | 0.0% | 33.3% | 0.0% | Improvement 3 | Open 2; In Progress 1 |
| MILAGRO | 3 | 2 | 0.0% | 66.7% | 33.3% | 33.3% | Improvement 2; Bug 1 | Resolved 2; Open 1 |
| AMQWEBSITE | 3 | 3 | 0.0% | 66.7% | 33.3% | 0.0% | Improvement 2; Bug 1 | Resolved 2; Open 1 |
| OTAVA | 3 | 3 | 0.0% | 33.3% | 33.3% | 0.0% | Task 3 | Open 2; Closed 1 |
| DEPOT | 2 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | New Feature 1; Bug 1 | Open 2 |
| DIRNAMING | 2 | 0 | 0.0% | 0.0% | 100.0% | 0.0% | Test 1; Improvement 1 | In Progress 1; Open 1 |
| HERALDRY | 2 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | New Feature 1; Improvement 1 | Open 2 |
| TRIPLES | 2 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Task 2 | Open 2 |
| ATTRIBUTES | 2 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Bug 2 | Open 2 |
| PROXY | 2 | 0 | 0.0% | 0.0% | 100.0% | 100.0% | New Feature 2 | Open 2 |
| JCRCL | 2 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Bug 1; Improvement 1 | Open 2 |
| TSIK | 1 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Improvement 1 | Open 1 |
| KI | 1 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Bug 1 | Open 1 |
| JCRBENCH | 1 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Improvement 1 | Open 1 |
| SB | 1 | 0 | 0.0% | 0.0% | 100.0% | 0.0% | Improvement 1 | Open 1 |
| RBATIS | 1 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Bug 1 | Open 1 |
| TEVAL | 1 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | Bug 1 | Open 1 |
| ESCIMO | 1 | 0 | 0.0% | 0.0% | 100.0% | 0.0% | Improvement 1 | Open 1 |
| DVSL | 1 | 0 | 0.0% | 0.0% | 100.0% | 0.0% | Bug 1 | Open 1 |
| MANT | 1 | 0 | 0.0% | 100.0% | 100.0% | 0.0% | Wish 1 | Closed 1 |
| MYNEWT | 1 | 0 | 0.0% | 100.0% | 100.0% | 0.0% | Improvement 1 | Closed 1 |
| ZIPKIN | 1 | 0 | 0.0% | 0.0% | 0.0% | 0.0% | New Feature 1 | Open 1 |
| MREPOSITORY | 1 | 0 | 0.0% | 100.0% | 100.0% | 0.0% | Task 1 | Closed 1 |
| OWC | 1 | 1 | 0.0% | 0.0% | 0.0% | 0.0% | Bug 1 | Open 1 |
| STOMP | 1 | 1 | 0.0% | 100.0% | 100.0% | 0.0% | Test 1 | Closed 1 |
| INFRATESTY33 | 1 | 1 | 0.0% | 0.0% | 0.0% | 0.0% | Wish 1 | Open 1 |
| CLOUDBERRY | 1 | 1 | 0.0% | 100.0% | 0.0% | 0.0% | Test 1 | Resolved 1 |
| GAVTESTY | 1 | 1 | 0.0% | 0.0% | 0.0% | 0.0% | Task 1 | Open 1 |
| MMETRIC | 1 | 1 | 0.0% | 0.0% | 0.0% | 0.0% | New Feature 1 | To Do 1 |
| MCFSDK | 1 | 1 | 0.0% | 0.0% | 0.0% | 0.0% | Task 1 | Open 1 |
| WEAVER | 1 | 1 | 0.0% | 0.0% | 0.0% | 0.0% | Wish 1 | Open 1 |
