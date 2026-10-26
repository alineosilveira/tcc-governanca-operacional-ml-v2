#!/usr/bin/env python3
"""
Validação de regras de negócio (sem modelagem):
  A. associação explícita release -> bug via Affects Version (IDs de versão);
  B. tempos até primeira resolução (B1), primeiro fechamento (B2) e primeira correção Fixed (B3);
  C. reaberturas, ciclos e estabilidade das resoluções; recorrência via links (separada).

Projeto é a unidade primária: todos os indicadores são calculados por projeto.
Entradas: cache de 01_projetar_base.py (issues_c.csv, changelog_c.csv) e, da base,
versions.jsonl e issue_versions.jsonl (somente leitura). Não lê comments/worklogs.

Saídas (evidencias/):
  regras_releases_bugs_por_projeto.csv
  regras_tempo_correcao_por_projeto.csv
  regras_reaberturas_por_projeto.csv
  e um resumo JSON impresso na saída padrão (citado no relatório).
"""
import argparse
import json
import os

import numpy as np
import pandas as pd

DATA_END = pd.Timestamp("2026-10-25", tz="UTC")
SINCE = pd.Timestamp("2020-01-01", tz="UTC")
WINDOWS = (30, 90, 180)
HORIZONS = (30, 90)
AV_MIN, AV_LOW, MIN_BUGS = 0.5, 0.2, 30
G = {}  # resumo global


def ts(s):
    return pd.to_datetime(s, utc=True, errors="coerce", format="ISO8601")


def pct(a, b):
    return round(100.0 * a / b, 2) if b else None


