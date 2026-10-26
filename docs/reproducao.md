# Reprodução

## Modos de uso

| Modo | O que é possível | Requisitos |
|---|---|---|
| **1. Consulta** | Ler o notebook já executado (tabelas, gráficos e conclusões) no GitHub ou no Colab, e ver `resultados/` | Nenhum |
| **2. Reprodução completa local** | Refazer as bases analíticas e reexecutar o notebook, obtendo os mesmos números | Snapshot JSONL de 25/10/2026 (≈ 43 GB com intermediários; ≈ 21 GB de arquivos finais) e Python 3.11+ |
| **3. Reexecução no Colab** | **Não disponível nesta versão.** As bases analíticas linha a linha não são publicadas (política conservadora), então no Colab o notebook serve só para consulta. | — |

## Por que o snapshot não está no GitHub

- **Volume:** ≈ 21 GB de JSONL finais, mais ≈ 22 GB de parciais de retomada.
- **Conteúdo:** os arquivos contêm nomes de exibição e logins de contribuidores da Apache, além do texto integral de comentários (a API anônima não expõe e-mails). São dados públicos na origem, mas a sua redistribuição em massa num repositório de TCC não é adequada.
- **O que é publicado:** só código, documentação, resultados agregados por projeto e gráficos.

## Nova coleta (resultado pode diferir)

```bash
pip install -r requirements.txt
export ALINE_JIRA_DATA_DIR=/caminho/data/apache_jira
python src/coleta/apache_jira_extract.py --dry-run     # inspeção + plano
python src/coleta/apache_jira_extract.py               # coleta completa; repetir o comando retoma do checkpoint
python src/coleta/quality_report.py                    # relatório de integridade/qualidade
```

O Jira da Apache continua sendo atualizado, então uma nova coleta **não** reproduz exatamente o snapshot de 25/10/2026: a coleta registrou 561.363 issues no planejamento e 561.369 ao final. A coleta anterior levou ~1h35, com 4 a 8 requisições simultâneas e retentativas. Para a reprodução exata dos números do notebook, é necessário o snapshot correspondente (`manifest.json` em `resultados/coleta/` identifica a extração).

## Preparação das bases (Modo 2)

```bash
export ALINE_JIRA_DATA_DIR=/caminho/data/apache_jira
export ALINE_CACHE_DIR=/caminho/data/cache_projecao
export ALINE_EVIDENCIAS_DIR=/caminho/data/derivados/evidencias
export ALINE_BASES_DIR=/caminho/data/derivados/bases

python src/preparacao/01_projetar_base.py          # ~4 min; uma passagem pelos JSONL
python src/analise/03_diagnostico_cobertura.py     # ~1 min
python src/analise/04_caracterizacao_por_projeto.py
python src/preparacao/05_validar_regras_negocio.py # ~1-2 min; grava bases B-E (ALINE_BASES_DIR definido)
python src/preparacao/06_validar_pendencias.py     # ~5 min; grava níveis de evidência
python src/preparacao/07_bases_modelagem.py        # bases de modelagem (T0, split cronológico)
python -m pytest tests -q                          # verificações mínimas
```

O sal de pseudonimização é gerado na primeira execução do 01 (`ALINE_CACHE_DIR/.salt`). Deve ser mantido local para que os hashes sejam estáveis.

## Execução do notebook

```bash
jupyter nbconvert --to notebook --execute --inplace TCC_Analise_e_Modelos_v2.ipynb
# ou, sem Jupyter instalado:
python -c "import nbformat,nbclient;nb=nbformat.read('TCC_Analise_e_Modelos_v2.ipynb',4);nbclient.NotebookClient(nb,timeout=1800).execute();nbformat.write(nb,'TCC_Analise_e_Modelos_v2.ipynb')"
```

O notebook lê `ALINE_JIRA_DATA_DIR` (só `manifest.json`, `data_quality_report.md` e `errors.jsonl`), `ALINE_EVIDENCIAS_DIR` e `ALINE_BASES_DIR`. Ele grava tabelas agregadas em `resultados/tabelas/` e gráficos em `resultados/graficos/`.

## Ambiente testado

Windows 11, Python 3.13.13, com as versões efetivamente instaladas:

| Pacote | Versão |
|---|---|
| httpx | 0.28.1 |
| pandas | 2.3.3 |
| numpy | 2.5.4 |
| scipy | 1.18.1 |
| matplotlib | 3.11.2 |
| scikit-learn | 1.9.1 |
| statsmodels | 0.15.0 |
| nbformat | 5.11.1 |
| nbclient | 0.11.0 |
| ipykernel | 7.4.0 |
| pytest | 9.1.1 |
| pymupdf | 2.0 |
