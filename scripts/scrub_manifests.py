#!/usr/bin/env python3
"""Scrub per-recording window manifests for public release on Hugging Face.

What it does (metadata only; window ``.npz`` files are never touched):

* rewrites absolute/private paths to portable references:
  - ``npz_path`` -> config-relative ``windows/<file>.npz`` (the file name on the Hub)
  - raw-source paths (``psg_path``, ``hypno_path``, ``bdf``, ``events``, ``log_file``,
    ``per_task_bdf[].bdf``) -> upstream-relative paths (e.g. ``sub-001/ses-01/eeg/...``)
    or are dropped when a ``*_file`` name already carries the same information
* adds ``license_spdx`` (SPDX id of the upstream source), ``source_url`` (upstream landing
  page or file URL) and ``source_dataset`` to every manifest
* removes encoder entries (e.g. CBraMod) from the data ``license_attribution`` block:
  encoders are not data sources of these windows
* keeps ``npz_sha256`` unchanged and (optionally) verifies it against the Hub LFS oid

Usage (stdlib only; run with ``uv run python``)::

    uv run python scripts/scrub_manifests.py --in hf_snapshot/ --out hf_scrubbed/ \
        [--lfs-oids oids.json]

``--in`` is a local copy of the dataset repo (config folders at top level). Only
``<config>/windows/*_manifest.json`` files are read; output mirrors the same layout.
The script exits non-zero if any private path pattern survives.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PRIVATE_PATTERNS = [
    re.compile(p)
    for p in (
        r"/workspace",
        r"/tmp/kaggle",
        r"/kaggle/",
        r"muse-eeg-heads-cache",
        r"/home/",
        r"/root/",
        r"kaggle_datasets",
        r"exports/windows",
    )
]

# Upstream sources: SPDX id, landing page, optional per-file URL builder.
SOURCES = {
    "sleep_edf": {
        "name": "Sleep-EDF Database Expanded v1.0.0 (PhysioNet)",
        "license_spdx": "ODC-By-1.0",
        "landing": "https://physionet.org/content/sleep-edfx/1.0.0/",
    },
    "hmc": {
        "name": "HMC Sleep Staging Database v1.1 (PhysioNet)",
        "license_spdx": "CC-BY-4.0",
        "landing": "https://physionet.org/content/hmc-sleep-staging/1.1/",
    },
    "ds001787": {
        "name": "OpenNeuro ds001787 v1.1.1 (EEG meditation study)",
        "license_spdx": "CC0-1.0",
        "landing": "https://openneuro.org/datasets/ds001787/versions/1.1.1",
    },
    "ds003969": {
        "name": "OpenNeuro ds003969 v1.0.0 (Meditation vs thinking task)",
        "license_spdx": "CC0-1.0",
        "landing": "https://openneuro.org/datasets/ds003969/versions/1.0.0",
    },
    "ds007169": {
        "name": "OpenNeuro ds007169 (Multimodal Cognitive Workload n-back)",
        "license_spdx": "CC0-1.0",
        "landing": "https://openneuro.org/datasets/ds007169",
    },
    "ds007262": {
        "name": "OpenNeuro ds007262 (Cognitive Workload 8-level arithmetic)",
        "license_spdx": "CC0-1.0",
        "landing": "https://openneuro.org/datasets/ds007262",
    },
    "ds007554": {
        "name": "OpenNeuro ds007554 (CMx7-MM cognitive-motor)",
        "license_spdx": "CC0-1.0",
        "landing": "https://openneuro.org/datasets/ds007554",
    },
    "eegmat": {
        "name": "EEG During Mental Arithmetic Tasks v1.0.0 (PhysioNet eegmat)",
        "license_spdx": "ODC-By-1.0",
        "landing": "https://physionet.org/content/eegmat/1.0.0/",
    },
    "stew": {
        "name": "STEW, processed MONSTER mirror (monster-monash/STEW on Hugging Face)",
        "license_spdx": "CC-BY-4.0",
        "landing": "https://huggingface.co/datasets/monster-monash/STEW",
    },
}

ENCODER_KEYS = {"cbramod", "reve", "labram"}


def detect_source(m: dict) -> str:
    for key in ("source", "dataset"):
        v = m.get(key)
        if isinstance(v, str) and v.lower() in SOURCES:
            return v.lower()
    psg = str(m.get("psg_file") or "")
    if psg.startswith(("SC4", "ST7")):
        return "sleep_edf"
    if psg.startswith("SN"):
        return "hmc"
    doi = str(m.get("doi") or "")
    for k in ("ds001787", "ds003969"):
        if k in doi:
            return k
    raise ValueError(f"cannot detect source for manifest keys={sorted(m)[:8]}")


def upstream_rel(path: str) -> str:
    """Map a private absolute path to an upstream-relative path."""
    p = path.replace("\\", "/")
    for marker in ("/raw/",):
        if marker in p:
            return p.split(marker, 1)[1]
    m = re.search(r"/data/[^/]+/(.+)$", p)
    if m:
        return m.group(1)
    return p.rsplit("/", 1)[-1]


def scrub_value(v):
    if isinstance(v, str):
        if any(rx.search(v) for rx in PRIVATE_PATTERNS) or v.startswith("/"):
            return upstream_rel(v)
        return v
    if isinstance(v, list):
        return [scrub_value(x) for x in v]
    if isinstance(v, dict):
        return {k: scrub_value(x) for k, x in v.items()}
    return v


def source_url(src: str, m: dict) -> str:
    psg = m.get("psg_file")
    if src == "sleep_edf" and psg:
        sub = "sleep-telemetry" if psg.startswith("ST7") else "sleep-cassette"
        return f"https://physionet.org/content/sleep-edfx/1.0.0/{sub}/{psg}"
    if src == "hmc" and psg:
        return f"https://physionet.org/content/hmc-sleep-staging/1.1/recordings/{psg}"
    return SOURCES[src]["landing"]


def scrub_manifest(m: dict, npz_name: str) -> dict:
    src = detect_source(m)
    out = {}
    for k, v in m.items():
        if k in ("psg_path", "hypno_path"):
            continue  # psg_file / hypno_file keep the upstream file name
        if k == "npz_path":
            out[k] = f"windows/{npz_name}"
            continue
        if k == "muse4_windows_ref" and isinstance(v, str):
            out[k] = "windows/" + v.rsplit("/", 1)[-1]
            continue
        if k == "license_attribution" and isinstance(v, dict):
            out[k] = {
                name: text
                for name, text in v.items()
                if name.lower() not in ENCODER_KEYS
            }
            continue
        out[k] = scrub_value(v)
    info = SOURCES[src]
    out["source_dataset"] = info["name"]
    out["license_spdx"] = m.get("license_spdx") or info["license_spdx"]
    if out["license_spdx"] != info["license_spdx"]:
        raise ValueError(f"license mismatch for {src}: {out['license_spdx']}")
    out["source_url"] = source_url(src, m)
    out["source_landing_page"] = info["landing"]
    out["manifest_scrubbed"] = "paths made portable; encoder entries removed from data license block"
    return out


def check_clean(text: str) -> list[str]:
    return [rx.pattern for rx in PRIVATE_PATTERNS if rx.search(text)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--in", dest="inp", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--lfs-oids", type=Path, help="JSON {repo_path: sha256} to verify npz_sha256")
    args = ap.parse_args()
    oids = json.loads(args.lfs_oids.read_text()) if args.lfs_oids else None

    n = bad = 0
    for mf in sorted(args.inp.glob("*/windows/*_manifest.json")):
        cfg = mf.parent.parent.name
        stem = mf.name[: -len("_manifest.json")]
        npz_name = f"{stem}_windows.npz"
        m = json.loads(mf.read_text())
        s = scrub_manifest(m, npz_name)
        text = json.dumps(s, indent=2, ensure_ascii=False) + "\n"
        leaks = check_clean(text)
        if leaks:
            print(f"LEAK {cfg}/{mf.name}: {leaks}", file=sys.stderr)
            bad += 1
        if s.get("npz_sha256") != m.get("npz_sha256"):
            print(f"SHA CHANGED {cfg}/{mf.name}", file=sys.stderr)
            bad += 1
        if oids is not None:
            key = f"{cfg}/windows/{npz_name}"
            if oids.get(key) != m.get("npz_sha256"):
                print(f"SHA != Hub LFS oid for {key}", file=sys.stderr)
                bad += 1
        dst = args.out / cfg / "windows" / mf.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text)
        n += 1
    print(f"scrubbed {n} manifests; problems={bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
