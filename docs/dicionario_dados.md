# Dicionário de dados

O dicionário descreve apenas os campos usados nas bases analíticas e no notebook.

**Convenções:**
- **Datas:** em UTC (ISO 8601); `release_date` é uma data sem hora.
- **Valor vazio:** "sem dado/evento", nunca zero.
- **Pessoas:** não aparecem nas bases. Só há indicadores booleanos (ex.: responsável presente na abertura).

## Campos de origem (Jira) usados

| Campo Jira | Uso |
|---|---|
| `id`, `key`, `fields.project.key` | identificação da issue e do projeto (chave técnica = `id`) |
| `fields.issuetype.name` | tipo de demanda (Bug, Improvement, …) |
| `fields.created`, `fields.resolutiondate` | abertura; data da resolução vigente (conciliada com o histórico) |
| `fields.status.name` + `statusCategory.key` | estado atual e categoria (`new`, `indeterminate`, `done`) |
| `fields.resolution.name` | tipo de resolução (Fixed, Duplicate, Won't Fix…) |
| `fields.priority.name` | prioridade (estado atual; a da abertura é reconstruída) |
| `fields.assignee` | só a presença (pseudonimizada no cache) |
| `fields.versions[].id` | **Affects Version** (vínculo bug → versão) |
| `fields.fixVersions[].id` | Fix Version (composição da release; nunca usada como desfecho) |
| `fields.components` | nº de componentes |
| `changelog.histories[].items[]` (`field`, `from`, `to`, `fromString`, `toString`, `created`) | reconstrução de status, resolution, priority, assignee, Version, Fix Version, Component, Project/Key |
| versão: `id`, `project_key`, `name`, `released`, `releaseDate` | releases |

## Base A — `projetos_caracterizacao.csv` (1 linha por projeto)

| Campo | Descrição |
|---|---|
| `projeto` | chave do projeto Apache |
| `issues_criadas>=2020`, `bugs>=2020`, `bugs_AAAA` | volumes por período |
| `releases>=2020`, `releases_por_ano`, `intervalo_mediano_dias` | cadência de releases |
| `nomes_modulares_%`, `prefixos_modulo_distintos`, `overlap_90d_%` | versionamento modular e sobreposição de janelas |
| `affects_version_%`, `affects_version_na_abertura_%` | cobertura do Affects Version entre os bugs |
| `abertos_%`, `fixed_%`, `dias_fixed_mediana`, `reabertos_%` | resolução e retrabalho |
| `prioridade_alterada_%`, `assignee_na_abertura_%`, `componente_%`, `severity_%`, `environment_%` | disponibilidade de preditores |
| `serie_interrompida(...)`, `ultimo_bug_criado` | série interrompida (≥ 100 bugs e nenhum bug nos últimos 12 meses) |

## Base B — `base_releases.csv` (1 linha por versão publicada com data)

| Campo | Descrição |
|---|---|
| `version_id` (chave), `project_key`, `name`, `release_date` | identificação; T0 = `release_date` |
| `bugs_proj`, `av_cov` | bugs do projeto desde 2020 e fração com Affects Version |
| `n_vinculados` | bugs distintos com Affects Version = versão (qualquer classe) |
| `bugs_pos_{30,90,180}d` | bugs da classe C criados em (T0, T0+w] |
| `bugs_pos_{w}d_conhecidos_na_janela` | idem, com o vínculo existente até T0+w |
| `classe_{w}d` | `com bugs vinculados`, `zero vinculado (cobertura adequada)`, `projeto com baixa cobertura AV (<50%)`, `dados insuficientes (<30 bugs no projeto)`, `acompanhamento incompleto` |

## Base C — `base_bug_release.csv` (1 linha por par bug × release do período) e `base_vinculos_evidencia.csv` (1 linha por vínculo atual)

| Campo | Descrição |
|---|---|
| `issue_id`, `version_id` (chave composta) | par bug × versão |
| `classe` | A antes / B mesmo dia / C depois / D data insuficiente (data UTC do bug × `release_date`) |
| `status_vinculo`, `t_conhecido` | regra simples do 05 (substituída pelos níveis do 06) |
| `n_av`, `fv_same` | nº de Affects Versions do bug; Affects Version = Fix Version na mesma versão |
| `pos_{w}`, `pos_{w}_conhecido` | classe C dentro da janela w; vínculo existente até o fim da janela |
| `nivel` | COMPROVADO / RECONSTRUIDO (= inferido com corroboração) / INFERIDO (sem corroboração) / INDETERMINADO |
| `in_initial`, `t_add`, `n_add`, `n_rem`, `chain_ok`, `tem_historico`, `motivo_indeterminado` | detalhes da reconstrução reversa |
| `ver_cat`, `bug_cat`, `bug_misto` | posição do vínculo em relação ao corte de 2020 |

## Base D — `base_bugs_ciclos.csv` (1 linha por bug criado ≥ 2020)

| Campo | Descrição |
|---|---|
| `issue_id` (chave), `key`, `project`, `created` | identificação; T0 = `created` |
| `status`, `status_cat`, `resolution` | estado atual (só para descrição, nunca como feature) |
| `t_b1`, `t_b2`, `t_b3` / `d_b1`, `d_b2`, `d_b3` | instantes / dias até B1 (1ª resolução), B2 (1º fechamento) e B3 (1ª correção Fixed) |
| `b1_status`, `b2_status`, `b3_status` | datado / censurado / encerrado sem Fixed |
| `recup_hist`, `rd_differs_b1` | sem `resolutiondate`, mas com fechamento datado; `resolutiondate` diferente da 1ª resolução |
| `h30_b3`, `h90_b3` | situação no horizonte fixo |
| `n_reab`, `n_ciclos`, `t_last_close`, `dur_adic_dias`, `dur_total_dias` | reaberturas, ciclos e durações |
| `est_{fechamento,fixed}_{30,90}` | estável / reaberta na janela / acompanhamento insuficiente |
| `resolved_to_closed` | o workflow usou Resolved → Closed |

## Base E — `base_reaberturas.csv` (1 linha por evento de reabertura) e `base_reaberturas_rapidas.csv`

| Campo | Descrição |
|---|---|
| `issue_id`, `project`, `t_reabertura`, `from_str`, `to_str` | evento: status terminal → não terminal |
| `t_fechamento_anterior`, `horas`, `faixa` | tempo desde a entrada em estado terminal imediatamente anterior |
| `classe` (rápidas) | o que ocorre após uma reabertura ≤ 5 min (re-encerrado ≤ 1 h com outra Resolution / com outros campos alterados / sem alteração; > 1 h; sem novo fechamento) |

## Base F — `resultados/tabelas/base_F_demandas_por_ano_classe.csv`

É um agregado por ano × classe proxy (correção = Bug; evolução = Improvement/New Feature/Wish/Story/Epic; outras/indefinidas). Inclui só combinações ano × tipo de issue com ≥ 50 issues (filtro do script 03). A composição por projeto vem das colunas `share_correcao_%` e `share_evolucao_%` da Base A.

## Bases de modelagem

| Base | Campos |
|---|---|
| `modelo_bugs_faixa.csv` | `issue_id`, `project`, `created`, `split`, `faixa_90d` (alvo), `prioridade_t0`, `responsavel_na_abertura`, `affects_version_na_criacao`, `componentes_na_criacao`, `bugs_projeto_30d_anteriores`, `backlog_aberto_projeto_t0` |
| `modelo_releases.csv` | `version_id`, `project_key`, `name`, `release_date`, `split`, `classe_180d`, `projeto_modular`, `tipo_versao`, `tamanho_t0`, `bugs_na_release_t0`, `evolucao_na_release_t0`, `dias_desde_release_anterior`, `releases_90d_anteriores`, `acompanhamento_180d_completo`, `bugs_180d_{conservador,ampliado,maximo}` (alvos) |