def med(s):
    s = pd.Series(s).dropna()
    return round(float(s.median()), 2) if len(s) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=os.environ.get("ALINE_JIRA_DATA_DIR"), required=os.environ.get("ALINE_JIRA_DATA_DIR") is None)
    ap.add_argument("--cache", default=os.environ.get("ALINE_CACHE_DIR"), required=os.environ.get("ALINE_CACHE_DIR") is None)
    ap.add_argument("--ev", default=os.environ.get("ALINE_EVIDENCIAS_DIR"), required=os.environ.get("ALINE_EVIDENCIAS_DIR") is None)
    ap.add_argument("--bases", default=os.environ.get("ALINE_BASES_DIR"),
                    help="opcional: grava as bases analíticas linha a linha (uso local; não versionar)")
    a = ap.parse_args()

    I = pd.read_csv(os.path.join(a.cache, "issues_c.csv"), dtype=str, keep_default_na=False,
                    usecols=["issue_id", "key", "project", "issuetype", "status", "status_cat", "resolution",
                             "created", "resolutiondate", "affects_versions", "fix_versions"])
    I["created"] = ts(I["created"])
    I["resolutiondate"] = ts(I["resolutiondate"].replace("", None))
    I["valid"] = I["created"] >= pd.Timestamp("2000-01-01", tz="UTC")
    C = pd.read_csv(os.path.join(a.cache, "changelog_c.csv"), dtype=str, keep_default_na=False,
                    usecols=["issue_id", "ts", "field", "from", "from_str", "to", "to_str"])
    C = C[C["field"].isin(["status", "resolution", "Version", "Project", "Key", "Link"])]
    C["ts"] = ts(C["ts"])
    C = C.sort_values(["issue_id", "ts"], kind="stable")
    bugs_all = I[(I["issuetype"] == "Bug")]
    moved = set(C.loc[C["field"].isin(["Project", "Key"]), "issue_id"])
    # mapa de categoria por nome de status (estado atual; verificado: nenhum nome com >1 categoria)
    catmap = I.groupby("status")["status_cat"].agg(lambda s: s.mode().iat[0]).to_dict()
    G["status_categoria_inconsistente"] = int((I.groupby("status")["status_cat"].nunique() > 1).sum())
    G["status_terminais(done)"] = sorted(k for k, v in catmap.items() if v == "done")

    # ======================================================================== A
    V = pd.read_json(os.path.join(a.base, "versions.jsonl"), lines=True, dtype=False)
    V["id"] = V["id"].astype(str)
    V["rel"] = ts(V["releaseDate"])
    V["released"] = V["released"].fillna(False).astype(bool)
    V = V.set_index("id")
    # vínculos atuais Affects Version (IDs) a partir dos campos do issue
    L = bugs_all.loc[bugs_all["affects_versions"] != "", ["issue_id", "project", "created", "valid",
                                                          "affects_versions", "fix_versions"]].copy()
    L["version_id"] = L["affects_versions"].str.split("|")
    L = L.explode("version_id")
    L["fv_same"] = [v in f.split("|") for v, f in zip(L["version_id"], L["fix_versions"])]
    L["n_av"] = L.groupby("issue_id")["version_id"].transform("nunique")
    L = L.join(V[["project_key", "released", "rel", "name"]], on="version_id")
    # conferência com issue_versions.jsonl (relação 'versions')
    IV = pd.read_json(os.path.join(a.base, "issue_versions.jsonl"), lines=True, dtype=False)
    IV = IV[IV["relation"] == "versions"]
    IV["issue_id"] = IV["issue_id"].astype(str)
    IV["version_id"] = IV["version_id"].astype(str)
    ivb = IV[IV["issue_id"].isin(set(bugs_all["issue_id"]))]
    G["A_pares_affects_issues_c"] = len(L)
    G["A_pares_affects_issue_versions_jsonl"] = len(ivb)
    G["A_pares_coincidentes"] = int(len(L.merge(ivb[["issue_id", "version_id"]], on=["issue_id", "version_id"])))
    G["A_versao_inexistente_no_inventario"] = int(L["project_key"].isna().sum())
    G["A_versao_de_outro_projeto"] = int((L["project_key"].notna() & (L["project_key"] != L["project"])).sum())
    # histórico do vínculo (eventos do campo Version)
    ve = C[C["field"] == "Version"]
    ev = pd.concat([ve.loc[ve["to"] != "", ["issue_id", "ts", "to"]].rename(columns={"to": "version_id"}).assign(op="add"),
                    ve.loc[ve["from"] != "", ["issue_id", "ts", "from"]].rename(columns={"from": "version_id"}).assign(op="rem")])
    ev = ev.sort_values(["issue_id", "version_id", "ts"])
    last = ev.groupby(["issue_id", "version_id"]).agg(last_op=("op", "last"), last_ts=("ts", "last"),
                                                      n_add=("op", lambda s: (s == "add").sum()))
    L = L.join(last, on=["issue_id", "version_id"])
    L["status_vinculo"] = np.select(
        [L["issue_id"].isin(moved), L["last_op"].isna(), L["last_op"] == "add"],
        ["indeterminado (issue movida)", "na criacao (inferido: sem evento)", "inclusao datada"],
        "contraditorio (ultimo evento = remocao)")
    L["t_conhecido"] = np.where(L["status_vinculo"] == "na criacao (inferido: sem evento)", L["created"],
                                np.where(L["status_vinculo"] == "inclusao datada", L["last_ts"], pd.NaT))
    L["t_conhecido"] = pd.to_datetime(L["t_conhecido"], utc=True)
    G["A_status_vinculo"] = L["status_vinculo"].value_counts().to_dict()
    G["A_vinculos_readicionados(>1 inclusao)"] = int((L["n_add"] > 1).sum())
    cur = set(zip(L["issue_id"], L["version_id"]))
    rem = last[last["last_op"] == "rem"].reset_index()
    rem = rem[[(i, v) not in cur for i, v in zip(rem["issue_id"], rem["version_id"])]]
    rem = rem.join(I.set_index("issue_id")["project"], on="issue_id")
    G["A_vinculos_removidos(existiram e nao existem hoje)"] = len(rem)
    # releases do período e classificação temporal dos bugs vinculados
    R = V[V["released"] & V["rel"].notna() & (V["rel"] >= SINCE) & (V["rel"] <= DATA_END)].reset_index()
    G["A_releases_T0>=2020"] = len(R)
    G["A_versoes_released_sem_data(todas)"] = int((V["released"] & V["rel"].isna()).sum())
    LR = L[L["version_id"].isin(set(R["id"]))].copy()
    cdate = LR["created"].dt.tz_convert(None).dt.normalize()
    rdate = LR["rel"].dt.tz_convert(None).dt.normalize()
    LR["classe"] = np.select([~LR["valid"] | LR["created"].isna(), cdate < rdate, cdate == rdate],
                             ["D data insuficiente", "A antes", "B mesmo dia"], "C depois")
    G["A_pares_bug_release"] = len(LR)
    G["A_bugs_unicos_vinculados_a_releases"] = int(LR["issue_id"].nunique())
    G["A_classes_pares"] = LR["classe"].value_counts().to_dict()
    G["A_bugs_vinculados_a_>1_release_do_periodo_%"] = pct(
        (LR.groupby("issue_id")["version_id"].nunique() > 1).sum(), LR["issue_id"].nunique())
    # cobertura Affects Version por projeto (bugs criados >= 2020)
    b20 = bugs_all[bugs_all["created"] >= SINCE]
    cov = b20.assign(av=b20["affects_versions"] != "").groupby("project")["av"].agg(["size", "mean"])
    R = R.join(cov.rename(columns={"size": "bugs_proj", "mean": "av_cov"}), on="project_key")
    for w in WINDOWS:
        endw = LR["rel"] + pd.Timedelta(days=w + 1)          # fim do dia T0+w
        inw = (LR["classe"] == "C depois") & (LR["created"] < endw)
        LR[f"pos_{w}"] = inw
        LR[f"pos_{w}_conhecido"] = inw & (LR["t_conhecido"] < endw)
        cnt = LR[inw].groupby("version_id")["issue_id"].nunique()
        R[f"bugs_pos_{w}d"] = R["id"].map(cnt).fillna(0).astype(int)
        R[f"bugs_pos_{w}d_conhecidos_na_janela"] = R["id"].map(
            LR[LR[f"pos_{w}_conhecido"]].groupby("version_id")["issue_id"].nunique()).fillna(0).astype(int)
        full = R["rel"] + pd.Timedelta(days=w) <= DATA_END
        R[f"classe_{w}d"] = np.select(
            [~full, R["bugs_proj"].fillna(0) < MIN_BUGS, R["av_cov"].fillna(0) < AV_MIN, R[f"bugs_pos_{w}d"] == 0],
            ["acompanhamento incompleto", "dados insuficientes (<30 bugs no projeto)",
             "projeto com baixa cobertura AV (<50%)", "zero vinculado (cobertura adequada)"], "com bugs vinculados")
        G[f"A_releases_classe_{w}d"] = R[f"classe_{w}d"].value_counts().to_dict()
        sub = R[R[f"classe_{w}d"].isin(["zero vinculado (cobertura adequada)", "com bugs vinculados"])]
        G[f"A_{w}d_bugs_pos_hoje_vs_conhecidos_na_janela"] = [int(sub[f"bugs_pos_{w}d"].sum()),
                                                              int(sub[f"bugs_pos_{w}d_conhecidos_na_janela"].sum())]
    R["n_vinculados"] = R["id"].map(LR.groupby("version_id")["issue_id"].nunique()).fillna(0).astype(int)
    # por projeto
    rows = []
    gL, gLR, gR = dict(tuple(L.groupby("project"))), dict(tuple(LR.groupby("project_key"))), dict(tuple(R.groupby("project_key")))
    rem_p = rem.groupby("project").size()
    for p in sorted(set(cov.index) | set(gR)):
        l, lr, r = gL.get(p, L.iloc[0:0]), gLR.get(p, LR.iloc[0:0]), gR.get(p, R.iloc[0:0])
        cv = cov["mean"].get(p, np.nan)
        nb = int(cov["size"].get(p, 0))
        det = l["status_vinculo"].isin(["na criacao (inferido: sem evento)", "inclusao datada"]).mean() if len(l) else np.nan
        if len(r) == 0:
            cls = "sem releases no periodo"
        elif nb < MIN_BUGS:
            cls = "dados insuficientes (<30 bugs)"
        elif cv < AV_LOW:
            cls = "baixa cobertura AV (<20%)"
        elif cv < AV_MIN:
            cls = "cobertura intermediaria AV (20-50%)"
        else:
            cls = "associacao verificavel (AV>=50%)"
        row = {"projeto": p, "bugs>=2020": nb, "affects_version_%": round(100 * cv, 1) if nb else None,
               "classificacao_associacao": cls, "releases_T0>=2020": len(r),
               "releases_com_>=1_bug_vinculado": int((r["n_vinculados"] > 0).sum()),
               "pares_bug_release": len(lr), "bugs_unicos_vinculados": int(lr["issue_id"].nunique()),
               "A_antes_%": pct((lr["classe"] == "A antes").sum(), len(lr)),
               "B_mesmo_dia_%": pct((lr["classe"] == "B mesmo dia").sum(), len(lr)),
               "C_depois_%": pct((lr["classe"] == "C depois").sum(), len(lr)),
               "D_data_insuficiente": int((lr["classe"] == "D data insuficiente").sum()),
               "bugs_com_>1_affects_version_%": pct((l.drop_duplicates("issue_id")["n_av"] > 1).sum(), l["issue_id"].nunique()),
               "vinculos_momento_determinado_%": round(100 * det, 1) if len(l) else None,
               "vinculos_inclusao_datada_%": pct((l["status_vinculo"] == "inclusao datada").sum(), len(l)),
               "vinculos_indeterminados": int(l["status_vinculo"].str.startswith(("indeterminado", "contraditorio")).sum()),
               "vinculos_removidos": int(rem_p.get(p, 0)),
               "affects=fix_mesma_versao_%": pct(l["fv_same"].sum(), len(l)),
               "vinculos_a_versao_nao_publicada_ou_sem_data_%": pct((~l["released"].fillna(False).astype(bool) | l["rel"].isna()).sum(), len(l)),
               "vinculos_a_versao_de_outro_projeto": int((l["project_key"].notna() & (l["project_key"] != p)).sum())}
        for w in WINDOWS:
            el = r[r[f"classe_{w}d"].isin(["zero vinculado (cobertura adequada)", "com bugs vinculados"])]
            row[f"releases_elegiveis_{w}d"] = len(el)
            row[f"zero_vinculado_{w}d"] = int((el[f"classe_{w}d"] == "zero vinculado (cobertura adequada)").sum())
            row[f"incompletas_{w}d"] = int((r[f"classe_{w}d"] == "acompanhamento incompleto").sum())
            row[f"mediana_bugs_pos_{w}d"] = med(el[f"bugs_pos_{w}d"])
            row[f"bugs_pos_{w}d_conhecidos_na_janela_%"] = pct(el[f"bugs_pos_{w}d_conhecidos_na_janela"].sum(), el[f"bugs_pos_{w}d"].sum())
        rows.append(row)
    PA = pd.DataFrame(rows)
    PA.to_csv(os.path.join(a.ev, "regras_releases_bugs_por_projeto.csv"), index=False, encoding="utf-8")
    G["A_projetos_por_classe"] = PA["classificacao_associacao"].value_counts().to_dict()
    ver = PA[PA["classificacao_associacao"] == "associacao verificavel (AV>=50%)"]
    G["A_projetos_verificaveis_com>=10_releases"] = int((ver["releases_T0>=2020"] >= 10).sum())

    # ======================================================================== B
    B = bugs_all[bugs_all["valid"] & (bugs_all["created"] >= SINCE)].copy()
    bid = set(B["issue_id"])
    st = C[(C["field"] == "status") & C["issue_id"].isin(bid)].copy()
    st["cf"] = st["from_str"].map(catmap).fillna("desconhecido")
    st["ct"] = st["to_str"].map(catmap).fillna("desconhecido")
    G["B_transicoes_com_status_sem_categoria"] = int(((st["cf"] == "desconhecido") | (st["ct"] == "desconhecido")).sum())
    rs = C[(C["field"] == "resolution") & C["issue_id"].isin(bid)]
    first_res_ev = rs[rs["to_str"] != ""].groupby("issue_id")["ts"].min()
    first_fixed_ev = rs[rs["to_str"] == "Fixed"].groupby("issue_id")["ts"].min()
    done_entry = st[(st["ct"] == "done") & (st["cf"] != "done")]
    first_close = done_entry.groupby("issue_id")["ts"].min()
    B["t_b1"] = B["issue_id"].map(first_res_ev)
    B["t_b2"] = B["issue_id"].map(first_close)
    B["t_b3"] = B["issue_id"].map(first_fixed_ev)
    B["cur_done"] = B["status_cat"] == "done"
    B["has_rd"] = B["resolutiondate"].notna()
    B["has_res_ev"] = B["issue_id"].isin(set(rs["issue_id"]))
    B["has_st_ev"] = B["issue_id"].isin(set(st["issue_id"]))
    # status das medidas
    B["b1_status"] = np.select([B["t_b1"].notna(), B["has_rd"], B["resolution"] == ""],
                               ["datado por evento", "so resolutiondate (sem evento) - indeterminado", "sem resolucao (aberto/censurado)"],
                               "contraditorio")
    B["b2_status"] = np.select([B["t_b2"].notna(), B["cur_done"], ~B["cur_done"]],
                               ["datado por transicao", "terminal sem transicao datada - indeterminado", "nao terminal (aberto/censurado)"], "")
    B["b3_status"] = np.select([B["t_b3"].notna(), B["resolution"] == "Fixed", B["resolution"] == ""],
                               ["Fixed datado por evento", "Fixed sem evento - indeterminado", "sem resolucao (aberto/censurado)"],
                               "encerrado sem Fixed (nao corrigido)")
    for k in ("b1", "b2", "b3"):
        B[f"d_{k}"] = (B[f"t_{k}"] - B["created"]).dt.total_seconds() / 86400
    B["rd_differs_b1"] = B["t_b1"].notna() & B["has_rd"] & ((B["resolutiondate"] - B["t_b1"]).abs() > pd.Timedelta(minutes=1))
    B["recup_hist"] = ~B["has_rd"] & B["t_b2"].notna()             # sem resolutiondate, mas fechamento datado
    B["contr_done_sem_res"] = B["cur_done"] & (B["resolution"] == "")
    B["contr_res_nao_done"] = ~B["cur_done"] & (B["resolution"] != "")
    B["contr_rd_antes_criacao"] = B["has_rd"] & (B["resolutiondate"] < B["created"])
    B["contr_res_sem_fechamento"] = B["t_b1"].notna() & B["t_b2"].isna()
    G["B_bugs"] = len(B)
    for k in ("b1_status", "b2_status", "b3_status"):
        G[f"B_{k}"] = B[k].value_counts().to_dict()
    G["B_mensuravel_so_resolutiondate"] = int(B["has_rd"].sum())
    G["B_mensuravel_resolutiondate_ou_fechamento_datado"] = int((B["has_rd"] | B["t_b2"].notna()).sum())
    G["B_recuperados_pelo_historico(sem resolutiondate, com fechamento)"] = int(B["recup_hist"].sum())
    G["B_resolutiondate_difere_da_primeira_resolucao"] = int(B["rd_differs_b1"].sum())
    G["B_contradicoes"] = {k: int(B[k].sum()) for k in ("contr_done_sem_res", "contr_res_nao_done",
                                                        "contr_rd_antes_criacao", "contr_res_sem_fechamento")}
    for h in HORIZONS:
        ok = B["created"] + pd.Timedelta(days=h) <= DATA_END
        B[f"h{h}_elig"] = ok
        B[f"h{h}_b3"] = np.select([~ok, B["b3_status"] == "Fixed sem evento - indeterminado", B["d_b3"] <= h],
                                  ["acompanhamento incompleto", "indeterminado", f"corrigido (Fixed) ate {h}d"],
                                  f"nao corrigido em {h}d")
        G[f"B_horizonte_{h}d_b3"] = B[f"h{h}_b3"].value_counts().to_dict()
    # workflow por projeto
    rc = st[(st["from_str"] == "Resolved") & (st["to_str"] == "Closed")]["issue_id"]
    B["resolved_to_closed"] = B["issue_id"].isin(set(rc))
    used = pd.concat([st[["issue_id", "from_str"]].rename(columns={"from_str": "s"}),
                      st[["issue_id", "to_str"]].rename(columns={"to_str": "s"})]).join(B.set_index("issue_id")["project"], on="issue_id")
    rows = []
    for p, b in B.groupby("project"):
        u = used[used["project"] == p]["s"]
        ustat = sorted(set(u) - {""})
        row = {"projeto": p, "bugs>=2020": len(b),
               "status_usados": len(ustat), "status_terminais_usados": "|".join(s for s in ustat if catmap.get(s) == "done"),
               "status_personalizados": "|".join(s for s in ustat if s not in {"Open", "In Progress", "Resolved", "Closed", "Reopened", "Done", "To Do"}),
               "fluxo_Resolved->Closed_%": pct(b["resolved_to_closed"].sum(), len(b)),
               "usa_status_Reopened": bool("Reopened" in ustat),
               "abertos_%": pct((b["resolution"] == "").sum(), len(b)),
               "B1_datado_%": pct(b["t_b1"].notna().sum(), len(b)),
               "B1_indeterminado_%": pct((b["b1_status"].str.startswith("so resolutiondate")).sum(), len(b)),
               "B2_datado_%": pct(b["t_b2"].notna().sum(), len(b)),
               "B2_indeterminado_%": pct((b["b2_status"].str.startswith("terminal sem")).sum(), len(b)),
               "B3_fixed_datado_%": pct(b["t_b3"].notna().sum(), len(b)),
               "B3_indeterminado_%": pct((b["b3_status"] == "Fixed sem evento - indeterminado").sum(), len(b)),
               "encerrado_sem_fixed_%": pct((b["b3_status"] == "encerrado sem Fixed (nao corrigido)").sum(), len(b)),
               "mensuravel_resolutiondate": int(b["has_rd"].sum()),
               "recuperados_pelo_historico": int(b["recup_hist"].sum()),
               "resolutiondate_difere_primeira_resolucao": int(b["rd_differs_b1"].sum()),
               "contradicoes": int(b[["contr_done_sem_res", "contr_res_nao_done", "contr_rd_antes_criacao"]].any(axis=1).sum()),
               "mediana_dias_B1": med(b["d_b1"]), "mediana_dias_B2": med(b["d_b2"]), "mediana_dias_B3": med(b["d_b3"]),
               "B2_menos_B1_mediana_dias": med((b["t_b2"] - b["t_b1"]).dt.total_seconds() / 86400)}
        for h in HORIZONS:
            e = b[b[f"h{h}_elig"]]
            row[f"elegiveis_{h}d"] = len(e)
            row[f"fixed_ate_{h}d_%"] = pct((e[f"h{h}_b3"] == f"corrigido (Fixed) ate {h}d").sum(), len(e))
            row[f"nao_corrigido_{h}d_%"] = pct((e[f"h{h}_b3"] == f"nao corrigido em {h}d").sum(), len(e))
            row[f"indeterminado_{h}d"] = int((e[f"h{h}_b3"] == "indeterminado").sum())
        rows.append(row)
    PB = pd.DataFrame(rows).sort_values("bugs>=2020", ascending=False)
    PB.to_csv(os.path.join(a.ev, "regras_tempo_correcao_por_projeto.csv"), index=False, encoding="utf-8")
    G["B_status_personalizados_distintos"] = sorted(set("|".join(PB["status_personalizados"]).split("|")) - {""})
    G["B_mediana_dias_global(B1,B2,B3)"] = [med(B["d_b1"]), med(B["d_b2"]), med(B["d_b3"])]

    # ======================================================================== C
    reo = st[(st["cf"] == "done") & (st["ct"].isin(["new", "indeterminate"]))][["issue_id", "ts", "from_str", "to_str"]]
    rclear = rs[(rs["from_str"] != "") & (rs["to_str"] == "")][["issue_id", "ts"]]
    G["C_reaberturas_por_status"] = len(reo)
    G["C_reaberturas_por_limpeza_de_resolution"] = len(rclear)
    G["C_bugs_reabertos_status"] = int(reo["issue_id"].nunique())
    G["C_bugs_reabertos_resolution"] = int(rclear["issue_id"].nunique())
    G["C_bugs_reabertos_ambos_criterios"] = len(set(reo["issue_id"]) & set(rclear["issue_id"]))
    G["C_transicoes_Resolved->Closed_(nao_reabertura)"] = int(((st["from_str"] == "Resolved") & (st["to_str"] == "Closed")).sum())
    G["C_reaberturas_destino"] = reo["to_str"].value_counts().head(8).to_dict()
    # tempo desde a entrada em estado terminal imediatamente anterior
    de = done_entry[["issue_id", "ts"]].rename(columns={"ts": "t_done"}).sort_values("t_done")
    rr = pd.merge_asof(reo.sort_values("ts"), de, left_on="ts", right_on="t_done", by="issue_id", direction="backward")
    rr["horas"] = (rr["ts"] - rr["t_done"]).dt.total_seconds() / 3600
    bins = [-1e-9, 5 / 60, 1, 24, 24 * 7, 24 * 30, 24 * 90, 1e12]
    labels = ["<=5min", "5-60min", "1-24h", "1-7d", "7-30d", "30-90d", ">90d"]
    rr["faixa"] = pd.cut(rr["horas"], bins, labels=labels)
    G["C_tempo_ate_reabertura_faixas"] = rr["faixa"].value_counts().reindex(labels).fillna(0).astype(int).to_dict()
    G["C_reaberturas_sem_entrada_terminal_datada"] = int(rr["t_done"].isna().sum())
    nreo = reo.groupby("issue_id").size()
    ncyc = done_entry.groupby("issue_id").size()
    last_close = done_entry.groupby("issue_id")["ts"].max()
    B["n_reab"] = B["issue_id"].map(nreo).fillna(0).astype(int)
    B["n_ciclos"] = B["issue_id"].map(ncyc).fillna(0).astype(int)
    B["t_last_close"] = B["issue_id"].map(last_close)
    B["dur_adic_dias"] = np.where((B["n_reab"] > 0) & B["cur_done"],
                                  (B["t_last_close"] - B["t_b2"]).dt.total_seconds() / 86400, np.nan)
    B["dur_total_dias"] = np.where(B["cur_done"] & B["t_last_close"].notna(),
                                   (B["t_last_close"] - B["created"]).dt.total_seconds() / 86400, np.nan)
    G["C_distribuicao_reaberturas_por_bug"] = B["n_reab"].clip(upper=4).value_counts().sort_index().to_dict()
    G["C_ciclos_reconstruiveis(bugs com >=1 fechamento datado)"] = int((B["n_ciclos"] > 0).sum())
    G["C_mediana_duracao_adicional_apos_reabertura_dias"] = med(B["dur_adic_dias"])
    # estabilidade: sem reabertura em w dias após a primeira resolução válida (B2) e após Fixed (B3)
    reo_t = reo[["issue_id", "ts"]]
    for base, col in (("fechamento", "t_b2"), ("fixed", "t_b3")):
        t0 = B[["issue_id", "project", col]].dropna()
        m = reo_t.merge(t0, on="issue_id")
        m = m[m["ts"] > m[col]]
        first_after = m.groupby("issue_id")["ts"].min()
        t0["t_reab"] = t0["issue_id"].map(first_after)
        for w in HORIZONS:
            full = t0[col] + pd.Timedelta(days=w) <= DATA_END
            reab = t0["t_reab"].notna() & (t0["t_reab"] <= t0[col] + pd.Timedelta(days=w))
            t0[f"est_{w}"] = np.select([reab, ~full], ["reaberta na janela", "acompanhamento insuficiente"], "estavel")
            B[f"est_{base}_{w}"] = B["issue_id"].map(t0.set_index("issue_id")[f"est_{w}"])
            G[f"C_estabilidade_{base}_{w}d"] = t0[f"est_{w}"].value_counts().to_dict()
    # recorrência via links (separada de reabertura)
    lk = C[(C["field"] == "Link") & C["issue_id"].isin(bid) & (C["to_str"] != "")][["issue_id", "ts", "to", "to_str"]]
    k2 = I.set_index("key")
    lk = lk.assign(tipo=np.select([lk["to_str"].str.startswith("This issue duplicates"),
                                   lk["to_str"].str.startswith("This issue is broken by")],
                                  ["duplica issue anterior", "regressao (is broken by)"], "outro"))
    lk = lk[lk["tipo"] != "outro"].drop_duplicates(["issue_id", "to", "tipo"])
    lk["alvo_res"] = lk["to"].map(k2["resolutiondate"])
    lk["alvo_criado"] = lk["to"].map(k2["created"])
    lk["created"] = lk["issue_id"].map(B.set_index("issue_id")["created"])
    lk["alvo_na_base"] = lk["alvo_criado"].notna()
    lk["alvo_resolvido_antes"] = lk["alvo_res"].notna() & (lk["alvo_res"] < lk["created"])
    G["C_links_recorrencia"] = {t: {"links": int((lk["tipo"] == t).sum()),
                                    "alvo_na_base": int(((lk["tipo"] == t) & lk["alvo_na_base"]).sum()),
                                    "alvo_resolvido_antes_da_nova_issue": int(((lk["tipo"] == t) & lk["alvo_resolvido_antes"]).sum())}
                                for t in ("duplica issue anterior", "regressao (is broken by)")}
    lkp = lk.join(B.set_index("issue_id")["project"], on="issue_id")
    rows = []
    gr = rr.join(B.set_index("issue_id")["project"], on="issue_id")
    for p, b in B.groupby("project"):
        r_ = gr[gr["project"] == p]
        l_ = lkp[lkp["project"] == p]
        res_ever = b["t_b2"].notna() | (b["n_reab"] > 0)
        row = {"projeto": p, "bugs>=2020": len(b), "bugs_com_fechamento_datado": int(b["t_b2"].notna().sum()),
               "bugs_reabertos": int((b["n_reab"] > 0).sum()),
               "reabertos_%_dos_fechados": pct((b["n_reab"] > 0).sum(), res_ever.sum()),
               "reabertos_>1_vez": int((b["n_reab"] > 1).sum()),
               "reaberturas_por_bug_reaberto_media": round(float(b.loc[b["n_reab"] > 0, "n_reab"].mean()), 2) if (b["n_reab"] > 0).any() else None,
               "reabertura_<=5min_%": pct((r_["faixa"] == "<=5min").sum(), len(r_)),
               "reabertura_<=24h_%": pct(r_["faixa"].isin(["<=5min", "5-60min", "1-24h"]).sum(), len(r_)),
               "mediana_horas_ate_reabertura": med(r_["horas"]),
               "ciclos_max": int(b["n_ciclos"].max()),
               "mediana_duracao_adicional_dias": med(b["dur_adic_dias"]),
               "mediana_duracao_total_ate_ultimo_fechamento_dias": med(b["dur_total_dias"])}
        for base in ("fechamento", "fixed"):
            for w in HORIZONS:
                s = b[f"est_{base}_{w}"].dropna()
                ok = s[s != "acompanhamento insuficiente"]
                row[f"estavel_{base}_{w}d_%"] = pct((ok == "estavel").sum(), len(ok))
                row[f"elegiveis_{base}_{w}d"] = len(ok)
                row[f"insuficientes_{base}_{w}d"] = int((s == "acompanhamento insuficiente").sum())
        row["links_duplica_anterior"] = int((l_["tipo"] == "duplica issue anterior").sum())
        row["duplica_alvo_resolvido_antes"] = int(((l_["tipo"] == "duplica issue anterior") & l_["alvo_resolvido_antes"]).sum())
        row["links_regressao"] = int((l_["tipo"] == "regressao (is broken by)").sum())
        rows.append(row)
    PC = pd.DataFrame(rows).sort_values("bugs>=2020", ascending=False)
    PC.to_csv(os.path.join(a.ev, "regras_reaberturas_por_projeto.csv"), index=False, encoding="utf-8")
    G["C_projetos>=200_bugs_estabilidade_fechamento_90d_mediana_%"] = med(PC.loc[PC["bugs>=2020"] >= 200, "estavel_fechamento_90d_%"])
    G["C_projetos>=200_bugs_estabilidade_p10_p90"] = [round(float(PC.loc[PC["bugs>=2020"] >= 200, "estavel_fechamento_90d_%"].quantile(q)), 2) for q in (.1, .9)]
    if a.bases:  # bases analíticas derivadas exatamente das regras acima (sem reimplementação)
        os.makedirs(a.bases, exist_ok=True)
        rcols = ["id", "project_key", "name", "rel", "released", "bugs_proj", "av_cov", "n_vinculados"] +             [c for w in WINDOWS for c in (f"bugs_pos_{w}d", f"bugs_pos_{w}d_conhecidos_na_janela", f"classe_{w}d")]
        R[rcols].rename(columns={"id": "version_id", "rel": "release_date"}).to_csv(
            os.path.join(a.bases, "base_releases.csv"), index=False, encoding="utf-8")
        lcols = ["issue_id", "version_id", "project", "created", "rel", "classe", "status_vinculo", "t_conhecido",
                 "n_av", "fv_same"] + [f"pos_{w}" for w in WINDOWS] + [f"pos_{w}_conhecido" for w in WINDOWS]
        LR[lcols].rename(columns={"rel": "release_date"}).to_csv(
            os.path.join(a.bases, "base_bug_release.csv"), index=False, encoding="utf-8")
        bcols = ["issue_id", "key", "project", "created", "status", "status_cat", "resolution", "has_rd",
                 "t_b1", "t_b2", "t_b3", "d_b1", "d_b2", "d_b3", "b1_status", "b2_status", "b3_status",
                 "rd_differs_b1", "recup_hist", "contr_done_sem_res", "contr_res_nao_done", "h30_b3", "h90_b3",
                 "n_reab", "n_ciclos", "t_last_close", "dur_adic_dias", "dur_total_dias",
                 "est_fechamento_30", "est_fechamento_90", "est_fixed_30", "est_fixed_90", "resolved_to_closed"]
        B[bcols].to_csv(os.path.join(a.bases, "base_bugs_ciclos.csv"), index=False, encoding="utf-8")
        rr.join(B.set_index("issue_id")["project"], on="issue_id")[
            ["issue_id", "project", "ts", "from_str", "to_str", "t_done", "horas", "faixa"]].rename(
            columns={"ts": "t_reabertura", "t_done": "t_fechamento_anterior"}).to_csv(
            os.path.join(a.bases, "base_reaberturas.csv"), index=False, encoding="utf-8")
    print(json.dumps(G, ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    main()
