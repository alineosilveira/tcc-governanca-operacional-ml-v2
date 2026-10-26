#!/usr/bin/env python3
"""
Extrator read-only de dados públicos do Apache Jira (Jira Data Center/Server REST API v2).

- Somente requisições GET anônimas; nenhuma credencial é usada ou registrada.
- Um único processo coordena concorrência (limitador AIMD global), rate limit,
  retentativas (backoff exponencial + jitter, Retry-After) e checkpoints.
- Trabalho dividido em unidades disjuntas (janelas de `created`), cada uma com
  checkpoint por página (offsets dos arquivos parciais), permitindo retomada.

Uso típico:
  python apache_jira_extract.py --dry-run                     # inspeção + plano
  python apache_jira_extract.py --out data/pilot --limit 100 --max-units 8 --projects-limit 15
  python apache_jira_extract.py                               # coleta completa (retoma automaticamente)
"""
from __future__ import annotations

import argparse
import asyncio
import datetime as dt
import email.utils
import glob
import json
import os
import random
import re
import sys
import time

import httpx

API = "/rest/api/2"
DEFAULT_BASE = "https://issues.apache.org/jira"
SPRINT_FIELD_NAME = "Sprint"


def utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def dumps(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def atomic_write_json(path: str, obj, indent=None) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=indent)
        f.flush()
        os.fsync(f.fileno())
    replace_with_retry(tmp, path)


def replace_with_retry(src: str, dst: str, attempts: int = 50) -> None:
    """No Windows, os.replace falha se o destino estiver aberto por outro processo
    (leitor, antivírus, indexador); tenta novamente por alguns segundos."""
    for i in range(attempts):
        try:
            os.replace(src, dst)
            return
        except PermissionError:
            if i == attempts - 1:
                raise
            time.sleep(0.1 + 0.05 * i)


def truncate_to(path: str, size: int) -> None:
    if os.path.exists(path) and os.path.getsize(path) > size:
        with open(path, "r+b") as f:
            f.truncate(size)


def truncate_to_last_newline(path: str) -> None:
    """Remove uma linha final parcial (gravação interrompida)."""
    if not os.path.exists(path):
        return
    size = os.path.getsize(path)
    if size == 0:
        return
    with open(path, "r+b") as f:
        pos = size
        while pos > 0:
            step = min(65536, pos)
            f.seek(pos - step)
            chunk = f.read(step)
            i = chunk.rfind(b"\n")
            if i >= 0:
                f.truncate(pos - step + i + 1)
                return
            pos -= step
        f.truncate(0)


def iter_jsonl(path: str):
    with open(path, "rb") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


# --------------------------------------------------------------------------- #
# Log de erros e métricas
# --------------------------------------------------------------------------- #
class ErrorLog:
    def __init__(self, path: str):
        truncate_to_last_newline(path)
        self.f = open(path, "a", encoding="utf-8")
        self.count = 0

    def log(self, **kw) -> None:
        kw.setdefault("ts", utcnow())
        self.f.write(dumps(kw) + "\n")
        self.f.flush()
        self.count += 1


class Metrics:
    def __init__(self, path: str):
        self.path = path
        self.t0 = time.monotonic()
        self.requests = 0
        self.ok = 0
        self.bytes = 0
        self.records = 0
        self.statuses: dict[str, int] = {}
        self.timeouts = 0
        self.throttled = 0
        self._last = (self.t0, 0, 0)
        self.history: list[dict] = []

    def snapshot(self, limiter) -> dict:
        now = time.monotonic()
        lt, lr, lrec = self._last
        dtw = max(now - lt, 1e-6)
        snap = {
            "ts": utcnow(),
            "elapsed_s": round(now - self.t0, 1),
            "requests": self.requests,
            "records": self.records,
            "mb": round(self.bytes / 1e6, 1),
            "req_per_s_window": round((self.requests - lr) / dtw, 2),
            "records_per_s_window": round((self.records - lrec) / dtw, 1),
            "req_per_s_total": round(self.requests / max(now - self.t0, 1e-6), 2),
            "concurrency_limit": limiter.limit,
            "inflight": limiter.inflight,
            "timeouts": self.timeouts,
            "throttled": self.throttled,
            "statuses": dict(self.statuses),
        }
        self._last = (now, self.requests, self.records)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(dumps(snap) + "\n")
        return snap


# --------------------------------------------------------------------------- #
# Cliente HTTP com limitador global adaptativo
# --------------------------------------------------------------------------- #
class RetryExhausted(Exception):
    pass


