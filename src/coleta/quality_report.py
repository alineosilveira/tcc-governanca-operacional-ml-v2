#!/usr/bin/env python3
"""Gera data_quality_report.md a partir da saída de apache_jira_extract.py (leitura em streaming)."""
from __future__ import annotations

import argparse
import collections
import json
import os


def iter_jsonl(path):
    if not os.path.exists(path):
        return
    with open(path, "rb") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def filled(v) -> bool:
    return v not in (None, "", [], {})


def pct(a, b) -> str:
    return f"{(100.0 * a / b):.1f}%" if b else "n/a"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.environ.get("ALINE_JIRA_DATA_DIR", os.path.join("data", "apache_jira")))
    args = ap.parse_args()
    P = lambda *a: os.path.join(args.out, *a)  # noqa: E731

    with open(P("fields.json"), encoding="utf-8") as f:
        catalog = json.load(f)
    fname = {x["id"]: x["name"] for x in catalog["fields"]}
    relevant = catalog["relevant_custom_fields"]
    manifest = {}
    if os.path.exists(P("manifest.json")):
        with open(P("manifest.json"), encoding="utf-8") as f:
            manifest = json.load(f)

    projects = list(iter_jsonl(P("projects.jsonl")))
    inv_keys = {p["key"] for p in projects}

    std = ["duedate", "resolution", "resolutiondate", "priority", "assignee", "fixVersions", "versions",
           "components", "labels", "environment", "timeoriginalestimate", "timespent", "issuelinks", "parent"]
    n = 0
    fill = collections.Counter()
    cf_fill = collections.Counter()
    by_proj = collections.defaultdict(lambda: {"n": 0, "types": collections.Counter(),
                                               "status": collections.Counter(), "due": 0, "res": 0,
                                               "asg": 0, "fixv": 0, "created_2020": 0})
    types = collections.Counter()
    statuses = collections.Counter()
    years = collections.Counter()
    cl_issues = cl_hist = com_issues = com_total = wl_issues = wl_total = 0
    cl_trunc = com_trunc = wl_trunc = 0
    reopened_status = 0
    for r in iter_jsonl(P("issues.jsonl")):
        n += 1
        fl = r.get("fields") or {}
        pk = (fl.get("project") or {}).get("key")
        bp = by_proj[pk]
        bp["n"] += 1
        it = (fl.get("issuetype") or {}).get("name")
        stn = (fl.get("status") or {}).get("name")
        bp["types"][it] += 1
        bp["status"][stn] += 1
        types[it] += 1
        statuses[stn] += 1
        if stn and stn.lower() == "reopened":
            reopened_status += 1
        years[(fl.get("created") or "")[:4]] += 1
        if (fl.get("created") or "") >= "2020":
            bp["created_2020"] += 1
        for k in std:
            if filled(fl.get(k)):
                fill[k] += 1
        bp["due"] += filled(fl.get("duedate"))
        bp["res"] += filled(fl.get("resolution"))
        bp["asg"] += filled(fl.get("assignee"))
        bp["fixv"] += filled(fl.get("fixVersions"))
        for k, v in fl.items():
            if k.startswith("customfield_") and filled(v):
                cf_fill[k] += 1
        cl = r.get("changelog") or {}
        if cl.get("total"):
            cl_issues += 1
            cl_hist += cl["total"]
            cl_trunc += cl.get("_obtained", 0) < cl["total"]
        c = fl.get("comment") or {}
        if c.get("total"):
            com_issues += 1
            com_total += c["total"]
            com_trunc += c.get("_obtained", 0) < c["total"]
        w = fl.get("worklog") or {}
        if w.get("total"):
            wl_issues += 1
            wl_total += w["total"]
            wl_trunc += w.get("_obtained", 0) < w["total"]

    # contagens efetivas dos arquivos associados
    def count_lines(name):
        p = P(name)
        if not os.path.exists(p):
            return None
        with open(p, "rb") as f:
            return sum(1 for _ in f)

    wl_secs = 0
    wl_authors = set()
    for w in iter_jsonl(P("worklogs.jsonl")):
        wl_secs += int(w.get("timeSpentSeconds") or 0)
        a = w.get("author") or {}
        wl_authors.add(a.get("key") or a.get("name"))
    cl_lines = count_lines("changelog.jsonl")
    com_lines = count_lines("comments.jsonl")
    v_lines = count_lines("versions.jsonl")
    sp_lines = count_lines("sprints.jsonl")
    isp_lines = count_lines("issue_sprints.jsonl")

    errs = collections.Counter()
    for e in iter_jsonl(P("errors.jsonl")):
        errs[(e.get("phase"), e.get("endpoint") if e.get("phase") in ("inspect", "boards") else
              e.get("endpoint", "").split("/issue/")[0], e.get("status"), e.get("retried"))] += 1

    L = []
    w = L.append
    w("# Relatório de qualidade de dados — Apache Jira (extração pública)\n")
    w(f"- Base: `{manifest.get('base_url')}` — servidor {((manifest.get('server_info') or {}).get('version'))} "
      f"({(manifest.get('server_info') or {}).get('deploymentType')})")
    w(f"- Extração iniciada (UTC): {manifest.get('extraction_started_utc')}; manifesto: {manifest.get('manifest_written_utc')}")
    w(f"- Estado de conclusão: **{manifest.get('completion')}**")
    w(f"- JQL global: `{manifest.get('global_jql')}`\n")

    w("## 1. Volume\n")
    w(f"| Item | Valor |\n|---|---|")
    w(f"| Projetos no inventário (`/project`) | {len(projects)} |")
    w(f"| Projetos arquivados retornados | {sum(1 for p in projects if p.get('archived'))} |")
    w(f"| Projetos com issues no recorte | {len(by_proj)} |")
    w(f"| Projetos presentes nos issues mas ausentes do inventário | {len(set(by_proj) - inv_keys)} {sorted(set(by_proj) - inv_keys)[:20]} |")
    w(f"| Issues únicas | {n} |")
    plan = manifest.get("plan") or {}
    w(f"| Total da JQL no planejamento / ao final | {plan.get('global_total')} / {manifest.get('global_total_at_end')} |")
    m = manifest.get("merge") or {}
    w(f"| Registros duplicados removidos (mesmo id) | {m.get('duplicate_issue_records_removed')} |")
    w(f"| Unidades (janelas) concluídas | {manifest.get('units_done')}/{manifest.get('units_total')}; falhas: {manifest.get('units_failed')} |")
    w(f"| Páginas de busca processadas | {manifest.get('pages_fetched')} |")
    w("")
    w("Issues por ano de criação: " + ", ".join(f"{y or '?'}: {c}" for y, c in sorted(years.items())) + "\n")

    w("## 2. Cobertura de preenchimento (campos padrão)\n")
    w("| Campo | Issues preenchidas | % |\n|---|---|---|")
    for k in std:
        w(f"| {k} | {fill[k]} | {pct(fill[k], n)} |")
    w("\n> `duedate` vazio **não** permite classificar a issue como em dia/atrasada; nenhuma inferência de prazo foi feita.\n")

    w("## 3. Campos customizados relevantes encontrados\n")
    w("Classificação por **nome** do campo (heurística); o significado real depende de cada projeto e deve ser validado.\n")
    for cat, items in relevant.items():
        if cat == "padrao_relevantes":
            continue
        w(f"### {cat}\n")
        if not items:
            w("_nenhum campo encontrado_\n")
            continue
        w("| id | nome | tipo | issues preenchidas | % |\n|---|---|---|---|---|")
        for it in items:
            c = cf_fill.get(it["id"], 0)
            w(f"| {it['id']} | {it['name']} | {it['type']} | {c} | {pct(c, n)} |")
        w("")
    w("### Todos os campos customizados com algum preenchimento (top 60)\n")
    w("| id | nome | issues | % |\n|---|---|---|---|")
    for k, c in cf_fill.most_common(60):
        w(f"| {k} | {fname.get(k, '?')} | {c} | {pct(c, n)} |")
    w(f"\nCampos customizados no catálogo: {catalog.get('custom_count')}; com ≥1 valor no recorte: {len(cf_fill)}.\n")

    w("## 4. Changelog, comentários e worklogs\n")
    w("| Conjunto | Issues com dados | Registros (total informado pela API) | Registros gravados | Issues truncadas na busca (completadas por endpoint dedicado) |")
    w("|---|---|---|---|---|")
    w(f"| Changelog (históricos) | {cl_issues} ({pct(cl_issues, n)}) | {cl_hist} | {cl_lines} | {cl_trunc} |")
    w(f"| Comentários | {com_issues} ({pct(com_issues, n)}) | {com_total} | {com_lines} | {com_trunc} |")
    w(f"| Worklogs | {wl_issues} ({pct(wl_issues, n)}) | {wl_total} | {m.get('worklogs')} | {wl_trunc} |")
    w(f"\nDados associados faltantes após retentativas: {m.get('associated_missing')}; incompletos: {m.get('associated_incomplete')}.")
    w(f"\nWorklogs: {wl_secs/3600:.1f} horas registradas por {len(wl_authors)} autores distintos. "
      f"Issues **sem worklog = sem dado disponível**, não zero horas trabalhadas; o registro de worklog é raro e "
      f"opcional na ASF (apenas {pct(wl_issues, n)} das issues).")
    w(f"\nIssues atualmente no status 'Reopened': {reopened_status}. Reaberturas históricas devem ser medidas pelas "
      f"transições de status em `changelog.jsonl` (o nome do status de reabertura varia por workflow).\n")

    w("## 5. Versões, sprints e boards\n")
    w(f"- `versions.jsonl`: {v_lines} versões de {(manifest.get('versions_projects') or {}).get('done')} projetos "
      f"(`/project/{{key}}/version`). Não-200: {(manifest.get('versions_projects') or {}).get('non_200')}")
    w(f"- `issue_versions.jsonl`: associação issue → fixVersions/versions (extraída dos campos do issue).")
    ba = manifest.get("boards_api") or {}
    w(f"- Agile API (`/rest/agile/1.0/board`): HTTP {ba.get('status')} — "
      f"{'disponível' if ba.get('available') else 'INDISPONÍVEL para acesso anônimo; boards/sprints não foram listados pela API'}.")
    w(f"- `sprints.jsonl`: {sp_lines} sprints **derivados** do valor bruto do campo `Sprint` nos issues; "
      f"`issue_sprints.jsonl`: {isp_lines} associações; `boards.jsonl`: ids de board (`rapidViewId`) derivados, sem nome. "
      f"Sprints sem nenhuma issue no recorte não aparecem.\n")

    w("## 6. Endpoints indisponíveis, erros e limites observados\n")
    pr = manifest.get("probes") or {}
    w(f"- `maxResults` solicitado 5000 → servidor devolveu `maxResults={((pr.get('maxResults_requested_5000') or {}).get('returned_maxResults'))}` (limite real por página).")
    w(f"- `expand=changelog` na busca retornou histórico completo (total = obtido) na grande maioria; truncamentos: {cl_trunc}.")
    w(f"- Campo `comment` na busca: até 1000 por issue; campo `worklog`: no máximo 20 por issue (complementado via `/issue/{{id}}/worklog`).")
    w(f"- `/rest/agile/1.0/board`: HTTP {pr.get('agile_board')}; `/worklog/updated`: HTTP {pr.get('worklog_updated')}; "
      f"`/issue/{{key}}/changelog`: HTTP {pr.get('issue_changelog_endpoint')} (não existe nesta versão do servidor).")
    w(f"- Projetos arquivados: `/project?includeArchived=true` não retornou nenhum projeto arquivado para acesso anônimo; "
      f"issues de projetos não listados aparecem acima se existirem.")
    w(f"- Campos restritos/privados (issues com security level, comentários restritos) não são visíveis anonimamente e não foram coletados.\n")
    w("| fase | endpoint | status | retentado | ocorrências |\n|---|---|---|---|---|")
    for (ph, ep, stt, rt), c in sorted(errs.items(), key=lambda x: -x[1])[:40]:
        w(f"| {ph} | {ep} | {stt} | {rt} | {c} |")
    w("")

    w("## 7. Cautelas de interpretação\n")
    w("- **Incidente de produção**: não há campo padrão; tipo `Bug`, devolução por QA ou existência de `fixVersion` "
      "**não** caracterizam incidente de produção. Campos como `Environment`, `Severity`, `Regression`, `Bug Category`, "
      "`Flags` existem em poucos projetos e com convenções próprias.")
    w("- **Causa raiz**: não há campo de causa raiz amplamente usado; comentários foram guardados como texto bruto e "
      "não foram classificados.")
    w("- **Criticidade**: `priority` é padrão, mas os esquemas de prioridade (Blocker/Critical/Major… ou P0–P4) variam por "
      "projeto; existem vários campos `Severity` distintos (ids diferentes) por projeto.")
    w("- **Sprint/estimativa**: o campo `Sprint` e `Story Points` são usados por poucos projetos; ausência ≠ zero.")
    w("- **Pessoas**: assignee não é o único recurso envolvido — considere reporter, autores de comentários, autores do "
      "changelog, autores de worklog e campos como Tester/Reviewer.")
    w("- **Prazos**: só issues com `duedate` permitem avaliar atraso; não houve inferência.")
    w("- Todos os significados acima dependem de convenções específicas de cada projeto e precisam ser validados antes de interpretar.\n")

    w("## 8. Tipos de issue e status por projeto\n")
    w(f"Tipos globais: " + ", ".join(f"{k}: {v}" for k, v in types.most_common()) + "\n")
    w(f"Status globais: " + ", ".join(f"{k}: {v}" for k, v in statuses.most_common()) + "\n")
    w("| projeto | issues | criadas ≥2020 | % duedate | % resolução | % assignee | % fixVersion | tipos | status |")
    w("|---|---|---|---|---|---|---|---|---|")
    for pk, b in sorted(by_proj.items(), key=lambda x: -x[1]["n"]):
        w(f"| {pk} | {b['n']} | {b['created_2020']} | {pct(b['due'], b['n'])} | {pct(b['res'], b['n'])} | "
          f"{pct(b['asg'], b['n'])} | {pct(b['fixv'], b['n'])} | "
          + "; ".join(f"{k} {v}" for k, v in b["types"].most_common()) + " | "
          + "; ".join(f"{k} {v}" for k, v in b["status"].most_common()) + " |")

    tmp = P("data_quality_report.md.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    os.replace(tmp, P("data_quality_report.md"))
    print(f"ok: {P('data_quality_report.md')} ({n} issues)")


if __name__ == "__main__":
    main()
