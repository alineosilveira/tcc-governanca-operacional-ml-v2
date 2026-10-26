#!/usr/bin/env python3
"""
Diagnóstico de cobertura e viabilidade temporal (5 objetivos) a partir das tabelas
compactas geradas por 01_projetar_base.py e dos arquivos pequenos da base
(versions.jsonl, sprints.jsonl, issue_sprints.jsonl). Não treina modelos.

Saída: CSVs agregados (sem identidades) em diagnostico_viabilidade/evidencias/
       e resumo_metricas.json com os números citados no relatório.
"""
import argparse
import hashlib
import json
import os
import re

import numpy as np
import pandas as pd

DATA_END = pd.Timestamp("2026-10-25", tz="UTC")       # fim da extração (manifest)
SINCE = pd.Timestamp("2020-01-01", tz="UTC")
LAST24 = DATA_END - pd.DateOffset(months=24)
DONE_STATUS = {"Resolved", "Closed", "Done"}
BOT_KEYS = ["githubbot", "jira-bot", "hudson", "hadoopqa", "asfgit", "jiraposter"]
M = {}  # métricas citadas no relatório


def ts(s):
    return pd.to_datetime(s, utc=True, errors="coerce", format="ISO8601")


def pct(a, b):
    return round(100.0 * a / b, 2) if b else None


def proj_cov(df, flag, min_n, label):
    """Distribuição por projeto de uma taxa de cobertura (flag booleana)."""
    g = df.groupby("project")[flag].agg(["size", "mean"])
    g = g[g["size"] >= min_n]
    return {
        f"{label}_projetos_elegiveis(n>={min_n})": int(len(g)),
        f"{label}_projetos_cobertura>=50%": int((g["mean"] >= .5).sum()),
        f"{label}_projetos_cobertura>=80%": int((g["mean"] >= .8).sum()),
        f"{label}_mediana_cobertura_projeto_%": round(100 * g["mean"].median(), 1) if len(g) else None,
        f"{label}_p90_cobertura_projeto_%": round(100 * g["mean"].quantile(.9), 1) if len(g) else None,
    }