class Limiter:
    """Concorrência AIMD: começa em `start`, +1 a cada `ramp_every` sucessos
    sem incidentes até `cmax`; divide por 2 em 429/503/timeout/5xx."""

    def __init__(self, start: int, cmax: int, max_rps: float, ramp_every: int, log):
        self.limit = max(1, min(start, cmax))
        self.cmax = cmax
        self.inflight = 0
        self.cond = asyncio.Condition()
        self.min_interval = 1.0 / max_rps if max_rps > 0 else 0.0
        self.next_slot = 0.0
        self.slot_lock = asyncio.Lock()
        self.pause_until = 0.0
        self.streak = 0
        self.ramp_every = ramp_every
        self.log = log
        self.changes: list[dict] = []

    async def acquire(self) -> None:
        async with self.cond:
            while self.inflight >= self.limit:
                await self.cond.wait()
            self.inflight += 1
        async with self.slot_lock:
            now = time.monotonic()
            start = max(now, self.next_slot, self.pause_until)
            self.next_slot = start + self.min_interval
        delay = start - time.monotonic()
        if delay > 0:
            await asyncio.sleep(delay)

    async def release(self, outcome: str) -> None:
        async with self.cond:
            self.inflight -= 1
            if outcome == "ok":
                self.streak += 1
                if self.streak >= self.ramp_every and self.limit < self.cmax:
                    self._set(self.limit + 1, "ramp-up após %d sucessos" % self.streak)
                    self.streak = 0
            elif outcome == "throttle":
                self.streak = 0
                new = max(1, self.limit // 2)
                if new != self.limit:
                    self._set(new, "redução por 429/503/timeout/5xx")
            self.cond.notify_all()

    def pause(self, seconds: float) -> None:
        self.pause_until = max(self.pause_until, time.monotonic() + seconds)

    def _set(self, new: int, why: str) -> None:
        self.changes.append({"ts": utcnow(), "from": self.limit, "to": new, "why": why})
        self.log(f"[limiter] concorrência {self.limit} -> {new} ({why})")
        self.limit = new


def parse_retry_after(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        try:
            when = email.utils.parsedate_to_datetime(value)
            return max(0.0, (when - dt.datetime.now(dt.timezone.utc)).total_seconds())
        except Exception:
            return None


class Api:
    RETRY_STATUSES = {408, 429, 500, 502, 503, 504}

    def __init__(self, base: str, args, errors: ErrorLog, metrics: Metrics, log):
        self.base = base.rstrip("/")
        self.errors = errors
        self.metrics = metrics
        self.log = log
        self.limiter = Limiter(args.concurrency_start, args.concurrency_max, args.max_rps,
                               args.ramp_every, log)
        self.backoff_base = args.backoff_base
        self.backoff_cap = args.backoff_cap
        self.max_attempts = args.max_attempts
        self.client = httpx.AsyncClient(
            base_url=self.base,
            timeout=httpx.Timeout(connect=args.connect_timeout, read=args.read_timeout,
                                  write=30.0, pool=None),
            limits=httpx.Limits(max_connections=args.concurrency_max + 2,
                                max_keepalive_connections=args.concurrency_max + 2),
            headers={"Accept": "application/json",
                     "User-Agent": "apache-jira-research-extractor/1.0 (read-only; low-rate)"},
            follow_redirects=True,
        )

    async def close(self):
        await self.client.aclose()

    async def get_json(self, path: str, params: dict | None = None, ctx: dict | None = None,
                       max_attempts: int | None = None):
        """Retorna (status, json|None). Status 4xx permanentes retornam sem retry.
        Lança RetryExhausted se erros transitórios persistirem."""
        attempts = max_attempts or self.max_attempts
        ctx = ctx or {}
        last_err = None
        for attempt in range(1, attempts + 1):
            await self.limiter.acquire()
            outcome = "ok"
            try:
                self.metrics.requests += 1
                resp = await self.client.get(path, params=params)
            except (httpx.TimeoutException, httpx.TransportError) as e:
                outcome = "throttle"
                self.metrics.timeouts += 1
                last_err = f"{type(e).__name__}: {e}"[:300]
                self.errors.log(endpoint=path, params=_safe_params(params), **ctx, status=None,
                                message=last_err, attempt=attempt, retried=attempt < attempts)
                await self.limiter.release(outcome)
                await asyncio.sleep(self._backoff(attempt))
                continue
            status = resp.status_code
            self.metrics.statuses[str(status)] = self.metrics.statuses.get(str(status), 0) + 1
            self.metrics.bytes += len(resp.content)
            if status == 200:
                try:
                    data = await asyncio.to_thread(json.loads, resp.content)
                except ValueError as e:
                    outcome = "throttle"
                    last_err = f"JSON inválido: {e}"[:300]
                    self.errors.log(endpoint=path, params=_safe_params(params), **ctx, status=status,
                                    message=last_err, attempt=attempt, retried=attempt < attempts)
                    await self.limiter.release(outcome)
                    await asyncio.sleep(self._backoff(attempt))
                    continue
                self.metrics.ok += 1
                await self.limiter.release("ok")
                return status, data
            msg = _err_message(resp)
            if status in self.RETRY_STATUSES:
                outcome = "throttle"
                self.metrics.throttled += status in (429, 503)
                ra = parse_retry_after(resp.headers.get("Retry-After"))
                wait = ra if ra is not None else self._backoff(attempt)
                if status in (429, 503):
                    self.limiter.pause(wait)
                last_err = f"HTTP {status}: {msg}"
                self.errors.log(endpoint=path, params=_safe_params(params), **ctx, status=status,
                                message=msg, retry_after=ra, attempt=attempt,
                                retried=attempt < attempts)
                await self.limiter.release(outcome)
                await asyncio.sleep(wait)
                continue
            # 4xx permanente: não repetir
            self.errors.log(endpoint=path, params=_safe_params(params), **ctx, status=status,
                            message=msg, attempt=attempt, retried=False)
            await self.limiter.release("neutral")
            return status, None
        raise RetryExhausted(last_err or "retentativas esgotadas")

    def _backoff(self, attempt: int) -> float:
        cap = min(self.backoff_cap, self.backoff_base * (2 ** (attempt - 1)))
        return cap / 2 + random.uniform(0, cap / 2)  # equal jitter


def _safe_params(params):
    if not params:
        return None
    return {k: (v if len(str(v)) < 400 else str(v)[:400] + "...") for k, v in params.items()}


def _err_message(resp) -> str:
    try:
        j = resp.json()
        if isinstance(j, dict):
            m = j.get("errorMessages") or j.get("errors") or j.get("message")
            return str(m)[:500]
    except Exception:
        pass
    return re.sub(r"\s+", " ", resp.text[:500])


# --------------------------------------------------------------------------- #
# Extrator
# --------------------------------------------------------------------------- #
class Extractor:
    def __init__(self, args):
        self.args = args
        self.out = args.out
        self.parts = os.path.join(self.out, "parts")
        self.state_dir = os.path.join(self.out, "state")
        for d in (self.out, self.parts, self.state_dir):
            os.makedirs(d, exist_ok=True)
        for k in ("issues", "changelog", "comments", "worklogs", "needs", "versions", "extras"):
            os.makedirs(os.path.join(self.parts, k), exist_ok=True)
        self.errors = ErrorLog(os.path.join(self.out, "errors.jsonl"))
        self.metrics = Metrics(os.path.join(self.out, "metrics.jsonl"))
        self.api = Api(args.base_url, args, self.errors, self.metrics, self.log)
        self.ckpt_path = os.path.join(self.state_dir, "checkpoint.json")
        self.state = self._load_state()
        self.state_lock = asyncio.Lock()
        self.since = args.since
        self.global_jql = (f'created >= "{self.since}" OR updated >= "{self.since}" '
                           f'OR resolution IS EMPTY')

    # ---------------- infra ----------------
    def log(self, msg: str) -> None:
        line = f"{utcnow()} {msg}"
        print(line, flush=True)
        with open(os.path.join(self.out, "run.log"), "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def _load_state(self) -> dict:
        if os.path.exists(self.ckpt_path):
            with open(self.ckpt_path, encoding="utf-8") as f:
                return json.load(f)
        return {"created": utcnow(), "runs": [], "plan": None, "units": {},
                "versions": {}, "extras": {}, "phases": {}}

    def save_state(self) -> None:
        atomic_write_json(self.ckpt_path, self.state)

    def p(self, *a) -> str:
        return os.path.join(self.out, *a)

    async def metrics_loop(self):
        while True:
            await asyncio.sleep(self.args.metrics_every)
            s = self.metrics.snapshot(self.api.limiter)
            self.log(f"[metrics] req={s['requests']} rec={s['records']} {s['mb']}MB "
                     f"req/s={s['req_per_s_window']} rec/s={s['records_per_s_window']} "
                     f"conc={s['concurrency_limit']} inflight={s['inflight']} "
                     f"timeouts={s['timeouts']} throttled={s['throttled']} st={s['statuses']}")

    # ---------------- etapa 1: inspeção ----------------
    async def inspect(self):
        self.log("[inspect] serverInfo / projetos / campos")
        st, info = await self.api.get_json(f"{API}/serverInfo", ctx={"phase": "inspect"})
        self.state["serverInfo"] = info
        st, projects = await self.api.get_json(
            f"{API}/project",
            {"expand": "description,lead,url,projectKeys,issueTypes", "includeArchived": "true"},
            ctx={"phase": "inspect"})
        if st != 200 or not isinstance(projects, list):
            raise SystemExit(f"Falha ao obter projetos (HTTP {st})")
        tmp = self.p("projects.jsonl.tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            for pr in projects:
                f.write(dumps(pr) + "\n")
        replace_with_retry(tmp, self.p("projects.jsonl"))
        st, fields = await self.api.get_json(f"{API}/field", ctx={"phase": "inspect"})
        if st != 200:
            raise SystemExit(f"Falha ao obter campos (HTTP {st})")
        catalog = {"extracted_at": utcnow(), "count": len(fields),
                   "custom_count": sum(1 for x in fields if x.get("custom")),
                   "relevant_custom_fields": classify_fields(fields), "fields": fields}
        atomic_write_json(self.p("fields.json"), catalog, indent=1)

        # sondagens de capacidade
        probes = {}
        st, d = await self.api.get_json(f"{API}/search", {"jql": self.global_jql, "maxResults": 0},
                                        ctx={"phase": "inspect"})
        probes["global_total"] = d.get("total") if d else None
        st, d = await self.api.get_json(f"{API}/search",
                                        {"jql": self.global_jql + " ORDER BY created ASC",
                                         "maxResults": 5000, "fields": "key"},
                                        ctx={"phase": "inspect"})
        probes["maxResults_requested_5000"] = {"status": st, "returned_maxResults": d.get("maxResults") if d else None,
                                              "issues_returned": len(d.get("issues", [])) if d else None}
        endpoints = {
            "agile_board": "/rest/agile/1.0/board?maxResults=1",
            "worklog_updated": f"{API}/worklog/updated?since=1577836800000",
            "issue_changelog_endpoint": f"{API}/issue/{projects[0]['key']}-1/changelog",
        }
        for name, url in endpoints.items():
            path, _, q = url.partition("?")
            params = dict(x.split("=", 1) for x in q.split("&")) if q else None
            st, _ = await self.api.get_json(path, params, ctx={"phase": "inspect", "probe": name})
            probes[name] = st
        self.state["probes"] = probes
        self.state["phases"]["inspect"] = {"done": True, "at": utcnow(), "projects": len(projects),
                                           "fields": len(fields)}
        self.save_state()
        self.log(f"[inspect] projetos={len(projects)} campos={len(fields)} probes={probes}")

    # ---------------- planejamento de janelas ----------------
    async def count(self, jql: str) -> int:
        st, d = await self.api.get_json(f"{API}/search", {"jql": jql, "maxResults": 0, "fields": "key"},
                                        ctx={"phase": "count"})
        if st != 200 or d is None:
            raise RuntimeError(f"count falhou HTTP {st}: {jql}")
        return int(d["total"])

    def window_jql(self, lo: str | None, hi: str | None) -> str:
        w = []
        if lo:
            w.append(f'created >= "{lo}"')
        if hi:
            w.append(f'created < "{hi}"')
        return f"({self.global_jql}) AND " + " AND ".join(w)

    async def plan(self):
        if self.state.get("plan"):
            self.log(f"[plan] reutilizando plano com {len(self.state['plan']['units'])} unidades")
            return
        self.log("[plan] calculando janelas disjuntas por created")
        global_total = await self.count(self.global_jql)
        this_year = dt.date.today().year
        bounds = [None] + [f"{y}-01-01 00:00" for y in range(2000, this_year + 2)] + [None]
        # garante fronteira exata em --since
        since_b = f"{self.since} 00:00"
        if since_b not in bounds:
            bounds.insert(-1, since_b)
            mid = sorted(b for b in bounds if b)
            bounds = [None] + mid + [None]
        ranges = list(zip(bounds[:-1], bounds[1:]))

        sem = asyncio.Semaphore(self.args.concurrency_max)
        units: list[dict] = []

        async def split(lo, hi):
            async with sem:
                n = await self.count(self.window_jql(lo, hi))
            if n > self.args.window_max and lo and hi:
                a = dt.datetime.strptime(lo, "%Y-%m-%d %H:%M")
                b = dt.datetime.strptime(hi, "%Y-%m-%d %H:%M")
                if (b - a) > dt.timedelta(minutes=2):
                    m = a + (b - a) / 2
                    m = m.replace(second=0, microsecond=0)
                    ms = m.strftime("%Y-%m-%d %H:%M")
                    await asyncio.gather(split(lo, ms), split(ms, hi))
                    return
            if n > 0 or hi is None:
                units.append({"lo": lo, "hi": hi, "planned": n})

        await asyncio.gather(*(split(lo, hi) for lo, hi in ranges))
        units.sort(key=lambda u: (u["lo"] or ""))
        for i, u in enumerate(units):
            u["id"] = f"u{i:04d}_" + re.sub(r"[^0-9]", "", u["lo"] or "min")[:12] + "_" + \
                      re.sub(r"[^0-9]", "", u["hi"] or "max")[:12]
            u["jql"] = self.window_jql(u["lo"], u["hi"]) + " ORDER BY created ASC, key ASC"
        planned = sum(u["planned"] for u in units)
        self.state["plan"] = {"at": utcnow(), "global_jql": self.global_jql, "global_total": global_total,
                              "sum_of_windows": planned, "window_max": self.args.window_max,
                              "units": units}
        self.save_state()
        self.log(f"[plan] {len(units)} unidades; soma janelas={planned} total global={global_total}")
        if planned != global_total:
            self.log("[plan] AVISO: soma das janelas difere do total global (dados mudando durante o plano?)")

    def selected_units(self) -> list[dict]:
        units = self.state["plan"]["units"]
        k = self.args.max_units
        if k and k < len(units):
            idx = sorted({round(i * (len(units) - 1) / (k - 1)) for i in range(k)}) if k > 1 else [0]
            units = [units[i] for i in idx]
        return units

    # ---------------- etapa 2: issues ----------------
    async def run_issues(self):
        units = self.selected_units()
        pending = [u for u in units if not self.state["units"].get(u["id"], {}).get("done")]
        self.log(f"[issues] {len(pending)}/{len(units)} unidades pendentes")
        q: asyncio.Queue = asyncio.Queue()
        for u in pending:
            q.put_nowait(u)

        async def worker():
            while True:
                try:
                    u = q.get_nowait()
                except asyncio.QueueEmpty:
                    return
                try:
                    await self.run_unit(u)
                except RetryExhausted as e:
                    self.log(f"[issues] unidade {u['id']} falhou: {e}")
                    st = self.state["units"].setdefault(u["id"], {})
                    st["failed"] = str(e)
                    async with self.state_lock:
                        self.save_state()

        await asyncio.gather(*(worker() for _ in range(self.args.concurrency_max)))

    async def run_unit(self, u: dict):
        uid = u["id"]
        st = self.state["units"].setdefault(uid, {
            "startAt": 0, "pages": 0, "issues_written": 0, "offsets": {},
            "page_size": self.args.max_results, "done": False})
        st.pop("failed", None)
        kinds = ("issues", "changelog", "comments", "worklogs", "needs")
        paths = {k: os.path.join(self.parts, k, f"{uid}.jsonl") for k in kinds}
        for k, pth in paths.items():  # descarta o que foi gravado após o último checkpoint
            truncate_to(pth, st["offsets"].get(k, 0))
        files = {k: open(pth, "ab") for k, pth in paths.items()}
        try:
            limit = self.args.limit
            while True:
                if limit and st["issues_written"] >= limit:
                    st["limited"] = True
                    break
                size = st["page_size"]
                if limit:
                    size = min(size, limit - st["issues_written"])
                params = {"jql": u["jql"], "startAt": st["startAt"], "maxResults": size,
                          "fields": "*all", "expand": "changelog"}
                try:
                    status, data = await self.api.get_json(
                        f"{API}/search", params, ctx={"phase": "issues", "unit": uid},
                        max_attempts=4 if st["page_size"] > self.args.min_page_size else None)
                except RetryExhausted:
                    if st["page_size"] > self.args.min_page_size:
                        st["page_size"] = max(self.args.min_page_size, st["page_size"] // 2)
                        self.log(f"[issues] {uid}: reduzindo página para {st['page_size']}")
                        continue
                    raise
                if status != 200 or data is None:
                    raise RetryExhausted(f"HTTP {status} permanente na unidade {uid}")
                issues = data.get("issues") or []
                total = int(data.get("total", 0))
                self._write_issue_page(files, issues, uid, st["startAt"], "search")
                for f in files.values():
                    f.flush()
                    os.fsync(f.fileno())
                st["offsets"] = {k: files[k].tell() for k in kinds}
                st["startAt"] += len(issues)
                st["issues_written"] += len(issues)
                st["pages"] += 1
                st["last_total"] = total
                st["returned_maxResults"] = data.get("maxResults")
                self.metrics.records += len(issues)
                async with self.state_lock:
                    self.save_state()
                if not issues or st["startAt"] >= total:
                    if not issues and st["startAt"] < total:
                        self.errors.log(endpoint=f"{API}/search", unit=uid, status=200,
                                        message=f"página vazia com startAt={st['startAt']} < total={total}",
                                        retried=False)
                    break
            if not st.get("limited"):
                await self.reconcile_unit(u, st, files)
            st["done"] = True
            st["done_at"] = utcnow()
            async with self.state_lock:
                self.save_state()
            self.log(f"[issues] {uid} ok: {st['issues_written']} registros, {st['pages']} páginas, "
                     f"esperado={st.get('final_total', st.get('last_total'))} únicos={st.get('unique_ids')}")
        finally:
            for f in files.values():
                f.close()

    def _write_issue_page(self, files, issues, uid, start_at, source):
        now = utcnow()
        for i, iss in enumerate(issues):
            occ = f"{uid}:{source}:{start_at}:{i}"
            iid, key = iss.get("id"), iss.get("key")
            fields = iss.get("fields") or {}
            needs = []
            cl = iss.pop("changelog", None)
            if cl is not None:
                hist = cl.pop("histories", []) or []
                cl["_obtained"] = len(hist)
                iss["changelog"] = cl
                for h in hist:
                    h.update(issue_id=iid, issue_key=key, _occ=occ, _source="search_expand_changelog")
                    files["changelog"].write((dumps(h) + "\n").encode("utf-8"))
                if int(cl.get("total", len(hist))) > len(hist):
                    needs.append("changelog")
            com = fields.get("comment")
            if isinstance(com, dict):
                cs = com.pop("comments", []) or []
                com["_obtained"] = len(cs)
                for c in cs:
                    c.update(issue_id=iid, issue_key=key, _occ=occ, _source="search_field_comment")
                    files["comments"].write((dumps(c) + "\n").encode("utf-8"))
                if int(com.get("total", len(cs))) > len(cs):
                    needs.append("comments")
            wl = fields.get("worklog")
            if isinstance(wl, dict):
                ws = wl.pop("worklogs", []) or []
                wl["_obtained"] = len(ws)
                for w in ws:
                    w.update(issue_id=iid, issue_key=key, _occ=occ, _source="search_field_worklog")
                    files["worklogs"].write((dumps(w) + "\n").encode("utf-8"))
                if int(wl.get("total", len(ws))) > len(ws):
                    needs.append("worklogs")
            iss["_occ"] = occ
            iss["_fetched_at"] = now
            files["issues"].write((dumps(iss) + "\n").encode("utf-8"))
            for n in needs:
                files["needs"].write((dumps({"issue_id": iid, "issue_key": key, "kind": n,
                                             "expected": (cl if n == "changelog" else
                                                          com if n == "comments" else wl).get("total"),
                                             "obtained_embedded": (cl if n == "changelog" else
                                                                   com if n == "comments" else wl).get("_obtained")})
                                       + "\n").encode("utf-8"))

    async def reconcile_unit(self, u, st, files):
        """Confere ids obtidos x ids na janela; busca faltantes por `id in (...)`."""
        uid = u["id"]
        ids = set()
        with open(os.path.join(self.parts, "issues", f"{uid}.jsonl"), "rb") as f:
            for line in f:
                m = re.search(rb'"id":"(\d+)"', line)
                if m:
                    ids.add(m.group(1).decode())
        final_total = await self.count(u["jql"].split(" ORDER BY")[0])
        st["final_total"] = final_total
        st["unique_ids"] = len(ids)
        st["duplicates_in_unit"] = st["issues_written"] - len(ids)
        if len(ids) == final_total:
            st["reconciled"] = "match"
            return
        self.log(f"[reconcile] {uid}: únicos={len(ids)} total={final_total}; listando chaves")
        window_ids, start = {}, 0
        while True:
            status, d = await self.api.get_json(
                f"{API}/search", {"jql": u["jql"], "startAt": start, "maxResults": 1000, "fields": "key"},
                ctx={"phase": "reconcile", "unit": uid})
            if status != 200 or not d:
                raise RetryExhausted(f"reconcile HTTP {status}")
            for it in d.get("issues", []):
                window_ids[it["id"]] = it["key"]
            start += len(d.get("issues", []))
            if not d.get("issues") or start >= d["total"]:
                break
        missing = [i for i in window_ids if i not in ids]
        st["reconcile_missing"] = len(missing)
        st["reconcile_not_in_window_now"] = len(ids - set(window_ids))
        for b in range(0, len(missing), 50):
            batch = missing[b:b + 50]
            status, d = await self.api.get_json(
                f"{API}/search", {"jql": f"id in ({','.join(batch)})", "maxResults": 50,
                                  "fields": "*all", "expand": "changelog"},
                ctx={"phase": "reconcile", "unit": uid})
            if status != 200 or not d:
                raise RetryExhausted(f"reconcile fetch HTTP {status}")
            self._write_issue_page(files, d.get("issues", []), uid, b, "reconcile")
            st["issues_written"] += len(d.get("issues", []))
            for f in files.values():
                f.flush()
                os.fsync(f.fileno())
            st["offsets"] = {k: files[k].tell() for k in files}
            async with self.state_lock:
                self.save_state()
        st["unique_ids"] = len(ids | set(missing))
        st["reconciled"] = "fetched_missing"

    # ---------------- etapa 3: dados por issue ----------------
    async def run_extras(self):
        needs = {}
        for pth in sorted(glob.glob(os.path.join(self.parts, "needs", "*.jsonl"))):
            for r in iter_jsonl(pth):
                needs[(r["issue_id"], r["kind"])] = r
        done_path = os.path.join(self.parts, "extras", "done.jsonl")
        truncate_to_last_newline(done_path)
        done = set()
        if os.path.exists(done_path):
            for r in iter_jsonl(done_path):
                done.add((r["issue_id"], r["kind"]))
        todo = [r for k, r in needs.items() if k not in done]
        self.log(f"[extras] necessidades={len(needs)} já feitas={len(done & set(needs))} pendentes={len(todo)}")
        out = {}
        for k in ("changelog", "comments", "worklogs"):
            pth = os.path.join(self.parts, "extras", f"{k}.jsonl")
            truncate_to_last_newline(pth)
            out[k] = open(pth, "a", encoding="utf-8")
        donef = open(done_path, "a", encoding="utf-8")
        q: asyncio.Queue = asyncio.Queue()
        for r in todo:
            q.put_nowait(r)

        async def worker():
            while True:
                try:
                    r = q.get_nowait()
                except asyncio.QueueEmpty:
                    return
                try:
                    res = await self.fetch_extra(r)
                except RetryExhausted as e:
                    self.errors.log(endpoint="extras", issue_key=r["issue_key"], kind=r["kind"],
                                    status=None, message=str(e), retried=True, final=True)
                    continue
                token = f"x:{r['kind']}:{r['issue_id']}:{utcnow()}"
                for rec in res["records"]:
                    rec.update(issue_id=r["issue_id"], issue_key=r["issue_key"], _fetch=token,
                               _source=res["source"])
                    out[r["kind"]].write(dumps(rec) + "\n")
                out[r["kind"]].flush()
                donef.write(dumps({"issue_id": r["issue_id"], "issue_key": r["issue_key"], "kind": r["kind"],
                                   "token": token, "status": res["status"], "expected": res["expected"],
                                   "obtained": len(res["records"]), "complete": res["complete"],
                                   "at": utcnow()}) + "\n")
                donef.flush()
                self.metrics.records += len(res["records"])

        try:
            await asyncio.gather(*(worker() for _ in range(self.args.concurrency_max)))
        finally:
            for f in out.values():
                f.close()
            donef.close()

    async def fetch_extra(self, r) -> dict:
        iid, kind = r["issue_id"], r["kind"]
        ctx = {"phase": "extras", "issue_key": r["issue_key"], "kind": kind}
        if kind == "changelog":
            st, d = await self.api.get_json(f"{API}/issue/{iid}", {"expand": "changelog", "fields": "key"}, ctx=ctx)
            if st != 200 or not d:
                return {"records": [], "status": st, "expected": r.get("expected"), "complete": False,
                        "source": "issue_expand_changelog"}
            cl = d.get("changelog") or {}
            hist = cl.get("histories") or []
            exp = cl.get("total", len(hist))
            if exp > len(hist):
                self.errors.log(endpoint=f"{API}/issue/{{id}}", issue_key=r["issue_key"], status=200,
                                message=f"changelog truncado: {len(hist)}/{exp}", retried=False)
            return {"records": hist, "status": st, "expected": exp, "complete": exp <= len(hist),
                    "source": "issue_expand_changelog"}
        path = f"{API}/issue/{iid}/" + ("comment" if kind == "comments" else "worklog")
        key = "comments" if kind == "comments" else "worklogs"
        recs, start, exp, st = [], 0, None, None
        while True:
            st, d = await self.api.get_json(path, {"startAt": start, "maxResults": 1000}, ctx=ctx)
            if st != 200 or not d:
                break
            items = d.get(key) or []
            exp = d.get("total", len(items))
            recs.extend(items)
            start += len(items)
            if not items or start >= exp:
                break
        return {"records": recs, "status": st, "expected": exp,
                "complete": st == 200 and exp is not None and len(recs) >= exp,
                "source": f"issue_{key}_endpoint"}

    # ---------------- versões e boards ----------------
    async def run_versions(self):
        projects = list(iter_jsonl(self.p("projects.jsonl")))
        if self.args.projects_limit:
            step = max(1, len(projects) // self.args.projects_limit)
            projects = projects[::step][: self.args.projects_limit]
        vs = self.state.setdefault("versions", {})
        todo = [p for p in projects if not vs.get(p["key"], {}).get("done")]
        self.log(f"[versions] {len(todo)}/{len(projects)} projetos pendentes")
        sem = asyncio.Semaphore(self.args.concurrency_max)

        async def one(pr):
            async with sem:
                key, recs, start = pr["key"], [], 0
                while True:
                    try:
                        st, d = await self.api.get_json(
                            f"{API}/project/{key}/version", {"startAt": start, "maxResults": 100},
                            ctx={"phase": "versions", "project": key})
                    except RetryExhausted as e:
                        vs[key] = {"done": False, "error": str(e)}
                        return
                    if st != 200 or not d:
                        vs[key] = {"done": True, "status": st, "count": 0}
                        return
                    for v in d.get("values", []):
                        v.update(project_key=key, project_id=pr["id"])
                        recs.append(v)
                    start += len(d.get("values", []))
                    if d.get("isLast", True) or not d.get("values"):
                        break
                pth = os.path.join(self.parts, "versions", f"{key}.jsonl")
                with open(pth + ".tmp", "w", encoding="utf-8") as f:
                    for v in recs:
                        f.write(dumps(v) + "\n")
                replace_with_retry(pth + ".tmp", pth)
                vs[key] = {"done": True, "status": 200, "count": len(recs)}
                self.metrics.records += len(recs)
                async with self.state_lock:
                    self.save_state()

        await asyncio.gather(*(one(p) for p in todo))
        self.save_state()

    async def run_boards(self):
        st, d = await self.api.get_json("/rest/agile/1.0/board", {"maxResults": 50},
                                        ctx={"phase": "boards"})
        self.state["boards_api"] = {"status": st, "available": st == 200, "at": utcnow()}
        if st == 200 and d:
            recs, start = list(d.get("values", [])), len(d.get("values", []))
            while not d.get("isLast", True):
                st, d = await self.api.get_json("/rest/agile/1.0/board", {"startAt": start, "maxResults": 50},
                                                ctx={"phase": "boards"})
                if st != 200 or not d:
                    break
                recs += d.get("values", [])
                start += len(d.get("values", []))
            with open(os.path.join(self.parts, "boards_api.jsonl"), "w", encoding="utf-8") as f:
                for b in recs:
                    f.write(dumps(b) + "\n")
        else:
            self.log(f"[boards] Agile API indisponível para acesso anônimo (HTTP {st}); "
                     f"sprints serão derivados somente do campo Sprint dos issues")
        self.save_state()

    # ---------------- etapa 4: consolidação ----------------
    def merge(self):
        self.log("[merge] consolidando arquivos finais")
        sprint_fields = self._sprint_field_ids()
        issue_files = sorted(glob.glob(os.path.join(self.parts, "issues", "*.jsonl")))
        winners: dict[str, tuple] = {}  # id -> (updated, file_idx, offset, occ, key)
        lines = 0
        for fi, pth in enumerate(issue_files):
            with open(pth, "rb") as f:
                off = 0
                for line in f:
                    if line.strip():
                        lines += 1
                        r = json.loads(line)
                        upd = (r.get("fields") or {}).get("updated") or ""
                        cur = winners.get(r["id"])
                        if cur is None or (upd, r.get("_fetched_at", "")) >= (cur[0], cur[5]):
                            winners[r["id"]] = (upd, fi, off, r["_occ"], r["key"], r.get("_fetched_at", ""))
                    off += len(line)
        win_offsets = {(w[1], w[2]) for w in winners.values()}
        win_occ = {w[3] for w in winners.values()}
        id2key = {i: w[4] for i, w in winners.items()}
        dup = lines - len(winners)

        # extras: último token por (issue, kind)
        extra_tok: dict[tuple, str] = {}
        extra_status = {"changelog": {}, "comments": {}, "worklogs": {}}
        done_path = os.path.join(self.parts, "extras", "done.jsonl")
        if os.path.exists(done_path):
            for r in iter_jsonl(done_path):
                if r.get("status") == 200:
                    extra_tok[(r["issue_id"], r["kind"])] = r["token"]
                extra_status[r["kind"]][r["issue_id"]] = r

        sprints, boards, issue_sprints = {}, {}, 0
        n_issues = 0
        tmp_issues = self.p("issues.jsonl.tmp")
        tmp_iv = self.p("issue_versions.jsonl.tmp")
        tmp_is = self.p("issue_sprints.jsonl.tmp")
        with open(tmp_issues, "wb") as fo, open(tmp_iv, "w", encoding="utf-8") as fiv, \
                open(tmp_is, "w", encoding="utf-8") as fis:
            for fi, pth in enumerate(issue_files):
                with open(pth, "rb") as f:
                    off = 0
                    for line in f:
                        if (fi, off) in win_offsets:
                            fo.write(line if line.endswith(b"\n") else line + b"\n")
                            n_issues += 1
                            r = json.loads(line)
                            fl = r.get("fields") or {}
                            for rel in ("fixVersions", "versions"):
                                for v in fl.get(rel) or []:
                                    fiv.write(dumps({"issue_id": r["id"], "issue_key": r["key"],
                                                     "project_key": (fl.get("project") or {}).get("key"),
                                                     "relation": rel, "version_id": v.get("id"),
                                                     "version_name": v.get("name"),
                                                     "released": v.get("released"),
                                                     "releaseDate": v.get("releaseDate")}) + "\n")
                            for sf in sprint_fields:
                                for raw in fl.get(sf) or []:
                                    sp = parse_sprint(raw)
                                    sid = sp.get("id")
                                    fis.write(dumps({"issue_id": r["id"], "issue_key": r["key"],
                                                     "project_key": (fl.get("project") or {}).get("key"),
                                                     "sprint_id": sid, "sprint_name": sp.get("name"),
                                                     "sprint_state": sp.get("state"),
                                                     "board_id": sp.get("rapidViewId"),
                                                     "field": sf}) + "\n")
                                    issue_sprints += 1
                                    if sid and sid not in sprints:
                                        sprints[sid] = {**sp, "_raw": raw if isinstance(raw, str) else None,
                                                        "_source": f"derivado do campo {sf} dos issues"}
                                    if sp.get("rapidViewId"):
                                        b = boards.setdefault(sp["rapidViewId"], {
                                            "id": sp["rapidViewId"], "projects": set(),
                                            "_source": "derivado (rapidViewId) do campo Sprint; Agile API indisponível"})
                                        b["projects"].add((fl.get("project") or {}).get("key"))
                        off += len(line)
        replace_with_retry(tmp_issues, self.p("issues.jsonl"))
        replace_with_retry(tmp_iv, self.p("issue_versions.jsonl"))
        replace_with_retry(tmp_is, self.p("issue_sprints.jsonl"))

        child_counts = {}
        for kind, fname in (("changelog", "changelog.jsonl"), ("comments", "comments.jsonl"),
                            ("worklogs", "worklogs.jsonl")):
            tmp = self.p(fname + ".tmp")
            n = 0
            with open(tmp, "w", encoding="utf-8") as fo:
                for pth in sorted(glob.glob(os.path.join(self.parts, kind, "*.jsonl"))):
                    for r in iter_jsonl(pth):
                        if r["_occ"] in win_occ and (r["issue_id"], kind) not in extra_tok:
                            r["issue_key"] = id2key.get(r["issue_id"], r["issue_key"])
                            fo.write(dumps(r) + "\n")
                            n += 1
                xp = os.path.join(self.parts, "extras", f"{kind}.jsonl")
                if os.path.exists(xp):
                    for r in iter_jsonl(xp):
                        if extra_tok.get((r["issue_id"], kind)) == r["_fetch"] and r["issue_id"] in winners:
                            r["issue_key"] = id2key.get(r["issue_id"], r["issue_key"])
                            fo.write(dumps(r) + "\n")
                            n += 1
            replace_with_retry(tmp, self.p(fname))
            child_counts[kind] = n

        nv = 0
        tmp = self.p("versions.jsonl.tmp")
        with open(tmp, "w", encoding="utf-8") as fo:
            for pth in sorted(glob.glob(os.path.join(self.parts, "versions", "*.jsonl"))):
                with open(pth, encoding="utf-8") as f:
                    for line in f:
                        fo.write(line)
                        nv += 1
        replace_with_retry(tmp, self.p("versions.jsonl"))

        with open(self.p("sprints.jsonl.tmp"), "w", encoding="utf-8") as fo:
            for s in sprints.values():
                fo.write(dumps(s) + "\n")
        replace_with_retry(self.p("sprints.jsonl.tmp"), self.p("sprints.jsonl"))
        with open(self.p("boards.jsonl.tmp"), "w", encoding="utf-8") as fo:
            api_boards = os.path.join(self.parts, "boards_api.jsonl")
            if os.path.exists(api_boards):
                with open(api_boards, encoding="utf-8") as f:
                    fo.writelines(f)
            for b in boards.values():
                b["projects"] = sorted(x for x in b["projects"] if x)
                fo.write(dumps(b) + "\n")
        replace_with_retry(self.p("boards.jsonl.tmp"), self.p("boards.jsonl"))

        # pendências de dados associados
        needs = {}
        for pth in glob.glob(os.path.join(self.parts, "needs", "*.jsonl")):
            for r in iter_jsonl(pth):
                if r["issue_id"] in winners:
                    needs[(r["issue_id"], r["kind"])] = r
        missing_assoc = {"changelog": 0, "comments": 0, "worklogs": 0}
        incomplete_assoc = {"changelog": 0, "comments": 0, "worklogs": 0}
        for (iid, kind) in needs:
            s = extra_status[kind].get(iid)
            if not s or s.get("status") != 200:
                missing_assoc[kind] += 1
            elif not s.get("complete"):
                incomplete_assoc[kind] += 1

        self.state["merge"] = {
            "at": utcnow(), "issue_lines_in_parts": lines, "unique_issues": n_issues,
            "duplicate_issue_records_removed": dup, "changelog_histories": child_counts["changelog"],
            "comments": child_counts["comments"], "worklogs": child_counts["worklogs"],
            "versions": nv, "sprints_derived": len(sprints), "boards_derived": len(boards),
            "issue_sprint_links": issue_sprints,
            "associated_needs_total": len(needs),
            "associated_missing": missing_assoc, "associated_incomplete": incomplete_assoc,
        }
        self.save_state()
        self.log(f"[merge] {self.state['merge']}")

    def _sprint_field_ids(self) -> list[str]:
        try:
            with open(self.p("fields.json"), encoding="utf-8") as f:
                cat = json.load(f)
            return [x["id"] for x in cat["fields"]
                    if (x.get("schema") or {}).get("custom") == "com.pyxis.greenhopper.jira:gh-sprint"]
        except Exception:
            return []

    # ---------------- manifesto ----------------
    async def write_manifest(self, final_check: bool):
        plan = self.state.get("plan") or {}
        units = self.selected_units() if plan else []
        ust = self.state["units"]
        done_units = [u for u in units if ust.get(u["id"], {}).get("done")]
        failed_units = [u["id"] for u in units if ust.get(u["id"], {}).get("failed")]
        vs = self.state.get("versions", {})
        global_now = None
        if final_check:
            try:
                global_now = await self.count(self.global_jql)
            except Exception as e:
                global_now = f"erro: {e}"
        merge = self.state.get("merge", {})
        complete = (bool(units) and len(done_units) == len(units) and not failed_units
                    and not self.args.limit and not self.args.max_units
                    and all(v.get("done") for v in vs.values())
                    and not any((merge.get("associated_missing") or {}).values()))
        man = {
            "extraction_started_utc": self.state.get("created"),
            "manifest_written_utc": utcnow(),
            "base_url": self.args.base_url,
            "server_info": self.state.get("serverInfo"),
            "api": {"rest": "/rest/api/2", "agile": "/rest/agile/1.0",
                    "docs": "https://developer.atlassian.com/server/jira/platform/rest/v11002/"},
            "global_jql": self.global_jql,
            "parameters": {k: v for k, v in vars(self.args).items()},
            "probes": self.state.get("probes"),
            "plan": {k: v for k, v in plan.items() if k != "units"},
            "units_total": len(units), "units_done": len(done_units), "units_failed": failed_units,
            "pages_fetched": sum(ust.get(u["id"], {}).get("pages", 0) for u in units),
            "units": [{**{k: u[k] for k in ("id", "lo", "hi", "planned")},
                       **{k: v for k, v in ust.get(u["id"], {}).items() if k != "offsets"}} for u in units],
            "global_total_at_end": global_now,
            "versions_projects": {"total": len(vs), "done": sum(1 for v in vs.values() if v.get("done")),
                                  "non_200": {k: v.get("status") for k, v in vs.items() if v.get("status") != 200}},
            "boards_api": self.state.get("boards_api"),
            "merge": merge,
            "errors_logged_this_run": self.errors.count,
            "throughput_history_file": "metrics.jsonl",
            "concurrency_changes": self.api.limiter.changes[-200:],
            "completion": "complete" if complete else ("pilot/limited" if (self.args.limit or self.args.max_units)
                                                       else "incomplete"),
        }
        atomic_write_json(self.p("manifest.json"), man, indent=1)
        self.log(f"[manifest] status={man['completion']} unidades={len(done_units)}/{len(units)} "
                 f"total_global_agora={global_now}")

    # ---------------- orquestração ----------------
    async def run(self):
        phases = set(self.args.phases.split(","))
        run_rec = {"started": utcnow(), "argv": sys.argv[1:]}
        self.state["runs"].append(run_rec)
        mt = asyncio.create_task(self.metrics_loop())
        try:
            if "inspect" in phases and not (self.state["phases"].get("inspect", {}).get("done")
                                            and os.path.exists(self.p("fields.json"))):
                await self.inspect()
            if "plan" in phases or "issues" in phases:
                await self.plan()
            if self.args.dry_run:
                plan = self.state["plan"]
                self.log(f"[dry-run] {len(plan['units'])} unidades; total={plan['global_total']}; "
                         f"maiores: {sorted((u['planned'] for u in plan['units']), reverse=True)[:5]}")
                await self.write_manifest(False)
                return
            if "issues" in phases:
                await self.run_issues()
            if "extras" in phases:
                await self.run_extras()
            if "versions" in phases:
                await self.run_versions()
            if "boards" in phases:
                await self.run_boards()
            if "merge" in phases:
                await asyncio.to_thread(self.merge)
            await self.write_manifest("merge" in phases)
        finally:
            mt.cancel()
            s = self.metrics.snapshot(self.api.limiter)
            run_rec.update(ended=utcnow(), requests=s["requests"], records=s["records"],
                           elapsed_s=s["elapsed_s"], req_per_s=s["req_per_s_total"],
                           statuses=s["statuses"], timeouts=s["timeouts"], throttled=s["throttled"])
            self.save_state()
            await self.api.close()
            self.log(f"[fim] {run_rec}")


# --------------------------------------------------------------------------- #
# Helpers de domínio
# --------------------------------------------------------------------------- #
_SPRINT_RE = re.compile(r"\[(.*)\]\s*$", re.S)


def parse_sprint(raw) -> dict:
    """Interpreta o toString legado do GreenHopper (`...Sprint@x[id=1,name=..,state=..]`)
    ou um objeto JSON; não infere nada que não esteja no valor."""
    if isinstance(raw, dict):
        return {k: raw.get(k) for k in ("id", "name", "state", "rapidViewId", "boardId", "startDate",
                                        "endDate", "completeDate", "activatedDate", "goal", "sequence")}
    if not isinstance(raw, str):
        return {}
    m = _SPRINT_RE.search(raw)
    if not m:
        return {}
    out = {}
    # nomes podem conter vírgulas: separa somente antes de "chave="
    for part in re.split(r",(?=[A-Za-z]+=)", m.group(1)):
        k, _, v = part.partition("=")
        out[k] = None if v == "<null>" else v
    for k in ("id", "rapidViewId", "sequence"):
        if out.get(k) and str(out[k]).isdigit():
            out[k] = int(out[k])
    return out


FIELD_PATTERNS = {
    "estimativa/story_points": r"story ?point|estimat|complexity|effort|original story",
    "causa_raiz": r"root ?cause|cause|bug category|bug behavior",
    "ambiente/producao": r"environment|production|o/s|jdk|browser|platform",
    "versao": r"version|release|since",
    "sprint/agile": r"sprint|epic|rank|team",
    "severidade/criticidade": r"severity|critical|criticality|impact|priority|regression|flag",
    "datas_planejadas": r"date|due|deadline|start",
    "qa/teste": r"test|qa|review",
    "pessoas": r"tester|reviewer|mentor|contributor|shepherd",
}


def classify_fields(fields: list[dict]) -> dict:
    out = {k: [] for k in FIELD_PATTERNS}
    for f in fields:
        name = f.get("name") or ""
        for cat, pat in FIELD_PATTERNS.items():
            if f.get("custom") and re.search(pat, name, re.I):
                out[cat].append({"id": f["id"], "name": name,
                                 "type": (f.get("schema") or {}).get("type"),
                                 "custom": (f.get("schema") or {}).get("custom")})
    # campos padrão relevantes
    out["padrao_relevantes"] = [f["id"] for f in fields if not f.get("custom") and f["id"] in {
        "environment", "duedate", "priority", "resolution", "resolutiondate", "fixVersions", "versions",
        "timeoriginalestimate", "timeestimate", "timespent", "aggregatetimespent", "worklog", "labels",
        "components", "issuelinks", "parent", "subtasks"}]
    return out


def build_args(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base-url", default=DEFAULT_BASE)
    ap.add_argument("--out", default=os.environ.get("ALINE_JIRA_DATA_DIR", os.path.join("data", "apache_jira")), help="pasta de saída")
    ap.add_argument("--since", default="2020-01-01", help="data inicial (AAAA-MM-DD)")
    ap.add_argument("--max-results", type=int, default=1000, help="maxResults da busca")
    ap.add_argument("--min-page-size", type=int, default=100)
    ap.add_argument("--window-max", type=int, default=20000, help="máx. issues por unidade (janela)")
    ap.add_argument("--concurrency-start", type=int, default=4)
    ap.add_argument("--concurrency-max", type=int, default=8)
    ap.add_argument("--ramp-every", type=int, default=30, help="sucessos seguidos para +1 de concorrência")
    ap.add_argument("--max-rps", type=float, default=8.0, help="máx. início de requisições por segundo")
    ap.add_argument("--connect-timeout", type=float, default=20.0)
    ap.add_argument("--read-timeout", type=float, default=180.0)
    ap.add_argument("--max-attempts", type=int, default=8)
    ap.add_argument("--backoff-base", type=float, default=2.0)
    ap.add_argument("--backoff-cap", type=float, default=120.0)
    ap.add_argument("--limit", type=int, default=0, help="máx. issues por unidade (teste/piloto)")
    ap.add_argument("--max-units", type=int, default=0, help="usa K unidades espaçadas (piloto)")
    ap.add_argument("--projects-limit", type=int, default=0, help="limita projetos em versões (piloto)")
    ap.add_argument("--phases", default="inspect,plan,issues,extras,versions,boards,merge")
    ap.add_argument("--dry-run", action="store_true", help="só inspeção + plano, sem baixar issues")
    ap.add_argument("--metrics-every", type=float, default=30.0)
    return ap.parse_args(argv)


def main():
    args = build_args()
    ex = Extractor(args)
    try:
        asyncio.run(ex.run())
    except KeyboardInterrupt:
        print("Interrompido; execute novamente o mesmo comando para retomar pelo checkpoint.", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
