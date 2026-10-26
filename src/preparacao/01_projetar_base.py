#!/usr/bin/env python3
"""
Passagem única (streaming) pela base Apache Jira, projetando somente os campos
necessários ao diagnóstico de viabilidade. NÃO modifica a base original.

Saída (cache, fora da base): CSVs compactos
  issues_c.csv     1 linha por issue (atributos selecionados)
  changelog_c.csv  1 linha por item de changelog de campos relevantes
  worklogs_c.csv   1 linha por worklog (autor pseudonimizado)
  comments_c.csv   1 linha por comentário (autor pseudonimizado, sem texto)

Autores/assignees são substituídos por hash SHA-256 com sal local (não publicado).

Uso: python 01_projetar_base.py --base data/apache_jira --cache <dir>
"""
import argparse
import csv
import hashlib
import json
import os
import secrets
import sys
import time

CL_FIELDS = {"status", "resolution", "priority", "assignee", "Fix Version", "Version", "Sprint",
             "Story Points", "Component", "issuetype", "Link", "duedate", "timeoriginalestimate",
             "timeestimate", "environment", "Severity", "labels", "Epic Link", "Parent", "Project",
             "Key", "Workflow"}
SEVERITY_IDS = ["customfield_12311036", "customfield_12311031", "customfield_12310160",
                "customfield_12311021", "customfield_12311026", "customfield_12313820"]
CF = {
    "story_points": "customfield_12310293",
    "sprint": "customfield_12310921",
    "epic_link": "customfield_12311120",
    "bug_category": "customfield_12313825",
    "regression_a": "customfield_12310080",
    "regression_b": "customfield_12314120",
    "flags": "customfield_12310250",
    "platform": "customfield_12313921",
    "est_complexity": "customfield_12310060",
    "complexity": "customfield_12313821",
    "target_version": "customfield_12312821",
    "target_versions": "customfield_12310320",
    "since_version": "customfield_12311420",
}


def filled(v):
    return v not in (None, "", [], {})


class Pseudo:
    def __init__(self, salt):
        self.salt = salt
        self.cache = {}

    def __call__(self, user):
        if not user:
            return ""
        k = (user.get("key") or user.get("name")) if isinstance(user, dict) else str(user)
        if not k:
            return ""
        h = self.cache.get(k)
        if h is None:
            h = hashlib.sha256((self.salt + k).encode()).hexdigest()[:12]
            self.cache[k] = h
        return h


def name(o, key="name"):
    return (o or {}).get(key) if isinstance(o, dict) else None


def iter_lines(path):
    with open(path, "rb") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def progress(tag, n, t0):
    if n % 200000 == 0:
        print(f"[{tag}] {n} linhas, {time.time() - t0:.0f}s", flush=True)


def issues_pass(base, cache, ps):
    cols = ["issue_id", "key", "project", "issuetype", "is_subtask", "status", "status_cat",
            "resolution", "created", "resolutiondate", "updated", "priority", "assignee_h", "reporter_h",
            "n_components", "components", "fix_versions", "affects_versions", "n_links", "link_types",
            "n_labels", "has_environment", "has_duedate", "duedate", "timeoriginalestimate", "timespent",
            "worklog_total", "comment_total", "changelog_total", "n_sprints", "story_points",
            "severity_fields", "severity_value", "bug_category", "regression", "flags", "platform",
            "est_complexity", "complexity", "target_version", "since_version", "has_epic_link",
            "has_parent", "n_subtasks", "desc_len"]
    t0 = time.time()
    with open(os.path.join(cache, "issues_c.csv"), "w", newline="", encoding="utf-8") as fo:
        w = csv.writer(fo)
        w.writerow(cols)
        for n, r in enumerate(iter_lines(os.path.join(base, "issues.jsonl")), 1):
            f = r.get("fields") or {}
            it = f.get("issuetype") or {}
            st = f.get("status") or {}
            links = []
            for l in f.get("issuelinks") or []:
                t = (l.get("type") or {}).get("name", "?")
                links.append(t + (">" if "outwardIssue" in l else "<"))
            sev_f = [s for s in SEVERITY_IDS if filled(f.get(s))]
            sev_v = name(f.get(sev_f[0]), "value") if sev_f else ""
            def cfv(k):
                v = f.get(CF[k])
                if isinstance(v, dict):
                    return v.get("value") or v.get("name") or "1"
                if isinstance(v, list):
                    return "|".join(str((x.get("value") or x.get("name")) if isinstance(x, dict) else "1")
                                    for x in v)
                return "" if v is None else str(v)
            w.writerow([
                r.get("id"), r.get("key"), name(f.get("project"), "key"), it.get("name"),
                int(bool(it.get("subtask"))), st.get("name"), name(st.get("statusCategory"), "key"),
                name(f.get("resolution")), f.get("created"), f.get("resolutiondate"), f.get("updated"),
                name(f.get("priority")), ps(f.get("assignee")), ps(f.get("reporter")),
                len(f.get("components") or []), "|".join(c.get("name", "") for c in f.get("components") or []),
                "|".join(v.get("id", "") for v in f.get("fixVersions") or []),
                "|".join(v.get("id", "") for v in f.get("versions") or []),
                len(links), "|".join(links), len(f.get("labels") or []),
                int(filled(f.get("environment"))), int(filled(f.get("duedate"))), f.get("duedate") or "",
                f.get("timeoriginalestimate") or "", f.get("timespent") or "",
                (f.get("worklog") or {}).get("total", ""), (f.get("comment") or {}).get("total", ""),
                (r.get("changelog") or {}).get("total", ""), len(f.get(CF["sprint"]) or []),
                f.get(CF["story_points"]) if f.get(CF["story_points"]) is not None else "",
                "|".join(sev_f), sev_v or "", cfv("bug_category"),
                cfv("regression_a") or cfv("regression_b"), cfv("flags"), cfv("platform"),
                cfv("est_complexity"), cfv("complexity"), cfv("target_version") or cfv("target_versions"),
                cfv("since_version"), int(filled(f.get(CF["epic_link"]))), int(filled(f.get("parent"))),
                len(f.get("subtasks") or []), len(f.get("description") or ""),
            ])
            progress("issues", n, t0)
    print(f"[issues] fim {n} em {time.time() - t0:.0f}s", flush=True)


