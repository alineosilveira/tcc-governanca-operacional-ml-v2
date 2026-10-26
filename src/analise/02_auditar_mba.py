#!/usr/bin/env python3
"""
Auditoria dos materiais de aula do MBA: localiza evidências textuais de técnicas
estatísticas/ML por arquivo e página (PDF) ou arquivo interno (notebooks/scripts
dentro de .zip, lidos sem extração). Não modifica os materiais.

Saídas:
  evidencias/mba_inventario_arquivos.csv   arquivos examinados (dedup por conteúdo)
  evidencias/mba_ocorrencias_tecnicas.csv  técnica x arquivo x página x trecho
"""
import argparse
import csv
import hashlib
import io
import json
import os
import re
import zipfile

try:
    import pymupdf as fitz  # PyMuPDF >= 1.24
except ImportError:
    import fitz

# padrões de busca (case-insensitive); termos em PT e EN e chamadas de bibliotecas
TECH = {
    "Analise exploratoria": r"an[aá]lise explorat[oó]ria|exploratory data analysis|\bEDA\b",
    "Estatistica descritiva": r"estat[ií]stica descritiva|medidas de posi[cç][aã]o|desvio[- ]padr[aã]o|quartil",
    "Estatistica inferencial / testes de hipoteses": r"teste de hip[oó]tese|hip[oó]tese nula|p[- ]valor|p-value|intervalo de confian[cç]a|teste t\b|qui[- ]quadrado",
    "Correlacao": r"correla[cç][aã]o de pearson|coeficiente de correla[cç][aã]o|\bcorrela[cç][aã]o\b|\.corr\(",
    "Regressao linear simples/multipla": r"regress[aã]o (linear|simples|m[uú]ltipla)|\bOLS\b|smf\.ols|m[ií]nimos quadrados",
    "Regressao logistica binaria": r"log[ií]stic[oa] bin[aá]ri|regress[aã]o log[ií]stica|smf\.logit|LogisticRegression",
    "Regressao logistica multinomial": r"multinomial|MNLogit",
    "Modelos de contagem (Poisson/Binomial Negativa/ZI)": r"poisson|binomial negativ|negative ?binomial|zero[- ]inflat|inflacionad",
    "Modelagem multinivel / efeitos aleatorios": r"multin[ií]vel|multilevel|efeitos? aleat[oó]rios|mixedlm|HLM",
    "Arvores de decisao": r"[aá]rvores? de decis[aã]o|decision ?tree|DecisionTree",
    "Random Forest": r"random ?forest|floresta aleat|RandomForest",
    "Boosting (AdaBoost/GBM/XGBoost)": r"boosting|xgboost|adaboost|gradient ?boost|lightgbm",
    "Bagging / Ensemble": r"\bbagging\b|ensemble",
    "Redes neurais / MLP": r"redes? neurais|neural network|\bMLP|perceptron|keras|tensorflow",
    "SVM": r"support vector|\bSVM\b|\bSVC\b",
    "KNN": r"\bKNN\b|k[- ]nearest|vizinhos mais pr[oó]ximos",
    "Clusterizacao": r"cluster|k[- ]means|agrupamento hier",
    "PCA / Analise fatorial": r"\bPCA\b|an[aá]lise fatorial|componentes principais",
    "Series temporais (ARIMA/decomposicao/suavizacao)": r"\bARIMA\b|s[eé]ries? temporais|time series|holt|suaviza[cç][aã]o exponencial|sazonalidade",
    "Analise de sobrevivencia": r"sobreviv[eê]ncia|survival|kaplan|cox proportional|\bcensur",
    "Tratamento de dados ausentes": r"dados (ausentes|faltantes)|missing values?|valores? ausentes|\bdropna\b|fillna|imputa[cç]",
    "Engenharia de atributos / dummies": r"engenharia de (atributos|vari[aá]veis|features)|feature engineering|dummiz|vari[aá]veis dummy|get_dummies|one[- ]hot",
    "Divisao treino/teste": r"treino e teste|treinamento e teste|train_test_split|base de (treino|teste)|amostra de (treino|teste)",
    "Validacao cruzada": r"valida[cç][aã]o cruzada|cross[- ]?validation|k[- ]?fold|cross_val",
    "Validacao temporal": r"TimeSeriesSplit|valida[cç][aã]o temporal|janela (m[oó]vel|deslizante)|walk[- ]forward|rolling (origin|window)|out[- ]of[- ]time",
    "Matriz de confusao / acuracia / sensibilidade": r"matriz de confus|confusion_matrix|confusion matrix|acur[aá]cia|sensitividade|sensibilidade|especificidade|precis[aã]o|recall|f1",
    "Curva ROC / AUC": r"\bROC\b|\bAUC\b|roc_auc|curva roc",
    "Metricas de regressao (RMSE/MAE/R2)": r"\bRMSE\b|\bMAE\b|\bMSE\b|\bMAPE\b|R[²2] ajustado|r2_score|coeficiente de determina",
    "Balanceamento de classes": r"desbalancead|imbalanc|SMOTE|oversampl|undersampl|class_weight",
    "Ajuste de hiperparametros": r"hiperpar[aâ]metro|hyperparameter|GridSearch|RandomizedSearch|grid search",
    "Explicabilidade (importancia/SHAP/LIME)": r"\bSHAP\b|\bLIME\b|feature_importances|import[aâ]ncia (das|de) vari[aá]veis|explicabilidade|interpretabilidade|permutation_importance",
    "Text mining / NLP": r"text mining|\bNLP\b|tokeniz|TF-?IDF|sentiment|sentimento",
    "Stepwise / selecao de variaveis": r"stepwise|sele[cç][aã]o de vari[aá]veis|feature selection",
    "Odds ratio / chance": r"odds ratio|raz[aã]o de chances|\bchance\b",
    "Box-Cox / transformacoes": r"box[- ]cox",
}
TECH_RE = {k: re.compile(v, re.I) for k, v in TECH.items()}
CODE_EXT = (".ipynb", ".py", ".r", ".R", ".txt")


