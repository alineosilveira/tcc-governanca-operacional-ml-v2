"""Verificações mínimas. Testes que dependem das bases locais são pulados se ALINE_BASES_DIR não existir."""
import os
import re
from pathlib import Path

import pandas as pd
import pytest

REPO = Path(__file__).resolve().parents[1]
BASES = Path(os.environ.get("ALINE_BASES_DIR", REPO.parent / "data" / "derivados" / "bases"))
EVID = Path(os.environ.get("ALINE_EVIDENCIAS_DIR", REPO.parent / "data" / "derivados" / "evidencias"))
DATA_END = pd.Timestamp("2026-10-25", tz="UTC")
TRAIN_END = pd.Timestamp("2024-01-01", tz="UTC")
needs_bases = pytest.mark.skipif(not (BASES / "base_bugs_ciclos.csv").exists(), reason="bases locais indisponíveis")


def ts(s):
    return pd.to_datetime(s, utc=True, errors="coerce", format="ISO8601")


def read(name, **kw):
    return pd.read_csv(BASES / name, dtype=str, **kw)


# ----------------------------------------------------------------- chaves e joins
@needs_bases
def test_chaves_unicas():
    for nome, chave in (("base_releases.csv", ["version_id"]), ("base_bugs_ciclos.csv", ["issue_id"]),
                        ("base_bug_release.csv", ["issue_id", "version_id"]),
                        ("base_vinculos_evidencia.csv", ["issue_id", "version_id"]),
                        ("modelo_bugs_faixa.csv", ["issue_id"]), ("modelo_releases.csv", ["version_id"])):
        df = read(nome, usecols=chave)
        assert not df.duplicated(chave).any(), f"chave duplicada em {nome}"
        assert not df[chave].isna().any().any(), f"chave ausente em {nome}"


@needs_bases
def test_integridade_projeto_issue_versao():
    br = read("base_bug_release.csv", usecols=["issue_id", "version_id", "project"])
    rel = read("base_releases.csv", usecols=["version_id", "project_key"]).set_index("version_id")["project_key"]
    assert br["version_id"].isin(rel.index).all(), "vínculo para versão fora do inventário de releases"
    assert (br["version_id"].map(rel) == br["project"]).all(), "vínculo bug->versão de outro projeto"


@needs_bases
def test_join_nao_multiplica_bugs():
    br = read("base_bug_release.csv", usecols=["issue_id", "version_id"])
    ve = read("base_vinculos_evidencia.csv", usecols=["issue_id", "version_id", "nivel"])
    j = br.merge(ve, on=["issue_id", "version_id"], how="left")
    assert len(j) == len(br), "join com níveis de evidência multiplicou linhas"
    rel = read("modelo_releases.csv", usecols=["version_id", "bugs_180d_maximo"])
    # o alvo por release nunca excede os bugs distintos vinculados à versão
    nb = br.groupby("version_id")["issue_id"].nunique()
    m = rel.assign(n=rel["version_id"].map(nb).fillna(0), y=pd.to_numeric(rel["bugs_180d_maximo"]))
    assert (m["y"] <= m["n"]).all()


# ----------------------------------------------------------------- cronologia e T0
@needs_bases
def test_cronologia_eventos():
    b = read("base_bugs_ciclos.csv", usecols=["created", "t_b1", "t_b2", "t_b3", "t_last_close"])
    c = ts(b["created"])
    for col in ("t_b1", "t_b2", "t_b3"):
        t = ts(b[col])
        assert ((t >= c) | t.isna()).all(), f"{col} anterior à criação"
    assert ((ts(b["t_last_close"]) >= ts(b["t_b2"])) | ts(b["t_last_close"]).isna()).all()
    r = read("base_reaberturas.csv", usecols=["t_reabertura", "t_fechamento_anterior"])
    assert (ts(r["t_reabertura"]) >= ts(r["t_fechamento_anterior"])).all(), "reabertura antes do fechamento"


@needs_bases
def test_features_apenas_t0():
    mb = pd.read_csv(BASES / "modelo_bugs_faixa.csv", nrows=5)
    proibidas = {"priority", "assignee_h", "resolution", "status", "fix_versions", "t_b2", "t_b3", "d_b3",
                 "n_reab", "comment_total", "worklog_total"}
    assert not (set(mb.columns) & proibidas), "base de bugs contém variável de estado final/futura"
    mr = pd.read_csv(BASES / "modelo_releases.csv", nrows=5)
    assert not (set(mr.columns) & {"n_vinculados", "bugs_pos_180d", "issues_fixversion"}), \
        "base de releases contém composição final/desfecho como feature"