def changelog_pass(base, cache, ps):
    t0 = time.time()
    with open(os.path.join(cache, "changelog_c.csv"), "w", newline="", encoding="utf-8") as fo:
        w = csv.writer(fo)
        w.writerow(["issue_id", "history_id", "ts", "author_h", "field", "from", "from_str", "to", "to_str"])
        for n, h in enumerate(iter_lines(os.path.join(base, "changelog.jsonl")), 1):
            items = [i for i in h.get("items") or [] if i.get("field") in CL_FIELDS]
            if items:
                a = ps(h.get("author"))
                for i in items:
                    fs, ts_ = i.get("fromString"), i.get("toString")
                    if i.get("field") == "assignee":  # pseudonimiza nomes
                        fs = ps({"key": i.get("from")}) if i.get("from") else ""
                        ts_ = ps({"key": i.get("to")}) if i.get("to") else ""
                    w.writerow([h.get("issue_id"), h.get("id"), h.get("created"), a, i.get("field"),
                                "" if i.get("field") == "assignee" else (i.get("from") or ""),
                                (fs or "")[:200], "" if i.get("field") == "assignee" else (i.get("to") or ""),
                                (ts_ or "")[:200]])
            progress("changelog", n, t0)
    print(f"[changelog] fim {n} em {time.time() - t0:.0f}s", flush=True)


def worklog_pass(base, cache, ps):
    t0 = time.time()
    with open(os.path.join(cache, "worklogs_c.csv"), "w", newline="", encoding="utf-8") as fo:
        w = csv.writer(fo)
        w.writerow(["issue_id", "worklog_id", "author_h", "started", "created", "seconds"])
        for n, r in enumerate(iter_lines(os.path.join(base, "worklogs.jsonl")), 1):
            w.writerow([r.get("issue_id"), r.get("id"), ps(r.get("author")), r.get("started"),
                        r.get("created"), r.get("timeSpentSeconds")])
            progress("worklogs", n, t0)
    print(f"[worklogs] fim {n} em {time.time() - t0:.0f}s", flush=True)


def comment_pass(base, cache, ps):
    t0 = time.time()
    with open(os.path.join(cache, "comments_c.csv"), "w", newline="", encoding="utf-8") as fo:
        w = csv.writer(fo)
        w.writerow(["issue_id", "comment_id", "author_h", "created"])
        for n, r in enumerate(iter_lines(os.path.join(base, "comments.jsonl")), 1):
            w.writerow([r.get("issue_id"), r.get("id"), ps(r.get("author")), r.get("created")])
            progress("comments", n, t0)
    print(f"[comments] fim {n} em {time.time() - t0:.0f}s", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=os.environ.get("ALINE_JIRA_DATA_DIR"), required=os.environ.get("ALINE_JIRA_DATA_DIR") is None)
    ap.add_argument("--cache", default=os.environ.get("ALINE_CACHE_DIR"), required=os.environ.get("ALINE_CACHE_DIR") is None)
    ap.add_argument("--only", default="issues,changelog,worklogs,comments")
    a = ap.parse_args()
    os.makedirs(a.cache, exist_ok=True)
    salt_path = os.path.join(a.cache, ".salt")
    if not os.path.exists(salt_path):
        with open(salt_path, "w") as f:
            f.write(secrets.token_hex(16))
    ps = Pseudo(open(salt_path).read().strip())
    steps = {"issues": issues_pass, "changelog": changelog_pass, "worklogs": worklog_pass,
             "comments": comment_pass}
    for s in a.only.split(","):
        steps[s](a.base, a.cache, ps)


if __name__ == "__main__":
    sys.exit(main())
