#!/usr/bin/env python3
"""
Caracterização POR PROJETO (unidade primária) e segunda camada de heterogeneidade
entre projetos. Diagnóstico apenas: nenhum modelo é treinado.

Entradas: cache de 01_projetar_base.py; versions.jsonl da base; evidências de
03_diagnostico_cobertura.py (obj3_projetos_sprints.csv, obj4_worklogs_humanos_por_projeto.csv).

Recorte global comum: eventos com T0 >= 2020-01-01; fim da observação 2026-10-25.
Split cronológico comum (parâmetro de diagnóstico, não decisão final):
  treino = T0 em 2020-01-01..2023-12-31
  teste  = T0 em 2024-01-01..(fim - horizonte do desfecho)
Horizontes: bug -> faixa de tempo em 90 dias; resolução -> reabertura em 90 dias;
release -> bugs vinculados (Affects Version) em 180 dias.

Critérios de "modelo individual" (regra de bolso de eventos por variável, ~10
preditores x 10 eventos): ver CRITERIOS abaixo; registrados no CSV de saída.

Saídas em evidencias/:
  projetos_caracterizacao.csv        1 linha por projeto (indicadores)
  projetos_viabilidade_modelos.csv   1 linha por projeto x objetivo (n treino/teste, eventos, classificação)
  heterogeneidade_entre_projetos.csv segunda camada (dispersão e eta² entre projetos)
  fichas_projetos.md                 conclusões por projeto (projetos com volume relevante)
"""
import argparse
import json
import os
import re

import numpy as np
import pandas as pd

DATA_END = pd.Timestamp("2026-10-25", tz="UTC")
SINCE = pd.Timestamp("2020-01-01", tz="UTC")
TRAIN_END = pd.Timestamp("2024-01-01", tz="UTC")
H_BUG, H_REOPEN, H_REL = 90, 90, 180
DONE_STATUS = {"Resolved", "Closed", "Done"}
CRITERIOS = {
    "obj1_individual": "releases treino>=50, teste>=15, Affects Version>=50% dos bugs, nomes modulares<30%",
    "obj1_agrupado": "releases treino>=10 e Affects Version>=50% (entra em modelo multinível/efeito fixo)",
    "obj2_individual": "bugs treino>=500, menor faixa no treino>=50, bugs teste>=150",
    "obj2_agrupado": "bugs treino>=100",
    "obj5_individual": "reaberturas(<=90d) treino>=100 e teste>=30",
    "obj5_agrupado": "reaberturas(<=90d) treino>=20",
    "obj3_caso": ">=10 sprints reconstruíveis e >=500 pares issue-sprint (após validação manual)",
    "obj4_horas": ">=50 worklogs de contas não automáticas",
}
BANDS = ["<=7d", "8-30d", "31-90d", ">90d ou nao Fixed"]


def ts(s):
    return pd.to_datetime(s, utc=True, errors="coerce", format="ISO8601")


def r(x, n=3):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), n)


def eta2(values, groups):
    """Proporção da variância explicada pelo projeto (ANOVA de um fator, descritiva)."""
    d = pd.DataFrame({"v": values, "g": groups}).dropna()
    if d["g"].nunique() < 2:
        return None
    m = d["v"].mean()
    sst = ((d["v"] - m) ** 2).sum()
    ssb = d.groupby("g")["v"].agg(lambda s: len(s) * (s.mean() - m) ** 2).sum()
    return r(ssb / sst if sst else None)