def norm_name(fn):
    return re.sub(r" \(\d+\)(?=\.[A-Za-z]+$)", "", fn)


# CPF da marca d'água é sempre mascarado; nomes da marca d'água vêm de ALINE_REDACT_NAMES (separados por ';')
REDACT = [re.compile(r"\d{3}\.\d{3}\.\d{3}-\d{2}")] + [
    re.compile(r"\s+".join(map(re.escape, n.split())), re.I)
    for n in os.environ.get("ALINE_REDACT_NAMES", "").split(";") if n.strip()]


def redact(s):
    for rx in REDACT:
        s = rx.sub("[REDACTED]", s)
    return s


def snippet(text, m, width=90):
    s = max(0, m.start() - width)
    return redact(re.sub(r"\s+", " ", text[s:m.end() + width]).strip())[:220]


def scan_text(units, rows, source, kind):
    """units: lista de (página/arquivo interno, texto)."""
    for loc, text in units:
        for tech, rx in TECH_RE.items():
            hits = list(rx.finditer(text))
            if hits:
                rows.append({"tecnica": tech, "arquivo": source, "tipo": kind, "local": loc,
                             "n_ocorrencias": len(hits), "trecho": snippet(text, hits[0])})


def notebook_text(raw):
    try:
        nb = json.loads(raw)
    except Exception:
        return raw.decode("utf-8", "ignore")
    parts = []
    for c in nb.get("cells", []):
        src = c.get("source", "")
        parts.append("".join(src) if isinstance(src, list) else src)
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aulas", default=os.environ.get("ALINE_AULAS_DIR"), required=os.environ.get("ALINE_AULAS_DIR") is None)
    ap.add_argument("--out", default=os.environ.get("ALINE_EVIDENCIAS_DIR"), required=os.environ.get("ALINE_EVIDENCIAS_DIR") is None)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    inv, rows, seen = [], [], {}
    for fn in sorted(os.listdir(a.aulas)):
        p = os.path.join(a.aulas, fn)
        ext = os.path.splitext(fn)[1].lower()
        if ext not in (".pdf", ".zip"):
            inv.append({"arquivo": fn, "tipo": ext, "status": "nao examinado (formato)", "unidades": ""})
            continue
        if ext == ".pdf":
            doc = fitz.open(p)
            pages = [(f"p.{i + 1}", pg.get_text()) for i, pg in enumerate(doc)]
            h = hashlib.md5("".join(t for _, t in pages).encode()).hexdigest()
            if h in seen:
                inv.append({"arquivo": fn, "tipo": "pdf", "status": f"duplicata textual de {seen[h]}",
                            "unidades": len(pages)})
                continue
            seen[h] = fn
            inv.append({"arquivo": fn, "tipo": "pdf", "status": "examinado", "unidades": len(pages)})
            scan_text(pages, rows, norm_name(fn), "pdf")
        else:
            try:
                z = zipfile.ZipFile(p)
            except zipfile.BadZipFile:
                inv.append({"arquivo": fn, "tipo": "zip", "status": "zip inválido", "unidades": ""})
                continue
            units = []
            for zi in z.infolist():
                if zi.is_dir() or not zi.filename.endswith(CODE_EXT) or zi.file_size > 20_000_000:
                    continue
                raw = z.read(zi)
                txt = notebook_text(raw) if zi.filename.endswith(".ipynb") else raw.decode("utf-8", "ignore")
                units.append((zi.filename, txt))
            h = hashlib.md5("".join(t for _, t in units).encode()).hexdigest()
            if units and h in seen:
                inv.append({"arquivo": fn, "tipo": "zip", "status": f"duplicata textual de {seen[h]}",
                            "unidades": len(units)})
                continue
            seen[h] = fn
            inv.append({"arquivo": fn, "tipo": "zip",
                        "status": "examinado" if units else "sem notebooks/scripts de texto",
                        "unidades": len(units)})
            scan_text(units, rows, norm_name(fn), "codigo")
    with open(os.path.join(a.out, "mba_inventario_arquivos.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, ["arquivo", "tipo", "status", "unidades"])
        w.writeheader()
        w.writerows(inv)
    with open(os.path.join(a.out, "mba_ocorrencias_tecnicas.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, ["tecnica", "arquivo", "tipo", "local", "n_ocorrencias", "trecho"])
        w.writeheader()
        w.writerows(rows)
    print(f"arquivos={len(inv)} examinados={sum(1 for i in inv if i['status'] == 'examinado')} ocorrencias={len(rows)}")


if __name__ == "__main__":
    main()
