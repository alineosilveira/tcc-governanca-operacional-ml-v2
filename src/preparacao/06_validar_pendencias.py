#!/usr/bin/env python3
"""
Validação das duas pendências metodológicas (somente verificação, sem alterar indicadores oficiais):

A. Affects Version: reconstrução reversa do campo Version a partir do estado atual,
   teste de completude pela cadeia de status, níveis de evidência por vínculo
   (COMPROVADO / RECONSTRUIDO / INFERIDO / INDETERMINADO), revisão da afirmação
   "99% conhecidos até o fim da janela de 90 dias" e amostra estratificada (seed 20261025).
B. Reaberturas: matriz de concordância status x Resolution (bugs distintos, mesmo universo),
   investigação de todas as divergências e análise das reaberturas em até 5 minutos.

Entradas: cache de 01_projetar_base.py (issues_c.csv, changelog_c.csv) e versions.jsonl (base, leitura).
Saídas: evidencias/pendencia_affects_version.csv, pendencia_reaberturas_concordancia.csv,
        pendencia_reaberturas_divergencias.csv; resumo JSON na saída padrão.
"""
import argparse
import json
import os

import numpy as np
import pandas as pd

DATA_END = pd.Timestamp("2026-10-25", tz="UTC")
SINCE = pd.Timestamp("2020-01-01", tz="UTC")
SEED = 20261025
SAMPLE_PROJECTS = ["CAMEL", "GROOVY", "FLINK", "HBASE", "SLING"]   # + 1 projeto de baixa cobertura
QUICK = pd.Timedelta(minutes=5)
G = {}


def ts(s):
    return pd.to_datetime(s, utc=True, errors="coerce", format="ISO8601")


