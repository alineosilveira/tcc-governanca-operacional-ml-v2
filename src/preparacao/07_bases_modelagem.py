#!/usr/bin/env python3
"""
Bases de modelagem com variáveis disponíveis em T0 (sem informação futura).

  modelo_bugs_faixa.csv   1 linha por bug criado >= 2020 (T0 = criação).
      alvo: faixa de tempo até a primeira correção Fixed em horizonte de 90 dias
            (<=7d, 8-30d, 31-90d, >90d ou nao Fixed) — mesma regra de 04/05 (B3).
      features: prioridade na abertura (reconstruída pelo changelog), responsável na abertura,
                Affects Version presente na criação (reconstrução reversa do 06), nº de componentes
                na criação (reverso por contagem), volume de bugs do projeto nos 30 dias anteriores
                e backlog aberto do projeto em T0 (entre bugs criados desde 2020), projeto.
  modelo_releases.csv     1 linha por release (T0 = releaseDate) em projeto com associação verificável.
      alvo: nº de bugs distintos criados após T0 e até T0+180d vinculados por Affects Version,
            em três níveis de evidência (conservador / ampliado / máximo) — regra do 06.
      features: tamanho e composição da release em T0 (Fix Version atribuída até T0, regra do 04),
                dias desde a release anterior, releases do projeto nos 90 dias anteriores,
                tipo de versão pelo nome, projeto.

Split cronológico comum: treino = T0 em 2020-01-01..2023-12-31; teste = T0 >= 2024-01-01 com
acompanhamento completo do horizonte; demais = 'fora'.

Entradas: ALINE_CACHE_DIR (issues_c.csv, changelog_c.csv), ALINE_JIRA_DATA_DIR (versions.jsonl),
ALINE_BASES_DIR (saídas --bases de 05 e 06), ALINE_EVIDENCIAS_DIR (regras_releases_bugs_por_projeto.csv,
projetos_caracterizacao.csv). Saída: ALINE_BASES_DIR.
"""
import argparse
import os
import re

import numpy as np
import pandas as pd

DATA_END = pd.Timestamp("2026-10-25", tz="UTC")
SINCE = pd.Timestamp("2020-01-01", tz="UTC")
TRAIN_END = pd.Timestamp("2024-01-01", tz="UTC")
H_BUG, H_REL = 90, 180
BANDS = ["<=7d", "8-30d", "31-90d", ">90d ou nao Fixed"]
EVOLUCAO = {"Improvement", "New Feature", "Wish", "Story", "Epic"}


def ts(s):
    return pd.to_datetime(s, utc=True, errors="coerce", format="ISO8601")


def env_arg(ap, name, env, help_=""):
    ap.add_argument(name, default=os.environ.get(env), required=os.environ.get(env) is None, help=help_)


def tipo_versao(name):
    n = str(name).lower()
    if re.search(r"(alpha|beta|rc|-m\d|milestone|preview|snapshot|incubating-rc)", n):
        return "pre-release"
    m = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", n)
    if not m:
        return "outro"
    if m.group(3) is None or m.group(3) == "0":
        return "major" if m.group(2) == "0" else "minor"
    return "patch"


def split(t0, horizon):
    return np.where(t0 < TRAIN_END, "treino",
                    np.where(t0 + pd.Timedelta(days=horizon) <= DATA_END, "teste", "fora"))