def save(df, out, name):
    df.to_csv(os.path.join(out, name), index=False, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=os.environ.get("ALINE_JIRA_DATA_DIR"), required=os.environ.get("ALINE_JIRA_DATA_DIR") is None)
    ap.add_argument("--cache", default=os.environ.get("ALINE_CACHE_DIR"), required=os.environ.get("ALINE_CACHE_DIR") is None)
    ap.add_argument("--out", default=os.environ.get("ALINE_EVIDENCIAS_DIR"), required=os.environ.get("ALINE_EVIDENCIAS_DIR") is None)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    salt = open(os.path.join(a.cache, ".salt")).read().strip()
    bot_h = {hashlib.sha256((salt + k).encode()).hexdigest()[:12] for k in BOT_KEYS}

    # ------------------------------------------------------------------ issues
    I = pd.read_csv(os.path.join(a.cache, "issues_c.csv"), dtype=str, keep_default_na=False)
    for c in ("created", "resolutiondate", "updated"):
        I[c] = ts(I[c].replace("", None))
    for c in ("n_components", "n_links", "n_labels", "has_environment", "has_duedate", "worklog_total",
              "comment_total", "changelog_total", "n_sprints", "is_subtask", "has_epic_link", "n_subtasks"):
        I[c] = pd.to_numeric(I[c], errors="coerce").fillna(0).astype(int)
    I["valid_created"] = I["created"] >= pd.Timestamp("2000-01-01", tz="UTC")
    I["cyear"] = I["created"].dt.year
    I["is_bug"] = I["issuetype"] == "Bug"
    M["issues_total"] = len(I)
    M["issues_created_invalid(<2000)"] = int((~I["valid_created"]).sum())
    M["issues_created>=2020"] = int((I["created"] >= SINCE).sum())
    M["issues_created_pre2020_no_recorte"] = int(((I["created"] < SINCE) & I["valid_created"]).sum())
    M["projetos_com_issues"] = int(I["project"].nunique())
    M["bugs_total"] = int(I["is_bug"].sum())
    M["bugs_created>=2020"] = int((I["is_bug"] & (I["created"] >= SINCE)).sum())

    # distribuição temporal geral
    yr = (I[I["valid_created"]].groupby(["cyear"]).agg(issues=("issue_id", "size"), bugs=("is_bug", "sum"),
                                                        projetos=("project", "nunique")).reset_index())
    save(yr, a.out, "base_issues_por_ano_criacao.csv")

    # ---------------------------------------------------------------- changelog
    C = pd.read_csv(os.path.join(a.cache, "changelog_c.csv"), dtype=str, keep_default_na=False)
    C["ts"] = ts(C["ts"])
    C = C.sort_values(["issue_id", "ts", "history_id"], kind="stable")
    bug_ids = set(I.loc[I["is_bug"], "issue_id"])
    created_map = I.set_index("issue_id")["created"]

    # ================================================================ OBJ 1
    V = pd.read_json(os.path.join(a.base, "versions.jsonl"), lines=True, dtype=False)
    V["id"] = V["id"].astype(str)
    V["rel"] = ts(V["releaseDate"]) if "releaseDate" in V else pd.NaT
    V["start"] = ts(V["startDate"]) if "startDate" in V else pd.NaT
    V["released"] = V["released"].fillna(False).astype(bool)
    M["versoes_total"] = len(V)
    M["versoes_released"] = int(V["released"].sum())
    M["versoes_released_com_releaseDate"] = int((V["released"] & V["rel"].notna()).sum())
    M["versoes_com_startDate_%"] = pct(V["start"].notna().sum(), len(V))
    R = V[V["released"] & V["rel"].notna()].copy()
    R["ryear"] = R["rel"].dt.year
    M["releases_T0>=2020"] = int((R["rel"] >= SINCE).sum())
    M["releases_T0_ultimos24m"] = int((R["rel"] >= LAST24).sum())
    M["releases_futuras(>fim)"] = int((R["rel"] > DATA_END).sum())
    R = R[R["rel"] <= DATA_END]
    save(R.groupby("ryear").agg(releases=("id", "size"), projetos=("project_key", "nunique")).reset_index(),
         a.out, "obj1_releases_por_ano.csv")
    # modularidade: nome com prefixo não numérico, várias releases no mesmo dia
    R["nome_modular"] = R["name"].astype(str).str.match(r"^[A-Za-z][A-Za-z0-9_.\- ]*[-_ ]v?\d")
    R2 = R[R["rel"] >= SINCE]
    pp = R2.groupby("project_key").agg(releases=("id", "size"), modular=("nome_modular", "mean"),
                                       dias_distintos=("rel", "nunique")).reset_index()
    pp["releases_por_dia_distinto"] = (pp["releases"] / pp["dias_distintos"]).round(2)
    M["obj1_projetos_com_release>=2020"] = int(len(pp))
    M["obj1_projetos_com>=10_releases>=2020"] = int((pp["releases"] >= 10).sum())
    M["obj1_projetos_versionamento_modular(>=30%nomes)"] = int((pp["modular"] >= .3).sum())
    M["obj1_projetos_>=1.5_releases_mesmo_dia"] = int((pp["releases_por_dia_distinto"] >= 1.5).sum())

    # vínculos issue-versão (estado final)
    def explode(col):
        x = I[["issue_id", "project", "is_bug", "created", col]].copy()
        x = x[x[col] != ""]
        x[col] = x[col].str.split("|")
        return x.explode(col).rename(columns={col: "version_id"})
    AV, FV = explode("affects_versions"), explode("fix_versions")
    bugs20 = I[I["is_bug"] & (I["created"] >= SINCE)]
    M["obj1_bugs>=2020_com_affects_version_%"] = pct((bugs20["affects_versions"] != "").sum(), len(bugs20))
    M["obj1_bugs>=2020_com_fix_version_%"] = pct((bugs20["fix_versions"] != "").sum(), len(bugs20))
    M.update(proj_cov(bugs20.assign(av=bugs20["affects_versions"] != ""), "av", 100, "obj1_affects_version_bugs"))
    rel_ids = set(R2["id"])
    av_rel = AV[AV["is_bug"] & AV["version_id"].isin(rel_ids)].groupby("version_id").size()
    fv_rel = FV[FV["version_id"].isin(rel_ids)].groupby("version_id").size()
    R2 = R2.assign(bugs_affects=R2["id"].map(av_rel).fillna(0).astype(int),
                   issues_fixversion=R2["id"].map(fv_rel).fillna(0).astype(int))
    M["obj1_releases>=2020_com_>=1_bug_affects_%"] = pct((R2["bugs_affects"] > 0).sum(), len(R2))
    M["obj1_releases>=2020_com_>=1_issue_fixversion_%"] = pct((R2["issues_fixversion"] > 0).sum(), len(R2))
    M["obj1_releases>=2020_desfecho_zero_bugs_affects_%"] = pct((R2["bugs_affects"] == 0).sum(), len(R2))
    # janelas de acompanhamento e bugs criados após T0 (associação temporal, mesmo projeto)
    bugs_by_proj = {p: np.sort(g["created"].values.astype("datetime64[ns]"))
                    for p, g in I[I["is_bug"] & I["valid_created"]].groupby("project")}
    wrows = []
    for w in (7, 30, 90, 180):
        ok = R2["rel"] + pd.Timedelta(days=w) <= DATA_END
        cnt = []
        for p, t0 in zip(R2["project_key"], R2["rel"]):
            arr = bugs_by_proj.get(p)
            if arr is None:
                cnt.append(0)
                continue
            t0n = np.datetime64(t0.tz_convert(None))
            cnt.append(int(np.searchsorted(arr, t0n + np.timedelta64(w, "D")) - np.searchsorted(arr, t0n)))
        cnt = np.array(cnt)
        wrows.append({"janela_dias": w, "releases>=2020": len(R2),
                      "com_acompanhamento_completo": int(ok.sum()),
                      "com_acompanhamento_completo_%": pct(ok.sum(), len(R2)),
                      "mediana_bugs_criados_no_projeto_na_janela": float(np.median(cnt[ok.values])) if ok.any() else None,
                      "releases_sem_bug_criado_na_janela_%": pct((cnt[ok.values] == 0).sum(), ok.sum()),
                      "releases_com_outra_release_do_projeto_na_janela_%": pct(sum(
                          int(((s > t) & (s <= t + pd.Timedelta(days=w))).any())
                          for _, s in R2.groupby("project_key")["rel"] for t in s), len(R2))})
    save(pd.DataFrame(wrows), a.out, "obj1_janelas_pos_release.csv")
    # momento de atribuição da Fix Version vs T0 (composição conhecida em T0?)
    fvc = C[C["field"] == "Fix Version"]
    add = fvc[fvc["to"] != ""][["issue_id", "ts", "to"]].rename(columns={"to": "version_id"})
    last_add = add.groupby(["issue_id", "version_id"])["ts"].max()
    pairs = FV[FV["version_id"].isin(rel_ids)][["issue_id", "version_id", "created"]].copy()
    pairs["t_assign"] = [last_add.get((i, v), c) for i, v, c in
                         zip(pairs["issue_id"], pairs["version_id"], pairs["created"])]
    pairs["sem_evento"] = [(i, v) not in last_add.index for i, v in zip(pairs["issue_id"], pairs["version_id"])]
    relmap = R2.set_index("id")["rel"]
    pairs["T0"] = pairs["version_id"].map(relmap)
    pairs["antes_T0"] = pairs["t_assign"] <= pairs["T0"] + pd.Timedelta(days=1)
    M["obj1_pares_issue_fixversion(release>=2020)"] = len(pairs)
    M["obj1_fixversion_atribuida_ate_T0_%"] = pct(pairs["antes_T0"].sum(), len(pairs))
    M["obj1_fixversion_sem_evento_changelog_%"] = pct(pairs["sem_evento"].sum(), len(pairs))
    lag = (pairs["t_assign"] - pairs["T0"]).dt.days
    M["obj1_fixversion_atribuida>30d_apos_T0_%"] = pct((lag > 30).sum(), len(pairs))
    # versão afetada atribuída depois da abertura do bug
    vc = C[(C["field"] == "Version") & (C["to"] != "") & C["issue_id"].isin(bug_ids)]
    M["obj1_bugs_com_affects_version_adicionada_apos_criacao_%"] = pct(
        vc["issue_id"].nunique(), (I["is_bug"] & (I["affects_versions"] != "")).sum())
    # relação projeto: releases x bugs (exploratória, descritiva)
    pb = bugs20.groupby("project").size()
    pp["bugs>=2020"] = pp["project_key"].map(pb).fillna(0).astype(int)
    M["obj1_spearman_releases_x_bugs_por_projeto(>=2020)"] = round(
        pp[["releases", "bugs>=2020"]].corr(method="spearman").iloc[0, 1], 3)
    pp["share_issues_fixversion"] = pp["project_key"].map(
        I[I["created"] >= SINCE].assign(f=lambda d: d["fix_versions"] != "").groupby("project")["f"].mean()).round(3)
    pp["share_bugs_affects"] = pp["project_key"].map(
        bugs20.assign(f=lambda d: d["affects_versions"] != "").groupby("project")["f"].mean()).round(3)
    pp = pp.sort_values("releases", ascending=False)
    pp["elegivel_ilustrativo(>=10rel,>=100bugs,>=50%affects)"] = (
        (pp["releases"] >= 10) & (pp["bugs>=2020"] >= 100) & (pp["share_bugs_affects"] >= .5))
    M["obj1_projetos_subconjunto(>=10rel,>=100bugs,>=50%affects)"] = int(pp.iloc[:, -1].sum())
    M["obj1_releases_no_subconjunto"] = int(pp.loc[pp.iloc[:, -1], "releases"].sum())
    save(pp, a.out, "obj1_projetos_releases_bugs.csv")

    # ================================================================ OBJ 2
    st = C[C["field"] == "status"][["issue_id", "ts", "from_str", "to_str"]]
    rs = C[C["field"] == "resolution"][["issue_id", "ts", "to_str"]]
    first_res = rs[rs["to_str"] != ""].groupby("issue_id")["ts"].min()
    n_res = rs[rs["to_str"] != ""].groupby("issue_id").size()
    reopen = st[st["from_str"].isin(DONE_STATUS) & ~st["to_str"].isin(DONE_STATUS)]
    n_reopen = reopen.groupby("issue_id").size()
    pr = C[C["field"] == "priority"]
    pr_first = pr.groupby("issue_id").first()
    asg = C[C["field"] == "assignee"]
    asg_first = asg.groupby("issue_id").first()
    B = I[I["is_bug"] & I["valid_created"]].copy()
    B["first_res"] = B["issue_id"].map(first_res)
    B["first_res"] = B["first_res"].fillna(B["resolutiondate"])     # resolução sem evento (definida na criação/importação)
    B["n_res_events"] = B["issue_id"].map(n_res).fillna(0).astype(int)
    B["n_reopen"] = B["issue_id"].map(n_reopen).fillna(0).astype(int)
    B["open"] = B["resolution"] == ""
    B["prio_changed"] = B["issue_id"].isin(pr_first.index)
    B["prio_t0"] = np.where(B["prio_changed"], B["issue_id"].map(pr_first["from_str"]), B["priority"])
    B["asg_changed"] = B["issue_id"].isin(asg_first.index)
    B["asg_t0_present"] = np.where(B["asg_changed"], B["issue_id"].map(asg_first["from_str"]).fillna("") != "",
                                   B["assignee_h"] != "")
    B20 = B[B["created"] >= SINCE]
    M["obj2_bugs>=2020"] = len(B20)
    M["obj2_bugs>=2020_abertos_%"] = pct(B20["open"].sum(), len(B20))
    M["obj2_bugs>=2020_resolution_Fixed_%"] = pct((B20["resolution"] == "Fixed").sum(), len(B20))
    M["obj2_bugs>=2020_resolvidos_nao_Fixed_%"] = pct(((~B20["open"]) & (B20["resolution"] != "Fixed")).sum(), len(B20))
    M["obj2_bugs>=2020_com_reabertura_%"] = pct((B20["n_reopen"] > 0).sum(), len(B20))
    M["obj2_bugs>=2020_primeira_resolucao_difere_da_vigente_%"] = pct(
        ((B20["first_res"].notna()) & (B20["resolutiondate"].notna()) &
         ((B20["resolutiondate"] - B20["first_res"]).abs() > pd.Timedelta(minutes=1))).sum(), (~B20["open"]).sum())
    M["obj2_bugs>=2020_prioridade_alterada_apos_abertura_%"] = pct(B20["prio_changed"].sum(), len(B20))
    M["obj2_bugs>=2020_assignee_presente_na_abertura_%"] = pct(B20["asg_t0_present"].sum(), len(B20))
    M["obj2_bugs>=2020_assignee_atual_presente_%"] = pct((B20["assignee_h"] != "").sum(), len(B20))
    M["obj2_bugs>=2020_assignee_alterado_%"] = pct(B20["asg_changed"].sum(), len(B20))
    save(B20["resolution"].replace("", "(aberto)").value_counts().rename_axis("resolution")
         .reset_index(name="bugs"), a.out, "obj2_resolucoes_bugs_desde2020.csv")
    fixed = B20[(B20["resolution"] == "Fixed") & B20["first_res"].notna()].copy()
    fixed["dias"] = (fixed["first_res"] - fixed["created"]).dt.total_seconds() / 86400
    bins = [-1e-9, 1, 7, 30, 90, 365, 1e9]
    labels = ["<=1d", "1-7d", "7-30d", "30-90d", "90-365d", ">365d"]
    fixed["faixa"] = pd.cut(fixed["dias"], bins, labels=labels)
    fx = fixed["faixa"].value_counts().reindex(labels).rename_axis("faixa").reset_index(name="bugs_fixed")
    fx["%"] = (100 * fx["bugs_fixed"] / fx["bugs_fixed"].sum()).round(1)
    save(fx, a.out, "obj2_faixas_tempo_primeira_resolucao_fixed.csv")
    M["obj2_mediana_dias_fixed"] = round(float(fixed["dias"].median()), 1)
    M["obj2_bugs_fixed_tempo_negativo_ou_zero"] = int((fixed["dias"] <= 0).sum())
    # censura por coorte anual
    cohort = []
    for y, g in B20.groupby("cyear"):
        d = (g["first_res"] - g["created"]).dt.days
        row = {"ano_criacao": int(y), "bugs": len(g), "abertos_%": pct(g["open"].sum(), len(g)),
               "fixed_%": pct((g["resolution"] == "Fixed").sum(), len(g))}
        for w in (30, 90, 365):
            row[f"resolvidos_em_{w}d_%"] = pct((d <= w).sum(), len(g))
            row[f"coorte_com_{w}d_observaveis"] = bool(pd.Timestamp(f"{int(y)}-12-31", tz="UTC")
                                                       + pd.Timedelta(days=w) <= DATA_END)
        cohort.append(row)
    save(pd.DataFrame(cohort), a.out, "obj2_coortes_anuais_censura.csv")
    M.update(proj_cov(B20.assign(f=B20["resolution"] == "Fixed"), "f", 200, "obj2_fixed"))
    M["obj2_bugs_ultimos24m"] = int((B["created"] >= LAST24).sum())
    M["obj2_bugs_ultimos24m_abertos_%"] = pct(B.loc[B["created"] >= LAST24, "open"].sum(), (B["created"] >= LAST24).sum())
    pj2 = B20.groupby("project").agg(bugs=("issue_id", "size"), abertos=("open", "mean"),
                                    fixed=("resolution", lambda s: (s == "Fixed").mean()),
                                    prio_alterada=("prio_changed", "mean")).reset_index()
    pj2 = pj2.sort_values("bugs", ascending=False)
    M["obj2_projetos_com>=200_bugs>=2020"] = int((pj2["bugs"] >= 200).sum())
    M["obj2_bugs_nos_projetos>=200"] = int(pj2.loc[pj2["bugs"] >= 200, "bugs"].sum())
    M["obj2_top10_projetos_share_bugs_%"] = pct(pj2["bugs"].head(10).sum(), pj2["bugs"].sum())
    save(pj2.round(3), a.out, "obj2_projetos_bugs.csv")

    # ================================================================ OBJ 3
    S = pd.read_json(os.path.join(a.base, "sprints.jsonl"), lines=True, dtype=False)
    for c in ("startDate", "endDate", "completeDate", "activatedDate"):
        S[c] = ts(S[c]) if c in S else pd.NaT
    S["id"] = S["id"].astype(str)
    IS = pd.read_json(os.path.join(a.base, "issue_sprints.jsonl"), lines=True, dtype=False)
    IS["sprint_id"] = IS["sprint_id"].astype(str)
    IS["issue_id"] = IS["issue_id"].astype(str)
    M["obj3_sprints"] = len(S)
    M["obj3_sprints_com_startDate_%"] = pct(S["startDate"].notna().sum(), len(S))
    M["obj3_sprints_com_completeDate_%"] = pct(S["completeDate"].notna().sum(), len(S))
    M["obj3_sprints_estado"] = S["state"].value_counts().to_dict()
    M["obj3_issue_sprint_links"] = len(IS)
    M["obj3_issues_com_sprint"] = int(IS["issue_id"].nunique())
    M["obj3_issues_em_>1_sprint"] = int((IS.groupby("issue_id").size() > 1).sum())
    sp_proj = IS.groupby("sprint_id")["project_key"].agg(lambda s: s.mode().iat[0])
    S["project"] = S["id"].map(sp_proj)
    S["syear"] = S["startDate"].dt.year
    # eventos de sprint no changelog (adição/remoção por id)
    sc = C[C["field"] == "Sprint"][["issue_id", "ts", "from", "to"]].copy()
    def ids(x):
        return set(t.strip() for t in str(x).split(",") if t.strip())
    ev = []
    for i, t, f, to in sc.itertuples(index=False):
        a_, b_ = ids(f), ids(to)
        for s in b_ - a_:
            ev.append((i, t, s, "add"))
        for s in a_ - b_:
            ev.append((i, t, s, "remove"))
    E = pd.DataFrame(ev, columns=["issue_id", "ts", "sprint_id", "op"])
    M["obj3_eventos_sprint_changelog"] = len(E)
    start = S.set_index("id")["startDate"]
    comp = S.set_index("id")["completeDate"]
    E["start"] = E["sprint_id"].map(start)
    adds = E[E["op"] == "add"].groupby(["issue_id", "sprint_id"])["ts"].min()
    rem_after = E[(E["op"] == "remove") & (E["ts"] > E["start"])].groupby("sprint_id")["issue_id"].nunique()
    IS["t_add"] = [adds.get((i, s)) for i, s in zip(IS["issue_id"], IS["sprint_id"])]
    IS["created"] = IS["issue_id"].map(created_map)
    IS["t_add"] = IS["t_add"].fillna(IS["created"])
    IS["start"] = IS["sprint_id"].map(start)
    IS["complete"] = IS["sprint_id"].map(comp)
    IS["planejada_inicio"] = IS["t_add"] <= IS["start"]
    IS["adicionada_depois"] = IS["t_add"] > IS["start"]
    IS["first_res"] = IS["issue_id"].map(first_res).fillna(IS["issue_id"].map(I.set_index("issue_id")["resolutiondate"]))
    IS["concluida_na_sprint"] = IS["first_res"].notna() & (IS["first_res"] <= IS["complete"])
    sp = IS.groupby("sprint_id").agg(issues_finais=("issue_id", "size"), planejadas=("planejada_inicio", "sum"),
                                    adicionadas_depois=("adicionada_depois", "sum"),
                                    concluidas=("concluida_na_sprint", "sum")).reset_index()
    sp = sp.merge(S[["id", "project", "state", "startDate", "endDate", "completeDate", "syear"]],
                  left_on="sprint_id", right_on="id", how="left")
    sp["removidas_apos_inicio"] = sp["sprint_id"].map(rem_after).fillna(0).astype(int)
    sp["reconstruivel"] = (sp["startDate"].notna() & sp["completeDate"].notna() & (sp["issues_finais"] >= 5))
    M["obj3_sprints_reconstruiveis(datas+>=5 issues)"] = int(sp["reconstruivel"].sum())
    M["obj3_sprints_reconstruiveis_inicio>=2020"] = int((sp["reconstruivel"] & (sp["startDate"] >= SINCE)).sum())
    M["obj3_sprints_reconstruiveis_ultimos24m"] = int((sp["reconstruivel"] & (sp["startDate"] >= LAST24)).sum())
    M["obj3_pares_issue_sprint_reconstruiveis"] = int(sp.loc[sp["reconstruivel"], "issues_finais"].sum())
    M["obj3_pares_com_evento_adicao_%"] = pct(sum(1 for i, s in zip(IS["issue_id"], IS["sprint_id"]) if (i, s) in adds.index), len(IS))
    psum = sp[sp["reconstruivel"]].groupby("project").agg(
        sprints=("sprint_id", "size"), pares=("issues_finais", "sum"), planejadas=("planejadas", "sum"),
        adicionadas=("adicionadas_depois", "sum"), concluidas=("concluidas", "sum"),
        primeiro=("startDate", "min"), ultimo=("startDate", "max")).reset_index().sort_values("sprints", ascending=False)
    psum["primeiro"] = psum["primeiro"].dt.date
    psum["ultimo"] = psum["ultimo"].dt.date
    M["obj3_projetos_com_sprints_reconstruiveis"] = int(len(psum))
    M["obj3_projetos_com>=10_sprints_reconstruiveis"] = int((psum["sprints"] >= 10).sum())
    M["obj3_pares_nos_projetos>=10_sprints"] = int(psum.loc[psum["sprints"] >= 10, "pares"].sum())
    nc = sp[sp["reconstruivel"]]
    M["obj3_taxa_nao_conclusao_pares_reconstruiveis_%"] = pct((nc["issues_finais"] - nc["concluidas"]).sum(),
                                                              nc["issues_finais"].sum())
    save(psum, a.out, "obj3_projetos_sprints.csv")
    save(sp.groupby("syear").agg(sprints=("sprint_id", "size"), reconstruiveis=("reconstruivel", "sum"),
                                 pares=("issues_finais", "sum")).reset_index(), a.out, "obj3_sprints_por_ano.csv")
    spi = I[I["issue_id"].isin(set(IS["issue_id"]))]
    M["obj3_issues_em_sprint_com_story_points_%"] = pct((spi["story_points"] != "").sum(), len(spi))
    M["obj3_issues_em_sprint_com_estimativa_tempo_%"] = pct((spi["timeoriginalestimate"] != "").sum(), len(spi))

    # ================================================================ OBJ 4
    W = pd.read_csv(os.path.join(a.cache, "worklogs_c.csv"), dtype=str, keep_default_na=False)
    W["seconds"] = pd.to_numeric(W["seconds"], errors="coerce").fillna(0)
    W["bot"] = W["author_h"].isin(bot_h)
    W["started"] = ts(W["started"])
    meta = I.set_index("issue_id")[["project", "issuetype"]]
    W = W.join(meta, on="issue_id")
    M["obj4_worklogs_total"] = len(W)
    M["obj4_worklogs_conta_automatica_%"] = pct(W["bot"].sum(), len(W))
    M["obj4_horas_total"] = round(W["seconds"].sum() / 3600, 1)
    M["obj4_horas_conta_automatica_%"] = pct(W.loc[W["bot"], "seconds"].sum(), W["seconds"].sum())
    Wh = W[~W["bot"]]
    M["obj4_worklogs_humanos"] = len(Wh)
    M["obj4_horas_humanas"] = round(Wh["seconds"].sum() / 3600, 1)
    M["obj4_issues_com_worklog_humano"] = int(Wh["issue_id"].nunique())
    M["obj4_projetos_com_worklog_humano"] = int(Wh["project"].nunique())
    M["obj4_autores_worklog_humano"] = int(Wh["author_h"].nunique())
    M["obj4_worklogs_humanos_desde2020"] = int((Wh["started"] >= SINCE).sum())
    M["obj4_worklogs_humanos_ultimos24m"] = int((Wh["started"] >= LAST24).sum())
    M["obj4_bot_mediana_segundos_por_registro"] = float(W.loc[W["bot"], "seconds"].median())
    wp = Wh.groupby("project").agg(worklogs=("worklog_id", "size"), issues=("issue_id", "nunique"),
                                   autores=("author_h", "nunique"), horas=("seconds", lambda s: round(s.sum() / 3600, 1)))
    wp = wp.reset_index().sort_values("worklogs", ascending=False)
    wp["share_top1_autor_%"] = wp["project"].map(
        Wh.groupby(["project", "author_h"]).size().groupby(level=0).apply(lambda s: round(100 * s.max() / s.sum(), 1)))
    save(wp, a.out, "obj4_worklogs_humanos_por_projeto.csv")
    wy = W.assign(ano=W["started"].dt.year).groupby(["ano", "bot"]).agg(
        worklogs=("worklog_id", "size"), horas=("seconds", lambda s: round(s.sum() / 3600, 1))).reset_index()
    wy["origem"] = np.where(wy["bot"], "conta automatica", "demais contas")
    save(wy.drop(columns="bot"), a.out, "obj4_worklogs_por_ano_origem.csv")
    I20 = I[I["created"] >= SINCE]
    tmap = {"Bug": "correcao (proxy)", "Improvement": "evolucao (proxy)", "New Feature": "evolucao (proxy)",
            "Wish": "evolucao (proxy)", "Story": "evolucao (proxy)", "Epic": "evolucao (proxy)",
            "Task": "outras/sustentacao? (indefinido)", "Sub-task": "outras/sustentacao? (indefinido)",
            "Test": "outras", "Documentation": "outras", "Dependency upgrade": "outras/sustentacao? (indefinido)",
            "Question": "outras"}
    ty = I20.assign(classe_proxy=I20["issuetype"].map(tmap).fillna("outras"), aberta=I20["resolution"] == "")
    tys = ty.groupby(["cyear", "issuetype", "classe_proxy"]).agg(issues=("issue_id", "size"),
                                                                 abertas=("aberta", "sum")).reset_index()
    tys = tys[tys["issues"] >= 50]
    save(tys, a.out, "obj4_tipos_issue_por_ano.csv")
    M["obj4_tipos_issue_distintos>=2020"] = int(I20["issuetype"].nunique())
    M["obj4_share_tipos_top5_>=2020"] = I20["issuetype"].value_counts(normalize=True).head(5).round(3).to_dict()
    M["obj4_issues>=2020_com_assignee_atual_%"] = pct((I20["assignee_h"] != "").sum(), len(I20))
    asg_n = asg.groupby("issue_id").size()
    M["obj4_issues>=2020_com_historico_atribuicao_%"] = pct(I20["issue_id"].isin(asg_n.index).sum(), len(I20))
    CM = pd.read_csv(os.path.join(a.cache, "comments_c.csv"), dtype=str, keep_default_na=False,
                     usecols=["issue_id", "author_h"])
    CM["bot"] = CM["author_h"].isin(bot_h)
    M["obj4_comentarios_conta_automatica_%"] = pct(CM["bot"].sum(), len(CM))
    ch = CM[~CM["bot"]].groupby("issue_id")["author_h"].nunique()
    M["obj4_issues>=2020_mediana_autores_humanos_comentario"] = float(I20["issue_id"].map(ch).fillna(0).median())
    # concentração: participação do assignee mais frequente por projeto (sem identificar pessoas)
    ag = I20[I20["assignee_h"] != ""].groupby(["project", "assignee_h"]).size()
    conc = ag.groupby(level=0).agg(lambda s: s.max() / s.sum())
    nproj = ag.groupby(level=0).sum()
    conc = conc[nproj >= 100]
    M["obj4_projetos(>=100 issues atribuidas)_share_top1_assignee_mediana_%"] = round(100 * conc.median(), 1)

    # ================================================================ OBJ 5
    rp = reopen.merge(st[st["to_str"].isin(DONE_STATUS)][["issue_id", "ts"]].rename(columns={"ts": "t_done"}),
                      on="issue_id")
    rp = rp[rp["t_done"] <= rp["ts"]].groupby(["issue_id", "ts"])["t_done"].max().reset_index()
    rp["dias"] = (rp["ts"] - rp["t_done"]).dt.total_seconds() / 86400
    rp = rp[rp["issue_id"].isin(set(B20["issue_id"]))]
    M["obj5_bugs>=2020_resolvidos"] = int((~B20["open"]).sum() + ((B20["open"]) & (B20["n_reopen"] > 0)).sum())
    M["obj5_bugs>=2020_reabertos"] = int((B20["n_reopen"] > 0).sum())
    M["obj5_bugs>=2020_reabertos_%_dos_resolvidos_alguma_vez"] = pct(
        (B20["n_reopen"] > 0).sum(), (B20["first_res"].notna() | (B20["n_reopen"] > 0)).sum())
    M["obj5_reaberturas_mediana_dias_apos_resolucao"] = round(float(rp["dias"].median()), 1) if len(rp) else None
    M["obj5_reaberturas_<=30d_%"] = pct((rp["dias"] <= 30).sum(), len(rp))
    M["obj5_bugs_reabertos_>1_vez"] = int((B20["n_reopen"] > 1).sum())
    M.update(proj_cov(B20.assign(r=B20["n_reopen"] > 0), "r", 200, "obj5_reabertura"))
    M["obj5_bugs>=2020_resolution_Duplicate_%"] = pct((B20["resolution"] == "Duplicate").sum(), len(B20))
    M["obj5_bugs>=2020_com_link_duplicate_%"] = pct(B20["link_types"].str.contains("Duplicate").sum(), len(B20))
    M["obj5_bugs>=2020_com_algum_link_%"] = pct((B20["n_links"] > 0).sum(), len(B20))
    M["obj5_bugs>=2020_com_componente_%"] = pct((B20["n_components"] > 0).sum(), len(B20))
    lt = B20["link_types"].str.split("|").explode()
    save(lt[lt != ""].str.rstrip("<>").value_counts().rename_axis("tipo_link").reset_index(name="ocorrencias_em_bugs"),
         a.out, "obj5_tipos_link_bugs_desde2020.csv")
    crit = {"severity_fields": "Severity (6 campos distintos)", "has_environment": "Environment",
            "bug_category": "Bug Category", "regression": "Regression", "flags": "Flags",
            "platform": "Platform", "labels": "Labels (texto livre)"}
    rows, pc = [], []
    for col, lab in crit.items():
        f = (B20["n_labels"] > 0) if col == "labels" else (B20[col].astype(str).isin(["", "0"]) == False)
        g = B20.assign(f=f).groupby("project")["f"].agg(["size", "mean"])
        g = g[g["size"] >= 100]
        rows.append({"campo": lab, "bugs>=2020_preenchidos_%": pct(f.sum(), len(B20)),
                     "projetos(>=100 bugs)": len(g), "projetos_cobertura>=50%": int((g["mean"] >= .5).sum()),
                     "projetos_cobertura>=80%": int((g["mean"] >= .8).sum()),
                     "bugs_nos_projetos>=50%": int(g.loc[g["mean"] >= .5, "size"].sum())})
    save(pd.DataFrame(rows), a.out, "obj5_campos_criticidade.csv")
    sevv = B20.loc[B20["severity_value"] != "", "severity_value"].value_counts().head(15)
    save(sevv.rename_axis("valor_severity").reset_index(name="bugs"), a.out, "obj5_valores_severity.csv")
    pri = B20.assign(prio_t0=B20["prio_t0"]).groupby("project")
    pc = B20.groupby("project").agg(bugs=("issue_id", "size"), reabertos=("n_reopen", lambda s: (s > 0).mean()),
                                    prio_alterada=("prio_changed", "mean"),
                                    duplicate=("resolution", lambda s: (s == "Duplicate").mean())).reset_index()
    save(pc[pc["bugs"] >= 200].sort_values("bugs", ascending=False).round(3), a.out, "obj5_projetos_retrabalho.csv")
    M["obj5_prioridades_distintas_bugs>=2020"] = B20["priority"].value_counts().head(10).to_dict()

    # ======================================================== PERÍODOS
    per = []
    for nome, ini in (("desde 2020-01-01", SINCE), ("ultimos 24 meses", LAST24)):
        b = B[B["created"] >= ini]
        per.append({"recorte": nome, "inicio": ini.date(),
                    "issues_criadas": int((I["created"] >= ini).sum()), "bugs_criados": len(b),
                    "bugs_abertos_%": pct(b["open"].sum(), len(b)),
                    "releases_T0": int((R["rel"] >= ini).sum()),
                    "releases_T0_com_180d_observaveis": int(((R["rel"] >= ini) &
                                                             (R["rel"] + pd.Timedelta(days=180) <= DATA_END)).sum()),
                    "sprints_reconstruiveis": int((sp["reconstruivel"] & (sp["startDate"] >= ini)).sum()),
                    "worklogs_humanos": int((Wh["started"] >= ini).sum()),
                    "bugs_reabertos": int((b["n_reopen"] > 0).sum())})
    save(pd.DataFrame(per), a.out, "periodos_comparacao.csv")
    # população coletada pré-2020: viés de seleção (apenas abertas ou atualizadas >=2020)
    pre = I[(I["created"] < SINCE) & I["valid_created"]]
    M["vies_pre2020_issues_abertas_%"] = pct((pre["resolution"] == "").sum(), len(pre))
    M["vies_desde2020_issues_abertas_%"] = pct((I20["resolution"] == "").sum(), len(I20))

    with open(os.path.join(a.out, "resumo_metricas.json"), "w", encoding="utf-8") as f:
        json.dump(M, f, ensure_ascii=False, indent=1, default=str)
    for k, v in M.items():
        print(k, "=", v)


if __name__ == "__main__":
    main()