def pct(a, b):
    return round(100.0 * a / b, 2) if b else None


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
                             "created", "affects_versions", "changelog_total"])
    I["created"] = ts(I["created"])
    I["changelog_total"] = pd.to_numeric(I["changelog_total"], errors="coerce").fillna(0).astype(int)
    catmap = I.groupby("status")["status_cat"].agg(lambda s: s.mode().iat[0]).to_dict()
    bugs = I[I["issuetype"] == "Bug"]
    bid_all = set(bugs["issue_id"])
    C = pd.read_csv(os.path.join(a.cache, "changelog_c.csv"), dtype=str, keep_default_na=False,
                    usecols=["issue_id", "history_id", "ts", "field", "from", "from_str", "to", "to_str"])
    C = C[C["issue_id"].isin(bid_all)]
    C["ts"] = ts(C["ts"])
    C["hid"] = pd.to_numeric(C["history_id"], errors="coerce")
    C = C.sort_values(["issue_id", "ts", "hid"], kind="stable")
    moved = set(C.loc[C["field"].isin(["Project", "Key"]), "issue_id"])

    # ============================================================== A. Affects Version
    # A.1 teste de completude independente: cadeia de status (from de cada transição = to da anterior;
    #     último to = status atual). Quebras indicam histórico incompleto ou renomeação de status.
    st = C[C["field"] == "status"][["issue_id", "ts", "from_str", "to_str"]]
    prev_to = st.groupby("issue_id")["to_str"].shift()
    st_break = st[prev_to.notna() & (st["from_str"] != prev_to)].groupby("issue_id").size()
    last_to = st.groupby("issue_id")["to_str"].last()
    cur_status = bugs.set_index("issue_id")["status"]
    end_break = (last_to != cur_status.reindex(last_to.index))
    chain_bad = set(st_break.index) | set(end_break[end_break].index)
    G["A_cadeia_status_bugs_com_transicoes"] = int(st["issue_id"].nunique())
    G["A_cadeia_status_quebrada"] = len(chain_bad)
    # A.2 reconstrução reversa do campo Version (todas as issues Bug com vínculo atual ou eventos)
    cur = {i: set(v.split("|")) for i, v in zip(bugs["issue_id"], bugs["affects_versions"]) if v}
    ve = C[C["field"] == "Version"][["issue_id", "ts", "from", "to"]]
    vids = set(pd.read_json(os.path.join(a.base, "versions.jsonl"), lines=True, dtype=False)["id"].astype(str))
    incons, initial, first_add = {}, {}, {}
    kinds = {"inclusao de versao ausente hoje (saiu sem evento)": 0, "remocao de versao presente hoje (entrou sem evento)": 0,
             "inconsistencias com versao inexistente no inventario": 0}
    for iid, g in ve.groupby("issue_id", sort=False):
        s = set(cur.get(iid, set()))
        bad = 0
        for f, t, tstamp in zip(g["from"].values[::-1], g["to"].values[::-1], g["ts"].values[::-1]):
            if t:                       # desfaz inclusão: a versão deve estar presente
                if t not in s:
                    bad += 1
                    kinds["inclusao de versao ausente hoje (saiu sem evento)"] += 1
                    kinds["inconsistencias com versao inexistente no inventario"] += t not in vids
                s.discard(t)
                first_add[(iid, t)] = tstamp     # ao final do laço reverso, fica a inclusão mais antiga
            if f:                       # desfaz remoção: a versão deve estar ausente
                if f in s:
                    bad += 1
                    kinds["remocao de versao presente hoje (entrou sem evento)"] += 1
                    kinds["inconsistencias com versao inexistente no inventario"] += f not in vids
                s.add(f)
        incons[iid] = bad
        initial[iid] = s
    G["A_issues_com_eventos_Version"] = len(incons)
    G["A_issues_reconstrucao_inconsistente"] = int(sum(1 for v in incons.values() if v))
    G["A_tipos_inconsistencia"] = kinds
    # A.3 níveis de evidência por vínculo atual
    L = bugs.loc[bugs["affects_versions"] != "", ["issue_id", "key", "project", "created", "affects_versions",
                                                   "changelog_total"]].copy()
    L["version_id"] = L["affects_versions"].str.split("|")
    L = L.explode("version_id")
    L["n_av"] = L.groupby("issue_id")["version_id"].transform("nunique")
    evc = ve.assign(vid=np.where(ve["to"] != "", ve["to"], ve["from"])).groupby(["issue_id", "vid"]).agg(
        n_add=("to", lambda s: (s != "").sum()), n_rem=("from", lambda s: (s != "").sum()))
    L = L.join(evc, on=["issue_id", "version_id"])
    L[["n_add", "n_rem"]] = L[["n_add", "n_rem"]].fillna(0).astype(int)
    L["inc_issue"] = L["issue_id"].map(incons).fillna(0).astype(int)
    L["in_initial"] = [v in initial[i] if i in initial else True for i, v in zip(L["issue_id"], L["version_id"])]
    L["t_add"] = [first_add.get((i, v)) for i, v in zip(L["issue_id"], L["version_id"])]
    L["t_add"] = pd.to_datetime(L["t_add"], utc=True)
    L["chain_ok"] = ~L["issue_id"].isin(chain_bad)
    L["tem_historico"] = L["changelog_total"] > 0
    L["nivel"] = np.select(
        [L["issue_id"].isin(moved) | (L["inc_issue"] > 0),
         (L["n_add"] > 0) & ~L["in_initial"],
         ~L["in_initial"],
         L["in_initial"] & L["tem_historico"] & L["chain_ok"],
         L["in_initial"]],
        ["INDETERMINADO", "COMPROVADO (inclusao por evento)", "INDETERMINADO",
         "RECONSTRUIDO (reverso consistente; premissa: historico completo)",
         "INFERIDO (sem historico corroborante)"], "INDETERMINADO")
    L["motivo_indeterminado"] = np.select(
        [L["issue_id"].isin(moved), L["inc_issue"] > 0],
        ["issue movida de projeto", "reconstrucao reversa inconsistente"], "")
    L.loc[L["nivel"].str.startswith("INFERIDO") & ~L["tem_historico"], "motivo_indeterminado"] = "issue sem nenhum evento de changelog"
    L.loc[L["nivel"].str.startswith("INFERIDO") & L["tem_historico"] & ~L["chain_ok"], "motivo_indeterminado"] = "cadeia de status quebrada"
    G["A_niveis_vinculos"] = L["nivel"].value_counts().to_dict()
    G["A_vinculos_removidos_e_reincluidos"] = int(((L["n_rem"] > 0) & (L["n_add"] > 0)).sum())
    G["A_vinculos_presentes_na_criacao_e_depois_removidos_e_reincluidos"] = int(((L["n_rem"] > 0) & L["in_initial"]).sum())

    # A.4 revisão dos "99%": pares classe C na janela de 90 d em releases elegíveis (mesma regra do script 05)
    V = pd.read_json(os.path.join(a.base, "versions.jsonl"), lines=True, dtype=False)
    V["id"] = V["id"].astype(str)
    V["rel"] = ts(V["releaseDate"])
    V["released"] = V["released"].fillna(False).astype(bool)
    R = V[V["released"] & V["rel"].notna() & (V["rel"] >= SINCE) & (V["rel"] <= DATA_END)].set_index("id")
    b20 = bugs[bugs["created"] >= SINCE]
    cov = b20.assign(av=b20["affects_versions"] != "").groupby("project")["av"].agg(["size", "mean"])
    LR = L[L["version_id"].isin(R.index)].join(R[["rel"]], on="version_id")
    LR = LR.join(cov, on="project")
    endw = LR["rel"] + pd.Timedelta(days=91)
    elig = (LR["rel"] + pd.Timedelta(days=90) <= DATA_END) & (LR["size"] >= 30) & (LR["mean"] >= 0.5)
    cdate = LR["created"].dt.tz_convert(None).dt.normalize()
    win = elig & (cdate > LR["rel"].dt.tz_convert(None).dt.normalize()) & (LR["created"] < endw)
    W = LR[win].copy()
    W["comprovado_na_janela"] = W["nivel"].str.startswith("COMPROVADO") & (W["t_add"] < endw[win])
    W["comprovado_apos_janela"] = W["nivel"].str.startswith("COMPROVADO") & (W["t_add"] >= endw[win])
    W["reconstruido"] = W["nivel"].str.startswith("RECONSTRUIDO")
    W["inferido"] = W["nivel"].str.startswith("INFERIDO")
    W["indeterminado"] = W["nivel"] == "INDETERMINADO"
    n = len(W)
    G["A3_pares_classeC_90d"] = n
    G["A3_conservadora_%(so evento na janela)"] = pct(W["comprovado_na_janela"].sum(), n)
    G["A3_ampliada_%(evento+reconstruido)"] = pct((W["comprovado_na_janela"] | W["reconstruido"]).sum(), n)
    G["A3_ampliada_max_%(+inferido)"] = pct((W["comprovado_na_janela"] | W["reconstruido"] | W["inferido"]).sum(), n)
    G["A3_incluido_apos_a_janela_%"] = pct(W["comprovado_apos_janela"].sum(), n)
    G["A3_indeterminado_%"] = pct(W["indeterminado"].sum(), n)

    # A.5 por projeto
    rows = []
    for p, l in L.groupby("project"):
        w = W[W["project"] == p]
        rows.append({"registro": "projeto", "projeto": p, "vinculos": len(l),
                     "comprovado_%": pct(l["nivel"].str.startswith("COMPROVADO").sum(), len(l)),
                     "reconstruido_%": pct(l["nivel"].str.startswith("RECONSTRUIDO").sum(), len(l)),
                     "inferido_%": pct(l["nivel"].str.startswith("INFERIDO").sum(), len(l)),
                     "indeterminado_%": pct((l["nivel"] == "INDETERMINADO").sum(), len(l)),
                     "issues_reconstrucao_inconsistente": int(l.loc[l["inc_issue"] > 0, "issue_id"].nunique()),
                     "issues_cadeia_status_quebrada": int(l.loc[~l["chain_ok"], "issue_id"].nunique()),
                     "pares_classeC_90d": len(w),
                     "conservadora_90d_%": pct(w["comprovado_na_janela"].sum(), len(w)),
                     "ampliada_90d_%": pct((w["comprovado_na_janela"] | w["reconstruido"]).sum(), len(w)),
                     "ampliada_max_90d_%": pct((w["comprovado_na_janela"] | w["reconstruido"] | w["inferido"]).sum(), len(w)),
                     "incluido_apos_janela_90d_%": pct(w["comprovado_apos_janela"].sum(), len(w)),
                     "indeterminado_90d_%": pct(w["indeterminado"].sum(), len(w))})
    PA = pd.DataFrame(rows)
    # A.7 vínculos que atravessam o corte T0 >= 2020 (todos os bugs coletados; estado atual)
    X = L.join(V.set_index("id")[["released", "rel"]], on="version_id").reset_index(drop=True)
    X["ver_cat"] = np.select(
        [~X["released"].fillna(False).astype(bool), X["rel"].isna(), X["rel"] > DATA_END, X["rel"] < SINCE],
        ["4 nao publicada", "4 publicada sem releaseDate", "4 data futura", "versao publicada <2020"],
        "versao publicada >=2020")
    X["bug_cat"] = np.select([X["created"] < pd.Timestamp("2000-01-01", tz="UTC"), X["created"] < SINCE],
                             ["bug data invalida", "bug <2020"], "bug >=2020")
    inside = X["ver_cat"] == "versao publicada >=2020"
    mixed = X.groupby("issue_id")["ver_cat"].agg(lambda s: (s == "versao publicada >=2020").any() and (s != "versao publicada >=2020").any())
    X["bug_misto"] = X["issue_id"].map(mixed)
    # links de bugs >=2020 a releases pre-2020 que caem dentro de 30/90/180 d após a release (janelas cortadas pelo recorte)
    after = X["created"] - X["rel"]
    def trio(m, df=X):
        d = df[m]
        return len(d), int(d["issue_id"].nunique()), int(d["version_id"].nunique())
    cats = {"1_bug>=2020_versao<2020": (X["bug_cat"] == "bug >=2020") & (X["ver_cat"] == "versao publicada <2020"),
            "2_bug<2020_versao>=2020": (X["bug_cat"] == "bug <2020") & inside,
            "3_bug>=2020_versao>=2020": (X["bug_cat"] == "bug >=2020") & inside,
            "4_versao_sem_data_nao_publicada_ou_futura": X["ver_cat"].str.startswith("4")}
    def cross_counts(df):
        out = {}
        for k, m in cats.items():
            m2 = m.reindex(df.index)
            n_l, n_b, n_v = trio(m2, df)
            out[f"{k}_vinculos"], out[f"{k}_bugs"], out[f"{k}_versoes"] = n_l, n_b, n_v
        sub = df[cats["4_versao_sem_data_nao_publicada_ou_futura"].reindex(df.index)]
        for r_ in ("4 nao publicada", "4 publicada sem releaseDate", "4 data futura"):
            out[f"4_{r_[2:]}_vinculos"] = int((sub["ver_cat"] == r_).sum())
        out["5_bugs_com_vinculos_dentro_e_fora"] = int(df.loc[df["bug_misto"].astype(bool), "issue_id"].nunique())
        c1 = cats["1_bug>=2020_versao<2020"].reindex(df.index)
        for w in (30, 90, 180):
            out[f"1_dentro_de_{w}d_apos_release_vinculos"] = int((c1 & (after.reindex(df.index) <= pd.Timedelta(days=w))
                                                                   & (after.reindex(df.index) > pd.Timedelta(0))).sum())
        b20i = df[df["bug_cat"] == "bug >=2020"]
        only_out = b20i.groupby("issue_id")["ver_cat"].agg(lambda s: (s != "versao publicada >=2020").all())
        out["bugs>=2020_so_com_vinculos_fora_do_recorte"] = int(only_out.sum())
        out["bugs>=2020_com_affects_version"] = int(b20i["issue_id"].nunique())
        return out
    G["A7_global"] = cross_counts(X)
    xp = {p: cross_counts(g) for p, g in X.groupby("project")}
    PA = PA.join(pd.DataFrame.from_dict(xp, orient="index"), on="projeto")
    # A.6 amostra estratificada (seed fixa; até 2 vínculos por projeto x grupo; ~60)
    low = pd.read_csv(os.path.join(a.ev, "regras_releases_bugs_por_projeto.csv"))
    low = low[low["classificacao_associacao"] == "baixa cobertura AV (<20%)"]
    low_p = low.merge(PA[["projeto", "vinculos"]], on="projeto").sort_values("vinculos", ascending=False)["projeto"].iloc[0]
    projs = SAMPLE_PROJECTS + [low_p]
    L["grupo"] = np.select([L["nivel"] == "INDETERMINADO", (L["n_rem"] > 0) & (L["n_add"] > 0),
                            L["nivel"].str.startswith("COMPROVADO"), L["n_av"] > 1],
                           ["5 indeterminado", "3 removido e reincluido", "1 inclusao por evento", "4 multiplas versoes"],
                           "2 inferido/reconstruido desde a criacao")
    rng = np.random.RandomState(SEED)
    samp = []
    for p in projs:
        for gname, g in L[L["project"] == p].groupby("grupo"):
            k = min(2, len(g))
            samp.append(g.iloc[rng.choice(len(g), k, replace=False)])
    S = pd.concat(samp)
    seqs = ve.assign(op=np.where(ve["to"] != "", "+" + ve["to"], "-" + ve["from"]))
    seqs = seqs.groupby("issue_id").apply(lambda g: " ".join(f"{t:%Y-%m-%d}{o}" for t, o in zip(g["ts"], g["op"])))
    S = S.assign(registro="amostra", issue_key=S["key"], sequencia_eventos_Version=S["issue_id"].map(seqs).fillna("(nenhum)"),
                 presente_na_criacao_reverso=S["in_initial"], inconsistencias_reverso=S["inc_issue"],
                 cadeia_status_ok=S["chain_ok"], issue_movida=S["issue_id"].isin(moved),
                 inclusao_mais_antiga=S["t_add"].dt.strftime("%Y-%m-%d %H:%M"), criacao=S["created"].dt.strftime("%Y-%m-%d %H:%M"))
    S = S.join(V.set_index("id")[["name", "releaseDate"]], on="version_id")
    S["verificacao"] = np.select(
        [S["nivel"].str.startswith("COMPROVADO"),
         S["nivel"].str.startswith("RECONSTRUIDO") & (S["n_add"] > 0),
         S["nivel"].str.startswith("RECONSTRUIDO"), S["nivel"].str.startswith("INFERIDO")],
        ["inclusao registrada; reverso consistente",
         "presente na criacao pelo reverso, com remocao/reinclusao registrada depois",
         "nenhum evento para a versao; reverso e cadeia de status consistentes",
         "sem evento e sem historico para corroborar"], "nao determinavel: " + S["motivo_indeterminado"])
    G["A_amostra"] = {"n": len(S), "projetos": projs, "por_grupo": S["grupo"].value_counts().to_dict(),
                      "por_nivel": S["nivel"].value_counts().to_dict()}
    cols_s = ["registro", "projeto", "grupo", "issue_key", "issue_id", "version_id", "name", "releaseDate", "criacao",
              "n_av", "sequencia_eventos_Version", "n_add", "n_rem", "inclusao_mais_antiga",
              "presente_na_criacao_reverso", "inconsistencias_reverso", "cadeia_status_ok", "issue_movida", "nivel", "verificacao"]
    S = S.rename(columns={"project": "projeto"})[cols_s].rename(columns={"name": "versao_nome"})
    pd.concat([PA, S], ignore_index=True).to_csv(os.path.join(a.ev, "pendencia_affects_version.csv"),
                                                 index=False, encoding="utf-8")

    # ============================================================== B. Reaberturas
    B = bugs[(bugs["created"] >= SINCE) & (bugs["created"] >= pd.Timestamp("2000-01-01", tz="UTC"))]
    bset = set(B["issue_id"])
    stb = st[st["issue_id"].isin(bset)].copy()
    stb["cf"] = stb["from_str"].map(catmap).fillna("desconhecido")
    stb["ct"] = stb["to_str"].map(catmap).fillna("desconhecido")
    rs = C[(C["field"] == "resolution") & C["issue_id"].isin(bset)][["issue_id", "ts", "from_str", "to_str"]]
    reo_st = stb[(stb["cf"] == "done") & stb["ct"].isin(["new", "indeterminate"])]
    reo_rs = rs[(rs["from_str"] != "") & (rs["to_str"] == "")]
    s1, s2 = set(reo_st["issue_id"]), set(reo_rs["issue_id"])
    mat = {"A_status_e_resolution": len(s1 & s2), "B_somente_status": len(s1 - s2),
           "C_somente_resolution": len(s2 - s1), "D_nenhum": len(bset - s1 - s2), "universo_bugs": len(bset),
           "eventos_reabertura_status": len(reo_st), "eventos_limpeza_resolution": len(reo_rs)}
    G["B_matriz"] = mat
    # resolução vigente no instante de cada transição (último evento de resolution anterior)
    rs_sorted = rs.sort_values("ts")
    def res_at(df):
        m = pd.merge_asof(df.sort_values("ts"), rs_sorted.rename(columns={"ts": "t_res", "from_str": "rf", "to_str": "res_val"}),
                          left_on="ts", right_on="t_res", by="issue_id", direction="backward", allow_exact_matches=True)
        return m
    # divergências: todos os bugs de B e C
    div_ids = (s1 - s2) | (s2 - s1)
    D = []
    proj = B.set_index("issue_id")["project"]
    key = B.set_index("issue_id")["key"]
    sg = {i: g for i, g in stb[stb["issue_id"].isin(div_ids)].groupby("issue_id")}
    rg = {i: g for i, g in rs[rs["issue_id"].isin(div_ids)].groupby("issue_id")}
    empty_s, empty_r = stb.iloc[0:0], rs.iloc[0:0]
    for iid in sorted(div_ids):
        es = sg.get(iid, empty_s)
        er = rg.get(iid, empty_r)
        tipo = "B somente status" if iid in s1 else "C somente resolution"
        if tipo == "B somente status":
            ev0 = reo_st[reo_st["issue_id"] == iid].iloc[0]
            t0 = ev0["ts"]
            before = er[er["ts"] <= t0]
            res_val = before["to_str"].iloc[-1] if len(before) else ""
            # entrada em terminal imediatamente anterior e a resolução definida nela
            prev_done = es[(es["ct"] == "done") & (es["cf"] != "done") & (es["ts"] <= t0)]
            near = er.iloc[(er["ts"] - t0).abs().argsort()[:1]] if len(er) else er
            dt_near = (near["ts"].iloc[0] - t0).total_seconds() / 60 if len(near) else None
            if res_val == "" and len(prev_done):
                causa = "fechado sem Resolution (nada a limpar ao reabrir)"
            elif res_val == "" and not len(prev_done):
                causa = "terminal sem entrada datada e sem Resolution"
            elif res_val != "":
                causa = "reaberto mantendo Resolution preenchida (workflow nao limpa)"
            transicao = f"{ev0['from_str']}->{ev0['to_str']}"
        else:
            ev0 = reo_rs[reo_rs["issue_id"] == iid].iloc[0]
            t0 = ev0["ts"]
            near = es.iloc[(es["ts"] - t0).abs().argsort()[:1]] if len(es) else es
            dt_near = (near["ts"].iloc[0] - t0).total_seconds() / 60 if len(near) else None
            st_at = es[es["ts"] <= t0]
            cur_st = st_at["to_str"].iloc[-1] if len(st_at) else "(sem transicao anterior)"
            transicao = f"status no instante: {cur_st}"
            if catmap.get(cur_st) == "done":
                causa = "Resolution limpa sem sair do status terminal"
            elif cur_st == "(sem transicao anterior)":
                causa = "Resolution limpa sem historico de status"
            else:
                causa = "Resolution limpa em status nao terminal"
            res_val = ev0["from_str"]
        D.append({"projeto": proj.get(iid), "issue_key": key.get(iid), "issue_id": iid, "tipo_divergencia": tipo,
                  "ts_evento": t0.strftime("%Y-%m-%d %H:%M"), "transicao_ou_status": transicao,
                  "resolution_vigente_no_evento": res_val,
                  "min_ate_evento_mais_proximo_outro_campo": round(dt_near, 1) if dt_near is not None else None,
                  "eventos_resolution_no_bug": len(er), "reaberturas_status_no_bug": int((reo_st["issue_id"] == iid).sum()),
                  "status_atual": B.set_index("issue_id").at[iid, "status"],
                  "resolution_atual": B.set_index("issue_id").at[iid, "resolution"], "causa_observavel": causa})
    DV = pd.DataFrame(D)
    G["B_divergencias_por_causa"] = {f"{t} | {c}": int(n) for (t, c), n in
                                     DV.groupby(["tipo_divergencia", "causa_observavel"]).size().items()}
    G["B_divergencias_projetos_top"] = DV["projeto"].value_counts().head(10).to_dict()
    # B3: transições por projeto (concentradores de divergência)
    topp = DV["projeto"].value_counts().head(8).index
    tr = stb.assign(project=stb["issue_id"].map(proj))
    def ttype(r):
        if r.cf == "done" and r.ct == "done":
            return "terminal->terminal" + (" (Resolved->Closed)" if (r.from_str, r.to_str) == ("Resolved", "Closed") else "")
        if r.cf == "done":
            return f"reabertura {r.from_str}->{r.to_str}"
        return None
    trt = tr[(tr["cf"] == "done")].copy()
    trt["tipo"] = [ttype(r) for r in trt.itertuples()]
    wf = trt[trt["project"].isin(topp)].groupby(["project", "tipo"]).size().unstack(fill_value=0)
    G["B_transicoes_saida_terminal_projetos_divergentes"] = {p: {k: int(v) for k, v in row.items() if v} for p, row in wf.iterrows()}
    # compatibilidade categoria x Resolution nas entradas em terminal
    de = tr[(tr["ct"] == "done") & (tr["cf"] != "done")]
    m = res_at(de)
    G["B_entradas_terminal_com_resolution_definida_%"] = pct((m["res_val"].fillna("") != "").sum(), len(m))
    # B4: reaberturas em até 5 minutos
    de2 = de[["issue_id", "ts", "from_str", "to_str"]].rename(columns={"ts": "t_done", "from_str": "d_from", "to_str": "d_to"})
    rr = pd.merge_asof(reo_st.sort_values("ts"), de2.sort_values("t_done"), left_on="ts", right_on="t_done",
                       by="issue_id", direction="backward")
    rr["gap"] = rr["ts"] - rr["t_done"]
    q = rr[rr["gap"] <= QUICK].copy()
    nxt = pd.merge_asof(q.sort_values("ts"), de2.rename(columns={"t_done": "t_next", "d_from": "n_from", "d_to": "n_to"})
                        .sort_values("t_next"), left_on="ts", right_on="t_next", by="issue_id",
                        direction="forward", allow_exact_matches=False)
    res_before = res_at(q[["issue_id", "t_done"]].rename(columns={"t_done": "ts"}).assign(ts=lambda d: d["ts"] + pd.Timedelta(seconds=1)))
    q = q.sort_values("ts").reset_index(drop=True)
    nxt = nxt.sort_values("ts").reset_index(drop=True)
    q["t_next"] = nxt["t_next"]
    res_b = res_before.set_index(["issue_id", "ts"])["res_val"]
    q["res_fechamento_anterior"] = [res_b.get((i, t + pd.Timedelta(seconds=1)), "") for i, t in zip(q["issue_id"], q["t_done"])]
    res_after = res_at(q[["issue_id", "t_next"]].dropna().rename(columns={"t_next": "ts"}).assign(ts=lambda d: d["ts"] + pd.Timedelta(seconds=1)))
    res_a = res_after.set_index(["issue_id", "ts"])["res_val"]
    q["res_novo_fechamento"] = [res_a.get((i, t + pd.Timedelta(seconds=1)), "") if pd.notna(t) else None
                                for i, t in zip(q["issue_id"], q["t_next"])]
    other = C[~C["field"].isin(["status", "resolution"]) & C["issue_id"].isin(set(q["issue_id"]))]
    og = {i: g for i, g in other.groupby("issue_id")}
    def other_fields(i, t1, t2):
        o = og.get(i)
        if pd.isna(t2) or o is None:
            return ""
        o = o[(o["ts"] >= t1) & (o["ts"] <= t2)]
        return "|".join(sorted(set(o["field"])))
    q["campos_alterados_no_intervalo"] = [other_fields(i, t, n) for i, t, n in zip(q["issue_id"], q["ts"], q["t_next"])]
    gap_next = q["t_next"] - q["ts"]
    q["classe"] = np.select(
        [q["t_next"].isna(),
         (gap_next <= pd.Timedelta(hours=1)) & (q["res_novo_fechamento"] != q["res_fechamento_anterior"]),
         (gap_next <= pd.Timedelta(hours=1)) & (q["campos_alterados_no_intervalo"] != ""),
         gap_next <= pd.Timedelta(hours=1)],
        ["sem novo fechamento (permanece aberto)",
         "re-encerrado <=1h com Resolution diferente (indicio de correcao administrativa)",
         "re-encerrado <=1h com outros campos alterados (indicio de ajuste administrativo)",
         "re-encerrado <=1h sem outra alteracao (indeterminado)"],
        "re-encerrado >1h (indicio de novo ciclo operacional)")
    q["project"] = q["issue_id"].map(proj)
    G["B4_reaberturas_rapidas"] = len(q)
    G["B4_classes"] = q["classe"].value_counts().to_dict()
    G["B4_campos_mais_alterados"] = q["campos_alterados_no_intervalo"].str.split("|").explode().replace("", np.nan).dropna().value_counts().head(6).to_dict()
    # concordância e rápidas por projeto
    rows = [{"escopo": "GLOBAL", **mat, "reaberturas_rapidas_<=5min": len(q),
             **{f"rapidas: {k}": v for k, v in q["classe"].value_counts().to_dict().items()}}]
    for p, b in B.groupby("project"):
        ids = set(b["issue_id"])
        qp = q[q["project"] == p]
        if not (ids & (s1 | s2)):
            continue
        rows.append({"escopo": p, "A_status_e_resolution": len(ids & s1 & s2), "B_somente_status": len(ids & (s1 - s2)),
                     "C_somente_resolution": len(ids & (s2 - s1)), "D_nenhum": len(ids - s1 - s2), "universo_bugs": len(ids),
                     "eventos_reabertura_status": int(reo_st["issue_id"].isin(ids).sum()),
                     "eventos_limpeza_resolution": int(reo_rs["issue_id"].isin(ids).sum()),
                     "reaberturas_rapidas_<=5min": len(qp),
                     **{f"rapidas: {k}": v for k, v in qp["classe"].value_counts().to_dict().items()}})
    CC = pd.DataFrame(rows).fillna(0)
    CC.to_csv(os.path.join(a.ev, "pendencia_reaberturas_concordancia.csv"), index=False, encoding="utf-8")
    DV.to_csv(os.path.join(a.ev, "pendencia_reaberturas_divergencias.csv"), index=False, encoding="utf-8")
    if a.bases:  # níveis de evidência por vínculo e classificação das reaberturas (sem reimplementação)
        os.makedirs(a.bases, exist_ok=True)
        X[["issue_id", "version_id", "project", "created", "n_av", "n_add", "n_rem", "in_initial", "t_add",
           "chain_ok", "tem_historico", "nivel", "motivo_indeterminado", "ver_cat", "bug_cat", "bug_misto"]].to_csv(
            os.path.join(a.bases, "base_vinculos_evidencia.csv"), index=False, encoding="utf-8")
        q.assign(gap_min=q["gap"].dt.total_seconds() / 60)[
            ["issue_id", "project", "ts", "t_done", "gap_min", "t_next", "res_fechamento_anterior",
             "res_novo_fechamento", "campos_alterados_no_intervalo", "classe"]].rename(
            columns={"ts": "t_reabertura", "t_done": "t_fechamento_anterior", "t_next": "t_novo_fechamento"}).to_csv(
            os.path.join(a.bases, "base_reaberturas_rapidas.csv"), index=False, encoding="utf-8")
        pd.DataFrame({"issue_id": sorted(s1 | s2)}).assign(
            reaberto_status=lambda d: d["issue_id"].isin(s1), reaberto_resolution=lambda d: d["issue_id"].isin(s2)).to_csv(
            os.path.join(a.bases, "base_reaberturas_corroboracao.csv"), index=False, encoding="utf-8")
    print(json.dumps(G, ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    main()