def main():
    ap = argparse.ArgumentParser()
    env_arg(ap, "--base", "ALINE_JIRA_DATA_DIR")
    env_arg(ap, "--cache", "ALINE_CACHE_DIR")
    env_arg(ap, "--bases", "ALINE_BASES_DIR")
    env_arg(ap, "--ev", "ALINE_EVIDENCIAS_DIR")
    a = ap.parse_args()

    I = pd.read_csv(os.path.join(a.cache, "issues_c.csv"), dtype=str, keep_default_na=False,
                    usecols=["issue_id", "project", "issuetype", "created", "priority", "assignee_h",
                             "n_components", "fix_versions"])
    I["created"] = ts(I["created"])
    I = I[I["created"] >= pd.Timestamp("2000-01-01", tz="UTC")]
    C = pd.read_csv(os.path.join(a.cache, "changelog_c.csv"), dtype=str, keep_default_na=False,
                    usecols=["issue_id", "ts", "field", "from", "from_str", "to"])
    C = C[C["field"].isin(["priority", "assignee", "Component", "Fix Version"])]
    C["ts"] = ts(C["ts"])
    C = C.sort_values(["issue_id", "ts"], kind="stable")

    # ------------------------------------------------------------------ bugs
    bc = pd.read_csv(os.path.join(a.bases, "base_bugs_ciclos.csv"), dtype={"issue_id": str})
    bc["created"] = ts(bc["created"])
    B = bc[["issue_id", "project", "created", "d_b3", "t_b2"]].copy()
    B["t_b2"] = ts(B["t_b2"])
    d = B["d_b3"]
    B["faixa_90d"] = np.select([d <= 7, d <= 30, d <= H_BUG], BANDS[:3], BANDS[3])
    B["split"] = split(B["created"], H_BUG)
    meta = I.set_index("issue_id")
    pr_first = C[C["field"] == "priority"].groupby("issue_id").first()
    B["prioridade_t0"] = np.where(B["issue_id"].isin(pr_first.index), B["issue_id"].map(pr_first["from_str"]),
                                  B["issue_id"].map(meta["priority"]))
    asg_first = C[C["field"] == "assignee"].groupby("issue_id").first()
    B["responsavel_na_abertura"] = np.where(B["issue_id"].isin(asg_first.index),
                                            B["issue_id"].map(asg_first["from_str"]).fillna("") != "",
                                            B["issue_id"].map(meta["assignee_h"]).fillna("") != "").astype(int)
    comp = C[C["field"] == "Component"]
    adds = comp[comp["to"] != ""].groupby("issue_id").size()
    rems = comp[comp["from"] != ""].groupby("issue_id").size()
    ncomp = pd.to_numeric(B["issue_id"].map(meta["n_components"]), errors="coerce").fillna(0)
    B["componentes_na_criacao"] = (ncomp - B["issue_id"].map(adds).fillna(0) + B["issue_id"].map(rems).fillna(0)).clip(lower=0)
    ve = pd.read_csv(os.path.join(a.bases, "base_vinculos_evidencia.csv"), dtype={"issue_id": str, "version_id": str})
    av0 = ve[(ve["in_initial"] == True) & (ve["nivel"] != "INDETERMINADO")].groupby("issue_id").size()  # noqa: E712
    B["affects_version_na_criacao"] = B["issue_id"].isin(av0.index).astype(int)
    # contexto do projeto estritamente anterior a T0
    allbugs = I[I["issuetype"] == "Bug"][["project", "created"]].sort_values("created")
    vol = []
    backlog = []
    gb = {p: g["created"].values for p, g in allbugs.groupby("project")}
    closed = {p: np.sort(g["t_b2"].dropna().values) for p, g in B.groupby("project")}
    created20 = {p: np.sort(g["created"].values) for p, g in B.groupby("project")}
    for p, t in zip(B["project"], B["created"]):
        arr = gb.get(p)
        t64 = np.datetime64(t.tz_convert(None))
        vol.append(int(np.searchsorted(arr, t64, "left") - np.searchsorted(arr, t64 - np.timedelta64(30, "D"), "left"))
                   if arr is not None else 0)
        c_arr, k_arr = created20.get(p), closed.get(p)
        n_created = np.searchsorted(c_arr, t64, "left") if c_arr is not None else 0
        n_closed = np.searchsorted(k_arr, t64, "left") if k_arr is not None and len(k_arr) else 0
        backlog.append(int(n_created - n_closed))
    B["bugs_projeto_30d_anteriores"] = vol
    B["backlog_aberto_projeto_t0"] = backlog
    B.drop(columns=["d_b3", "t_b2"]).to_csv(os.path.join(a.bases, "modelo_bugs_faixa.csv"), index=False, encoding="utf-8")

    # ------------------------------------------------------------------ releases
    V = pd.read_json(os.path.join(a.base, "versions.jsonl"), lines=True, dtype=False)
    V["id"] = V["id"].astype(str)
    V["rel"] = ts(V["releaseDate"])
    V["released"] = V["released"].fillna(False).astype(bool)
    Vr = V[V["released"] & V["rel"].notna() & (V["rel"] <= DATA_END)].sort_values(["project_key", "rel"])
    Vr["dias_desde_release_anterior"] = Vr.groupby("project_key")["rel"].diff().dt.days
    Vr["releases_90d_anteriores"] = Vr.groupby("project_key")["rel"].transform(
        lambda s: [int(((s < t) & (s >= t - pd.Timedelta(days=90))).sum()) for t in s])
    R = pd.read_csv(os.path.join(a.bases, "base_releases.csv"), dtype={"version_id": str})
    R["release_date"] = ts(R["release_date"])
    reg = pd.read_csv(os.path.join(a.ev, "regras_releases_bugs_por_projeto.csv"))
    car = pd.read_csv(os.path.join(a.ev, "projetos_caracterizacao.csv"))
    verif = set(reg.loc[reg["classificacao_associacao"] == "associacao verificavel (AV>=50%)", "projeto"])
    modular = set(car.loc[car["nomes_modulares_%"].fillna(0) >= 30, "projeto"])
    R = R[R["project_key"].isin(verif)].copy()
    R["projeto_modular"] = R["project_key"].isin(modular).astype(int)
    R = R.join(Vr.set_index("id")[["dias_desde_release_anterior", "releases_90d_anteriores"]], on="version_id")
    R["tipo_versao"] = R["name"].map(tipo_versao)
    # composição em T0: issues com Fix Version atribuída até T0 (+1 dia) — mesma regra de 04
    fva = C[(C["field"] == "Fix Version") & (C["to"] != "")].groupby(["issue_id", "to"])["ts"].max()
    FV = I[I["fix_versions"] != ""][["issue_id", "issuetype", "created", "fix_versions"]].assign(
        version_id=lambda x: x["fix_versions"].str.split("|")).explode("version_id")
    FV = FV[FV["version_id"].isin(set(R["version_id"]))]
    FV["t"] = [fva.get((i, v), c) for i, v, c in zip(FV["issue_id"], FV["version_id"], FV["created"])]
    FV = FV.join(R.set_index("version_id")["release_date"], on="version_id")
    FV = FV[FV["t"] <= FV["release_date"] + pd.Timedelta(days=1)]
    comp_t0 = FV.groupby("version_id").agg(tamanho_t0=("issue_id", "nunique"),
                                           bugs_na_release_t0=("issuetype", lambda s: (s == "Bug").sum()),
                                           evolucao_na_release_t0=("issuetype", lambda s: s.isin(EVOLUCAO).sum()))
    R = R.join(comp_t0, on="version_id")
    R[["tamanho_t0", "bugs_na_release_t0", "evolucao_na_release_t0"]] = R[
        ["tamanho_t0", "bugs_na_release_t0", "evolucao_na_release_t0"]].fillna(0).astype(int)
    # alvo por nível de evidência (classe C, janela 180 d)
    br = pd.read_csv(os.path.join(a.bases, "base_bug_release.csv"), dtype={"issue_id": str, "version_id": str})
    br = br[br["pos_180"] == True]  # noqa: E712
    br = br.merge(ve[["issue_id", "version_id", "nivel", "t_add"]], on=["issue_id", "version_id"], how="left")
    br["release_date"] = ts(br["release_date"])
    br["t_add"] = ts(br["t_add"])
    endw = br["release_date"] + pd.Timedelta(days=H_REL + 1)
    comprov = br["nivel"].str.startswith("COMPROVADO", na=False) & (br["t_add"] < endw)
    recons = br["nivel"].str.startswith("RECONSTRUIDO", na=False)
    infer = br["nivel"].str.startswith("INFERIDO", na=False)
    for nome, m in (("bugs_180d_conservador", comprov), ("bugs_180d_ampliado", comprov | recons),
                    ("bugs_180d_maximo", comprov | recons | infer)):
        R[nome] = R["version_id"].map(br[m].groupby("version_id")["issue_id"].nunique()).fillna(0).astype(int)
    R["acompanhamento_180d_completo"] = (R["release_date"] + pd.Timedelta(days=H_REL) <= DATA_END).astype(int)
    R["split"] = split(R["release_date"], H_REL)
    keep = ["version_id", "project_key", "name", "release_date", "split", "classe_180d", "projeto_modular",
            "tipo_versao", "tamanho_t0", "bugs_na_release_t0", "evolucao_na_release_t0",
            "dias_desde_release_anterior", "releases_90d_anteriores", "acompanhamento_180d_completo",
            "bugs_180d_conservador", "bugs_180d_ampliado", "bugs_180d_maximo"]
    R[keep].to_csv(os.path.join(a.bases, "modelo_releases.csv"), index=False, encoding="utf-8")
    print(f"modelo_bugs_faixa: {len(B)} bugs ({(B['split'] == 'treino').sum()} treino / {(B['split'] == 'teste').sum()} teste)")
    print(f"modelo_releases: {len(R)} releases ({(R['split'] == 'treino').sum()} treino / {(R['split'] == 'teste').sum()} teste)")


if __name__ == "__main__":
    main()
