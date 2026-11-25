"""End-to-end Gate-2 verification harness for Paper 15.

Author: Lluis Eriksson
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.lp_certifier import verify_lp_certificate_exact  # noqa: E402

MANIFEST_PATH = ROOT / "SHA256SUMS.json"
TRACKED_GLOBS = [
    "lean/StronglyPolyLP.lean",
    "lean/AuditAxioms.lean",
    "lean/lakefile.lean",
    "lean/lean-toolchain",
    "src/__init__.py",
    "src/lp_exact.py",
    "src/lp_certifier.py",
    "scripts/run_all_experiments.py",
    "scripts/make_figures.py",
    "scripts/verify_all.py",
    "tests/test_suite.py",
    "results/*.json",
    "results/certificates/*.cert.json",
    "paper/figures/*.png",
    "paper/main.tex",
    "paper/references.bib",
    "README.md",
    "pyproject.toml",
]


def sha256_file(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def collect_tracked_files() -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for pat in TRACKED_GLOBS:
        files.extend(sorted(ROOT.glob(pat)))
    seen = set()
    uniq = []
    for f in files:
        if f.is_file() and f not in seen:
            seen.add(f)
            uniq.append(f)
    return uniq


def check_lean() -> None:
    lean_dir = ROOT / "lean"
    p1 = subprocess.run(["lake", "build"], cwd=lean_dir, capture_output=True, text=True)
    if p1.returncode != 0 or "warning:" in (p1.stdout + p1.stderr).lower():
        raise RuntimeError(f"Lean build failed or warned:\n{p1.stdout}\n{p1.stderr}")
    p2 = subprocess.run(["lake", "env", "lean", "AuditAxioms.lean"], cwd=lean_dir, capture_output=True, text=True)
    out = p2.stdout + p2.stderr
    if p2.returncode != 0:
        raise RuntimeError(f"AuditAxioms failed:\n{out}")
    for forbidden in ("sorryAx", "Classical.choice", "Lean.ofReduceBool", "Lean.trustCompiler"):
        if forbidden in out:
            raise RuntimeError(f"Forbidden axiom detected: {forbidden}\n{out}")
    count = sum(1 for line in out.splitlines() if line.startswith("'StronglyPolyLP."))
    if count != 18:
        raise RuntimeError(f"Expected 18 Lean theorems in AuditAxioms, found {count}:\n{out}")
    print("[PASS] Lean 4 kernel: 18/18 theorems, 0 warnings, 0 sorry, 0 Classical.choice")


def check_certificates() -> None:
    cfiles = sorted((ROOT / "results" / "certificates").glob("*.cert.json"))
    if len(cfiles) != 16:
        raise RuntimeError(f"Expected 16 certificates, found {len(cfiles)}")
    for cf in cfiles:
        verify_lp_certificate_exact(json.loads(cf.read_text(encoding="utf-8")))
    print(f"[PASS] Exact-Q certificates: {len(cfiles)}/16 independently verified (0 floats)")


def check_pytest() -> None:
    p = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=ROOT, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"pytest failed:\n{p.stdout}\n{p.stderr}")
    print(f"[PASS] pytest: {p.stdout.strip()}")


def check_manifest(write: bool) -> None:
    files = collect_tracked_files()
    current = {f.relative_to(ROOT).as_posix(): sha256_file(f) for f in files}
    if write:
        MANIFEST_PATH.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"[PASS] Wrote SHA256SUMS.json ({len(current)} files)")
        return
    saved = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if saved != current:
        raise RuntimeError("SHA256SUMS.json mismatch!")
    print(f"[PASS] SHA256SUMS.json: {len(current)}/{len(current)} hashes match")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-manifest", action="store_true")
    args = ap.parse_args()
    check_lean()
    check_certificates()
    check_pytest()
    check_manifest(args.write_manifest)
    print("=== ALL PAPER 15 GATE-2 VERIFICATION CHECKS PASSED ===")


if __name__ == "__main__":
    main()