def module_prefix(name):
    m = re.match(r"^([A-Za-z][A-Za-z0-9_.\- ]*?)[-_ ]v?\d", str(name))
    return m.group(1).lower() if m else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=os.environ.get("ALINE_JIRA_DATA_DIR"), required=os.environ.get("ALINE_JIRA_DATA_DIR") is None)
    ap.add_argument("--cache", default=os.environ.get("ALINE_CACHE_DIR"), required=os.environ.get("ALINE_CACHE_DIR") is None)
    ap.add_argument("--ev", default=os.environ.get("ALINE_EVIDENCIAS_DIR"), required=os.environ.get("ALINE_EVIDENCIAS_DIR") is None, help="pasta evidencias (entrada e saída)")
    a = ap.parse_args()

    I = pd.read_csv(os.path.join(a.cache, "issues_c.csv"), dtype=str, keep_default_na=False)
    for c in ("created", "resolutiondate"):
        I[c] = ts(I[c].replace("", None))
    for c in ("n_components", "n_labels", "has_environment"):
        I[c] = pd.to_numeric(I[c], errors="coerce").fillna(0).astype(int)
    I = I[I["created"] >= pd.Timestamp("2000-01-01", tz="UTC")]
    I["cyear"] = I["created"].dt.year
    I20 = I[I["created"] >= SINCE]

    C = pd.read_csv(os.path.join(a.cache, "changelog_c.csv"), dtype=str, keep_default_na=False,
                    usecols=["issue_id", "ts", "field", "from", "from_str", "to", "to_str"])
    C = C[C["field"].isin(["status", "resolution", "priority", "assignee", "Version", "Fix Version",
                           "Component"])]
    C["ts"] = ts(C["ts"])
    C = C.sort_values(["issue_id", "ts"], kind="stable")

    # ---------------------------------------------------------------- bugs (T0 = criação)
    B = I20[I20["issuetype"] == "Bug"].copy()
    bug_ids = set(B["issue_id"])
    Cb = C[C["issue_id"].isin(bug_ids)]
    rs = Cb[(Cb["field"] == "resolution") & (Cb["to_str"] != "")]
    first_res = rs.groupby("issue_id")["ts"].min()
    first_fixed = rs[rs["to_str"] == "Fixed"].groupby("issue_id")["ts"].min()
    B["first_res"] = B["issue_id"].map(first_res).fillna(B["resolutiondate"])
    B["first_fixed"] = B["issue_id"].map(first_fixed)
    B.loc[B["first_fixed"].isna() & (B["resolution"] == "Fixed"), "first_fixed"] = B["resolutiondate"]
    B["open"] = B["resolution"] == ""
    B["days_fixed"] = (B["first_fixed"] - B["created"]).dt.total_seconds() / 86400
    pr_first = Cb[Cb["field"] == "priority"].groupby("issue_id").first()
    B["prio_changed"] = B["issue_id"].isin(pr_first.index)
    asg_first = Cb[Cb["field"] == "assignee"].groupby("issue_id").first()
    B["asg_t0"] = np.where(B["issue_id"].isin(asg_first.index),
                           B["issue_id"].map(asg_first["from_str"]).fillna("") != "", B["assignee_h"] != "")
    B["comp_changed"] = B["issue_id"].isin(set(Cb.loc[Cb["field"] == "Component", "issue_id"]))
    v_added = set(Cb.loc[(Cb["field"] == "Version") & (Cb["to"] != ""), "issue_id"])
    B["av_now"] = B["affects_versions"] != ""
    B["av_t0"] = B["av_now"] & ~B["issue_id"].isin(v_added)
    # faixa no horizonte de 90 dias (rotulável para toda coorte com 90 d observáveis)
    d = B["days_fixed"]
    B["band"] = np.select([d <= 7, d <= 30, d <= H_BUG], BANDS[:3], BANDS[3])
    B["obs_h"] = B["created"] + pd.Timedelta(days=H_BUG) <= DATA_END
    B["split"] = np.where(B["created"] < TRAIN_END, "treino", np.where(B["obs_h"], "teste", "fora"))
    # reaberturas em até 90 d após a primeira resolução (T0 = primeira resolução)
    st = Cb[Cb["field"] == "status"]
    reo = st[st["from_str"].isin(DONE_STATUS) & ~st["to_str"].isin(DONE_STATUS)][["issue_id", "ts"]]
    reo = reo.join(B.set_index("issue_id")["first_res"], on="issue_id")
    reo = reo[(reo["ts"] >= reo["first_res"]) &
              (reo["ts"] <= reo["first_res"] + pd.Timedelta(days=H_REOPEN))]
    B["reopen90"] = B["issue_id"].isin(set(reo["issue_id"]))
    B["ever_reopen"] = B["issue_id"].isin(set(st.loc[st["from_str"].isin(DONE_STATUS) &
                                                     ~st["to_str"].isin(DONE_STATUS), "issue_id"]))
    R5 = B[B["first_res"].notna() & (B["first_res"] >= SINCE)].copy()
    R5["split"] = np.where(R5["first_res"] < TRAIN_END, "treino",
                           np.where(R5["first_res"] + pd.Timedelta(days=H_REOPEN) <= DATA_END, "teste", "fora"))

    # ---------------------------------------------------------------- releases (T0 = releaseDate)
    V = pd.read_json(os.path.join(a.base, "versions.jsonl"), lines=True, dtype=False)
    V["id"] = V["id"].astype(str)
    V["rel"] = ts(V["releaseDate"])
    V["released"] = V["released"].fillna(False).astype(bool)
    R = V[V["released"] & V["rel"].notna() & (V["rel"] >= SINCE) & (V["rel"] <= DATA_END)].copy()
    R["prefix"] = R["name"].map(module_prefix)
    R["modular"] = R["prefix"] != ""
    AV = B[B["av_now"]][["issue_id", "affects_versions"]].assign(
        version_id=lambda x: x["affects_versions"].str.split("|")).explode("version_id")
    R["bugs_av"] = R["id"].map(AV.groupby("version_id").size()).fillna(0).astype(int)
    R["split"] = np.where(R["rel"] < TRAIN_END, "treino",
                          np.where(R["rel"] + pd.Timedelta(days=H_REL) <= DATA_END, "teste", "fora"))
    R = R.sort_values(["project_key", "rel"])
    R["gap"] = R.groupby("project_key")["rel"].diff().dt.days
    R["overlap90"] = R.groupby("project_key")["rel"].transform(
        lambda s: [int(((s > t) & (s <= t + pd.Timedelta(days=90))).any()) for t in s])
    # Fix Version atribuída até T0
    fva = C[(C["field"] == "Fix Version") & (C["to"] != "")].groupby(["issue_id", "to"])["ts"].max()
    FV = I[I["fix_versions"] != ""][["issue_id", "created", "fix_versions"]].assign(
        version_id=lambda x: x["fix_versions"].str.split("|")).explode("version_id")
    FV = FV[FV["version_id"].isin(set(R["id"]))]
    FV["t"] = [fva.get((i, v), c) for i, v, c in zip(FV["issue_id"], FV["version_id"], FV["created"])]
    FV = FV.join(R.set_index("id")[["rel", "project_key"]], on="version_id")
    FV["ate_T0"] = FV["t"] <= FV["rel"] + pd.Timedelta(days=1)
    FV["n_issues"] = 1
    rel_size = FV[FV["ate_T0"]].groupby("version_id").size()
    R["tamanho_T0"] = R["id"].map(rel_size).fillna(0).astype(int)

    sprints = pd.read_csv(os.path.join(a.ev, "obj3_projetos_sprints.csv"))
    whum = pd.read_csv(os.path.join(a.ev, "obj4_worklogs_humanos_por_projeto.csv"))

    # ---------------------------------------------------------------- por projeto
    proj = sorted(I["project"].unique())
    rows, viab = [], []
    tclass = {"Bug": "correcao", "Improvement": "evolucao", "New Feature": "evolucao", "Wish": "evolucao",
              "Story": "evolucao", "Epic": "evolucao"}
    gB, gR, gR5, gI = (dict(tuple(x.groupby(k))) for x, k in
                       ((B, "project"), (R, "project_key"), (R5, "project"), (I20, "project")))
    gFV = dict(tuple(FV.groupby("project_key")))
    sp_map = sprints.set_index("project").to_dict("index")
    wh_map = whum.set_index("project").to_dict("index")
    for p in proj:
        b = gB.get(p, B.iloc[0:0])
        rl = gR.get(p, R.iloc[0:0])
        r5 = gR5.get(p, R5.iloc[0:0])
        ii = gI.get(p, I20.iloc[0:0])
        fv = gFV.get(p, FV.iloc[0:0])
        sp = sp_map.get(p, {})
        wh = wh_map.get(p, {})
        fixed = b["days_fixed"].dropna()
        by_year = b.groupby("cyear").size()
        n_y = {f"bugs_{y}": int(by_year.get(y, 0)) for y in range(2020, 2027)}
        early = by_year.get(2020, 0) + by_year.get(2021, 0)
        late = by_year.get(2024, 0) + by_year.get(2025, 0)
        prios = b["priority"].value_counts(normalize=True)
        bpr = rl["bugs_av"]
        rows.append({
            "projeto": p,
            "issues_criadas>=2020": len(ii),
            "share_correcao_%": r(100 * (ii["issuetype"].map(tclass) == "correcao").mean(), 1) if len(ii) else None,
            "share_evolucao_%": r(100 * (ii["issuetype"].map(tclass) == "evolucao").mean(), 1) if len(ii) else None,
            "assignee_atual_%": r(100 * (ii["assignee_h"] != "").mean(), 1) if len(ii) else None,
            # releases
            "releases>=2020": len(rl),
            "releases_por_ano": r(len(rl) / ((DATA_END - SINCE).days / 365.25), 2),
            "intervalo_mediano_dias": r(rl["gap"].median(), 1),
            "releases_dias_distintos": int(rl["rel"].dt.date.nunique()),
            "nomes_modulares_%": r(100 * rl["modular"].mean(), 1) if len(rl) else None,
            "prefixos_modulo_distintos": int(rl.loc[rl["modular"], "prefix"].nunique()),
            "overlap_90d_%": r(100 * rl["overlap90"].mean(), 1) if len(rl) else None,
            "releases_com_bug_affects_%": r(100 * (bpr > 0).mean(), 1) if len(rl) else None,
            "bugs_affects_por_release_media": r(bpr.mean(), 2) if len(rl) else None,
            "bugs_affects_por_release_var/media": r(bpr.var() / bpr.mean(), 2) if len(rl) > 2 and bpr.mean() > 0 else None,
            "releases_zero_bugs_%": r(100 * (bpr == 0).mean(), 1) if len(rl) else None,
            "fixversion_ate_T0_%": r(100 * fv["ate_T0"].mean(), 1) if len(fv) else None,
            "tamanho_release_T0_mediana": r(rl["tamanho_T0"].median(), 1) if len(rl) else None,
            # bugs
            "bugs>=2020": len(b), **n_y,
            "tendencia_24-25_vs_20-21": r(late / early, 2) if early else None,
            "ultimo_bug_criado": b["created"].max().date() if len(b) else None,
            "serie_interrompida(>=100 bugs; nenhum nos ultimos 12m)": bool(
                len(b) >= 100 and b["created"].max() < DATA_END - pd.Timedelta(days=365)),
            "affects_version_%": r(100 * b["av_now"].mean(), 1) if len(b) else None,
            "affects_version_na_abertura_%": r(100 * b["av_t0"].mean(), 1) if len(b) else None,
            "abertos_%": r(100 * b["open"].mean(), 1) if len(b) else None,
            "fixed_%": r(100 * (b["resolution"] == "Fixed").mean(), 1) if len(b) else None,
            "dias_fixed_mediana": r(fixed.median(), 1) if len(fixed) else None,
            "dias_fixed_p75": r(fixed.quantile(.75), 1) if len(fixed) else None,
            "fixed_<=7d_%": r(100 * (fixed <= 7).mean(), 1) if len(fixed) else None,
            "reabertos_%": r(100 * b["ever_reopen"].mean(), 2) if len(b) else None,
            "reabertos_90d_n": int(b["reopen90"].sum()),
            # preditores
            "esquema_prioridade": "|".join(prios.head(4).index),
            "prioridade_dominante_%": r(100 * prios.iloc[0], 1) if len(prios) else None,
            "prioridade_alterada_%": r(100 * b["prio_changed"].mean(), 1) if len(b) else None,
            "assignee_na_abertura_%": r(100 * b["asg_t0"].mean(), 1) if len(b) else None,
            "componente_%": r(100 * (b["n_components"] > 0).mean(), 1) if len(b) else None,
            "componente_alterado_%": r(100 * b["comp_changed"].mean(), 1) if len(b) else None,
            "labels_%": r(100 * (b["n_labels"] > 0).mean(), 1) if len(b) else None,
            "severity_%": r(100 * (b["severity_fields"] != "").mean(), 1) if len(b) else None,
            "environment_%": r(100 * (b["has_environment"] > 0).mean(), 1) if len(b) else None,
            # sprints e horas
            "sprints_reconstruiveis": int(sp.get("sprints", 0) or 0),
            "pares_issue_sprint": int(sp.get("pares", 0) or 0),
            "worklogs_nao_automaticos": int(wh.get("worklogs", 0) or 0),
        })

        # viabilidade por objetivo (treino/teste no split comum)
        av_pct = b["av_now"].mean() if len(b) else 0
        rtr, rte = (rl["split"] == "treino").sum(), (rl["split"] == "teste").sum()
        mod = rl["modular"].mean() if len(rl) else 0
        if rtr >= 50 and rte >= 15 and av_pct >= .5 and mod < .3:
            c1 = "MODELO INDIVIDUAL VIAVEL"
        elif rtr >= 10 and av_pct >= .5:
            c1 = "AGRUPADO (multinivel/efeito fixo)" + (" - versoes modulares: tratar" if mod >= .3 else "")
        elif len(rl):
            c1 = "SOMENTE DESCRITIVO"
        else:
            c1 = "SEM DADOS"
        viab.append({"projeto": p, "objetivo": "1 releases-bugs (desfecho: bugs Affects Version em 180d)",
                     "n_treino": int(rtr), "n_teste": int(rte),
                     "eventos_treino": int(rl.loc[rl["split"] == "treino", "bugs_av"].gt(0).sum()),
                     "eventos_teste": int(rl.loc[rl["split"] == "teste", "bugs_av"].gt(0).sum()),
                     "cobertura_chave_%": r(100 * av_pct, 1), "classificacao": c1})
        btr, bte = b[b["split"] == "treino"], b[b["split"] == "teste"]
        minband = btr["band"].value_counts().reindex(BANDS).fillna(0).min() if len(btr) else 0
        if len(btr) >= 500 and minband >= 50 and len(bte) >= 150:
            c2 = "MODELO INDIVIDUAL VIAVEL"
        elif len(btr) >= 100:
            c2 = "AGRUPADO (multinivel/efeito fixo)"
        elif len(b) >= 30:
            c2 = "SOMENTE DESCRITIVO"
        else:
            c2 = "INSUFICIENTE"
        viab.append({"projeto": p, "objetivo": "2 faixa de tempo de correcao (horizonte 90d)",
                     "n_treino": len(btr), "n_teste": len(bte), "eventos_treino": int(minband),
                     "eventos_teste": int(bte["band"].value_counts().reindex(BANDS).fillna(0).min()) if len(bte) else 0,
                     "cobertura_chave_%": r(100 * b["asg_t0"].mean(), 1) if len(b) else None,
                     "classificacao": c2})
        etr = int(r5.loc[r5["split"] == "treino", "reopen90"].sum())
        ete = int(r5.loc[r5["split"] == "teste", "reopen90"].sum())
        if etr >= 100 and ete >= 30:
            c5 = "MODELO INDIVIDUAL VIAVEL"
        elif etr >= 20:
            c5 = "AGRUPADO (multinivel/efeito fixo)"
        elif len(r5) >= 30:
            c5 = "SOMENTE DESCRITIVO"
        else:
            c5 = "INSUFICIENTE"
        viab.append({"projeto": p, "objetivo": "5 reabertura em 90d apos primeira resolucao",
                     "n_treino": int((r5["split"] == "treino").sum()), "n_teste": int((r5["split"] == "teste").sum()),
                     "eventos_treino": etr, "eventos_teste": ete,
                     "cobertura_chave_%": r(100 * r5["reopen90"].mean(), 2) if len(r5) else None,
                     "classificacao": c5})
        ns, npairs = int(sp.get("sprints", 0) or 0), int(sp.get("pares", 0) or 0)
        viab.append({"projeto": p, "objetivo": "3 sprints (nao conclusao)", "n_treino": None, "n_teste": None,
                     "eventos_treino": ns, "eventos_teste": npairs, "cobertura_chave_%": None,
                     "classificacao": ("ESTUDO DE CASO (apos validacao)" if ns >= 10 and npairs >= 500 else
                                       "SOMENTE DESCRITIVO" if ns else "SEM DADOS")})
        nw = int(wh.get("worklogs", 0) or 0)
        viab.append({"projeto": p, "objetivo": "4 distribuicao do trabalho", "n_treino": len(ii), "n_teste": None,
                     "eventos_treino": nw, "eventos_teste": None, "cobertura_chave_%": None,
                     "classificacao": ("DEMANDAS: DESCRITIVO" if len(ii) >= 100 else "DEMANDAS: POUCOS DADOS")
                                      + ("; HORAS: DESCRITIVO LIMITADO" if nw >= 50 else "; HORAS: INDISPONIVEL")})

    P = pd.DataFrame(rows)
    VB = pd.DataFrame(viab)  # critérios por objetivo ficam em projetos_resumo.json
    VB["objetivo"] = VB["objetivo"].str[0]
    P.to_csv(os.path.join(a.ev, "projetos_caracterizacao.csv"), index=False, encoding="utf-8")
    VB[~VB["classificacao"].isin(["SEM DADOS", "INSUFICIENTE", "DEMANDAS: POUCOS DADOS; HORAS: INDISPONIVEL"])].to_csv(
        os.path.join(a.ev, "projetos_viabilidade_modelos.csv"), index=False, encoding="utf-8")

    # ---------------------------------------------------------------- 2a camada: heterogeneidade
    Bf = B[B["days_fixed"].notna()]
    Bf = Bf[Bf.groupby("project")["issue_id"].transform("size") >= 30]
    R5h = R5[R5.groupby("project")["issue_id"].transform("size") >= 100]
    Rh = R[R.groupby("project_key")["id"].transform("size") >= 10]
    Bh = B[B.groupby("project")["issue_id"].transform("size") >= 100]
    def disp(col, cond):
        x = P.loc[cond, col].dropna()
        return {"projetos": len(x), "p10": r(x.quantile(.1), 2), "mediana": r(x.median(), 2),
                "p90": r(x.quantile(.9), 2), "min": r(x.min(), 2), "max": r(x.max(), 2)}
    het = [
        {"indicador": "log(1+dias ate 1a resolucao Fixed)", "nivel": "bug", "eta2_projeto": eta2(np.log1p(Bf["days_fixed"]), Bf["project"]),
         **disp("dias_fixed_mediana", P["bugs>=2020"] >= 30), "obs": "dispersao da mediana de dias por projeto"},
        {"indicador": "reabertura em 90d", "nivel": "resolucao", "eta2_projeto": eta2(R5h["reopen90"].astype(float), R5h["project"]),
         **disp("reabertos_%", P["bugs>=2020"] >= 100), "obs": "evento raro; eta2 baixo em binario nao implica homogeneidade"},
        {"indicador": "bugs Affects Version por release", "nivel": "release", "eta2_projeto": eta2(Rh["bugs_av"].astype(float), Rh["project_key"]),
         **disp("bugs_affects_por_release_media", P["releases>=2020"] >= 10), "obs": "ver var/media por projeto"},
        {"indicador": "razao var/media de bugs por release", "nivel": "projeto", "eta2_projeto": None,
         **disp("bugs_affects_por_release_var/media", P["releases>=2020"] >= 10),
         "obs": ">1 indica superdispersao (Binomial Negativa); ~1 Poisson"},
        {"indicador": "Affects Version preenchido (% bugs)", "nivel": "bug", "eta2_projeto": eta2(Bh["av_now"].astype(float), Bh["project"]),
         **disp("affects_version_%", P["bugs>=2020"] >= 100), "obs": "pratica de registro varia por projeto"},
        {"indicador": "assignee na abertura (% bugs)", "nivel": "bug", "eta2_projeto": eta2(Bh["asg_t0"].astype(float), Bh["project"]),
         **disp("assignee_na_abertura_%", P["bugs>=2020"] >= 100), "obs": ""},
        {"indicador": "prioridade dominante (% bugs)", "nivel": "projeto", "eta2_projeto": None,
         **disp("prioridade_dominante_%", P["bugs>=2020"] >= 100), "obs": "esquemas de prioridade diferentes por projeto"},
    ]
    H = pd.DataFrame(het)
    H.to_csv(os.path.join(a.ev, "heterogeneidade_entre_projetos.csv"), index=False, encoding="utf-8")

    # ---------------------------------------------------------------- resumo e fichas
    piv = VB.pivot_table(index="projeto", columns=VB["objetivo"].str[0], values="classificacao", aggfunc="first")
    summ = {f"obj{k}": piv[k].value_counts().to_dict() for k in piv.columns}
    rel_sizes = {"obj1_individual_releases_treino": int(VB[(VB["objetivo"].str[0] == "1") & (VB["classificacao"] == "MODELO INDIVIDUAL VIAVEL")]["n_treino"].sum())}
    json.dump({"criterios": CRITERIOS, "split": {"treino": "2020-01-01..2023-12-31", "teste": "2024-01-01..fim-horizonte"},
               "classificacoes": summ, **rel_sizes}, open(os.path.join(a.ev, "projetos_resumo.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    rel = P[(P["bugs>=2020"] >= 200) | (P["releases>=2020"] >= 30) | (P["sprints_reconstruiveis"] >= 10)]
    rel = rel.sort_values("bugs>=2020", ascending=False)
    L = ["# Fichas por projeto — caracterização individual (diagnóstico)\n",
         "Projetos com ≥200 bugs desde 2020, ≥30 releases desde 2020 ou ≥10 sprints reconstruíveis "
         f"({len(rel)} de {len(P)} projetos). Demais projetos: ver `projetos_caracterizacao.csv`.\n",
         "Split comum: treino = T0 em 2020–2023; teste = T0 em 2024 até o fim menos o horizonte. "
         "Critérios em `projetos_resumo.json`. Classificações são de **viabilidade**, não de desempenho.\n"]
    for _, x in rel.iterrows():
        p = x["projeto"]
        v = piv.loc[p] if p in piv.index else {}
        L.append(f"## {p}\n")
        L.append(f"- **Volume:** {x['issues_criadas>=2020']} issues e {x['bugs>=2020']} bugs desde 2020 "
                 f"(2020: {x['bugs_2020']}, 2024: {x['bugs_2024']}, 2025: {x['bugs_2025']}; tendência 24-25/20-21 = {x['tendencia_24-25_vs_20-21']}; "
                 f"último bug {x['ultimo_bug_criado']})."
                 + (" **Série interrompida: nenhum bug nos últimos 12 meses — teste cronológico comprometido.**"
                    if x["serie_interrompida(>=100 bugs; nenhum nos ultimos 12m)"] else ""))
        L.append(f"- **Releases:** {x['releases>=2020']} ({x['releases_por_ano']}/ano; intervalo mediano {x['intervalo_mediano_dias']} d; "
                 f"nomes modulares {x['nomes_modulares_%']}% em {x['prefixos_modulo_distintos']} prefixos; sobreposição 90 d {x['overlap_90d_%']}%). "
                 f"Releases com ≥1 bug Affects Version: {x['releases_com_bug_affects_%']}%; var/média = {x['bugs_affects_por_release_var/media']}; "
                 f"Fix Version até T0: {x['fixversion_ate_T0_%']}%.")
        L.append(f"- **Affects Version:** {x['affects_version_%']}% dos bugs ({x['affects_version_na_abertura_%']}% já na abertura).")
        L.append(f"- **Resolução:** abertos {x['abertos_%']}%, Fixed {x['fixed_%']}%, mediana {x['dias_fixed_mediana']} d "
                 f"(p75 {x['dias_fixed_p75']} d; ≤7 d {x['fixed_<=7d_%']}%); reabertos {x['reabertos_%']}% "
                 f"({x['reabertos_90d_n']} em 90 d).")
        L.append(f"- **Preditores em T0:** prioridade ({x['esquema_prioridade']}; dominante {x['prioridade_dominante_%']}%; "
                 f"alterada {x['prioridade_alterada_%']}%), assignee na abertura {x['assignee_na_abertura_%']}%, "
                 f"componente {x['componente_%']}% (alterado depois {x['componente_alterado_%']}%), labels {x['labels_%']}%, "
                 f"severity {x['severity_%']}%.")
        L.append(f"- **Sprints / horas:** {x['sprints_reconstruiveis']} sprints reconstruíveis ({x['pares_issue_sprint']} pares); "
                 f"{x['worklogs_nao_automaticos']} worklogs não automáticos.")
        L.append(f"- **Viabilidade:** Obj1 {v.get('1', '-')}; Obj2 {v.get('2', '-')}; Obj3 {v.get('3', '-')}; "
                 f"Obj4 {v.get('4', '-')}; Obj5 {v.get('5', '-')}.\n")
    with open(os.path.join(a.ev, "fichas_projetos.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(json.dumps(summ, ensure_ascii=False, indent=1))
    print(H.to_string(index=False))


if __name__ == "__main__":
    main()
