# -*- coding: utf-8 -*-
"""Fetch the four public archives that the adjudication scripts need.

None of these are redistributed in this repository: together they are about
430 MB, they already carry their own DOIs, and three of the four are Git
repositories that must be pinned to a commit to be reproducible.

    python reproduce/fetch_data.py              # everything
    python reproduce/fetch_data.py --only sung  # one dataset
    python reproduce/fetch_data.py --list       # sources only, no download

Downloads land in data_external/external/<Name>/ (or $CELL_EXTERNAL_DATA).
Each dataset gets a .fetched marker holding the source and date, so re-running
is cheap and every directory states where it came from.
"""
import argparse
import io
import json
import os
import shutil
import sys
import time
import urllib.request
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEST = Path(os.environ.get("CELL_EXTERNAL_DATA", REPO / "data_external" / "external"))

ZENODO = {
    "hansen": dict(name="HansenZechner2021", record="2755026",
                   title="Hansen & Zechner 2021, Msn2 promoter raw data",
                   doi="10.5281/zenodo.2755026", used_by="code44, code44b"),
    "chavez": dict(name="ChavezAbiega2022", record="5836623",
                   title="Chavez-Abiega et al. 2022, ERK/Akt KTR imaging",
                   doi="10.5281/zenodo.5836623", used_by="code46"),
}

GITHUB = {
    "sung": dict(name="Sung2022", repo="tay-lab/Spatial_NF-kB_Signaling", ref="main",
                 note="commit cb3e057 as used in the adjudication",
                 doi="10.1016/j.celrep.2022.111159", used_by="code45"),
    "nikolic": dict(name="Nikolic2024", repo="mnikolic7/Scale-invariance-in-early-embryonic-development",
                    ref="main", note="per-embryo Bicoid profiles",
                    doi="10.1073/pnas.2403265121", used_by="p9_bcd_anchor_audit.py"),
}


def _get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "scale-free-framework/reproduce"})
    return urllib.request.urlopen(req, timeout=timeout)


def fetch_zenodo(key, meta):
    out = DEST / meta["name"]
    if (out / ".fetched").exists():
        print(f"  {meta['name']}: already present")
        return
    out.mkdir(parents=True, exist_ok=True)
    with _get(f"https://zenodo.org/api/records/{meta['record']}") as r:
        rec = json.load(r)
    for f in rec.get("files", []):
        url = f["links"]["self"]
        target = out / f["key"]
        print(f"  downloading {f['key']} ({f.get('size', 0)/1e6:.0f} MB)")
        with _get(url, timeout=600) as src, open(target, "wb") as dst:
            shutil.copyfileobj(src, dst, length=1 << 20)
    (out / ".fetched").write_text(
        f"source=zenodo:{meta['record']}\ndoi={meta['doi']}\ndate={time.strftime('%Y-%m-%d')}\n",
        encoding="utf-8")


def fetch_github(key, meta):
    out = DEST / meta["name"]
    if (out / ".fetched").exists():
        print(f"  {meta['name']}: already present")
        return
    url = f"https://codeload.github.com/{meta['repo']}/zip/refs/heads/{meta['ref']}"
    print(f"  downloading {meta['repo']}@{meta['ref']}")
    buf = io.BytesIO()
    with _get(url, timeout=600) as src:
        shutil.copyfileobj(src, buf, length=1 << 20)
    buf.seek(0)
    tmp = DEST / (meta["name"] + "_tmp")
    with zipfile.ZipFile(buf) as z:
        z.extractall(tmp)
    inner = [p for p in tmp.iterdir() if p.is_dir()]
    if len(inner) == 1:                       # strip the repo-branch prefix
        shutil.move(str(inner[0]), str(out))
        shutil.rmtree(tmp)
    else:
        shutil.move(str(tmp), str(out))
    (out / ".fetched").write_text(
        f"source=github:{meta['repo']}@{meta['ref']}\ndoi={meta['doi']}\n"
        f"date={time.strftime('%Y-%m-%d')}\n", encoding="utf-8")


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=list(ZENODO) + list(GITHUB))
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args(argv)

    if args.list:
        print(f"target directory: {DEST}\n")
        for k, m in list(ZENODO.items()) + list(GITHUB.items()):
            src = f"zenodo:{m['record']}" if k in ZENODO else f"github:{m['repo']}"
            print(f"{k:9s} {m['name']:20s} {src:48s} {m['doi']:28s} {m['used_by']}")
        return 0

    DEST.mkdir(parents=True, exist_ok=True)
    print(f"target: {DEST}\n")
    for k, m in ZENODO.items():
        if args.only and args.only != k:
            continue
        print(f"[{k}] {m['title']}")
        fetch_zenodo(k, m)
    for k, m in GITHUB.items():
        if args.only and args.only != k:
            continue
        print(f"[{k}] {m['note']}")
        fetch_github(k, m)
    print("\ndone; run `python reproduce/run_all.py 09` to use them")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