@needs_bases
def test_split_respeita_acompanhamento_completo():
    mb = read("modelo_bugs_faixa.csv", usecols=["created", "split"])
    c = ts(mb["created"])
    te = mb["split"] == "teste"
    assert (c[te] >= TRAIN_END).all() and (c[te] + pd.Timedelta(days=90) <= DATA_END).all()
    assert (c[mb["split"] == "treino"] < TRAIN_END).all()
    mr = read("modelo_releases.csv", usecols=["release_date", "split"])
    t = ts(mr["release_date"])
    te = mr["split"] == "teste"
    assert (t[te] + pd.Timedelta(days=180) <= DATA_END).all()


# ----------------------------------------------------------------- reprodutibilidade das tabelas
@needs_bases
def test_tabelas_publicadas_conferem_com_bases():
    tab = REPO / "resultados" / "tabelas"
    if not (tab / "cap6_indicadores_tempo.csv").exists():
        pytest.skip("notebook ainda não executado")
    b = read("base_bugs_ciclos.csv", usecols=["t_b3"])
    t6 = pd.read_csv(tab / "cap6_indicadores_tempo.csv")
    assert int(t6.loc[t6["indicador"].str.startswith("B3"), "bugs datados"].iloc[0]) == int(b["t_b3"].notna().sum())
    chk = pd.read_csv(tab / "preparacao_verificacao_chaves.csv")
    assert (chk["chaves duplicadas"] == 0).all()


# ----------------------------------------------------------------- decisões D2 e D8
@needs_bases
def test_d2_projetos_acima_do_limite_fora_da_h1():
    tab = REPO / "resultados" / "tabelas" / "cap9_h1_metricas_por_projeto.csv"
    if not tab.exists():
        pytest.skip("notebook ainda não executado")
    mr = pd.read_csv(BASES / "modelo_releases.csv", usecols=["project_key", "pct_vinculos_indeterminados_projeto"])
    acima = set(mr.loc[mr["pct_vinculos_indeterminados_projeto"] > 10, "project_key"])
    assert acima, "esperado ao menos um projeto acima do limite (ex.: HTTPCORE)"
    assert not (acima & set(pd.read_csv(tab)["projeto"])), "projeto com >10% de vínculos indeterminados na avaliação da H1"


def test_d8_teste_h2_inalterado():
    tab = REPO / "resultados" / "tabelas"
    atual, ant = tab / "cap9_h2_metricas_por_projeto.csv", tab / "versao_anterior_852b9c9" / "cap9_h2_metricas_por_projeto.csv"
    if not (atual.exists() and ant.exists()):
        pytest.skip("tabelas de comparação indisponíveis")
    a = pd.read_csv(atual).set_index("projeto")["bugs_teste"].sort_index()
    b = pd.read_csv(ant).set_index("projeto")["bugs_teste"].sort_index()
    assert a.equals(b), "o conjunto de teste da H2 deveria ser idêntico ao da versão anterior"


# ----------------------------------------------------------------- arquivos destinados ao GitHub
def _versionaveis():
    ignorar = {".git", ".venv", "__pycache__", ".pytest_cache", ".ipynb_checkpoints"}
    for p in REPO.rglob("*"):
        if p.is_file() and not (set(p.relative_to(REPO).parts) & ignorar):
            yield p


def test_sem_caminhos_temporarios():
    padrao = re.compile(r"AppData[\\/]+Local[\\/]+Temp|" + "scratch" + r"pad|[\\/]tmp[\\/]" + "cla" + "ude", re.I)
    for p in _versionaveis():
        if p.suffix in {".py", ".md", ".ipynb", ".txt", ".csv", ".json", ".example"}:
            assert not padrao.search(p.read_text(encoding="utf-8", errors="ignore")), f"caminho temporário em {p}"


def test_sem_credenciais_nem_dados_pessoais():
    segredo = re.compile(r"github_pat_[A-Za-z0-9_]{20,}|ghp_[A-Za-z0-9]{30,}|gho_[A-Za-z0-9]{30,}|"
                         r"Bearer\s+[A-Za-z0-9_\-\.]{20,}|" + "aws_" + "secret|BEGIN (RSA|OPENSSH) PRIVATE KEY")
    cpf = re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")
    email = re.compile(r"[A-Za-z0-9._%+-]+@(?!users\.noreply\.github\.com)[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    for p in _versionaveis():
        if p.name in {".env.local", ".env", ".salt"}:
            pytest.fail(f"arquivo sensível no repositório: {p}")
        if p.suffix in {".py", ".md", ".ipynb", ".txt", ".csv", ".json", ".example", ".gitignore"}:
            txt = p.read_text(encoding="utf-8", errors="ignore")
            assert not segredo.search(txt), f"possível credencial em {p}"
            assert not cpf.search(txt), f"possível CPF em {p}"
            assert not email.search(txt), f"possível e-mail em {p}"


def test_arquivos_pequenos():
    grandes = [p for p in _versionaveis() if p.stat().st_size > 20 * 1024 * 1024]
    assert not grandes, f"arquivos > 20 MB: {grandes}"
