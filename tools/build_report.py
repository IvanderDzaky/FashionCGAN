"""Compile laporan/main.tex and name the PDF after the report title.

Runs pdfLaTeX + BibTeX + pdfLaTeX twice, then copies the result to a
descriptive filename derived from the report title on the cover.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "laporan"
MIKTEX = Path.home() / "AppData/Local/Programs/MiKTeX/miktex/bin/x64"
JOB = "main"


def run(command: list[str]) -> None:
    result = subprocess.run(command, cwd=REPORT, capture_output=True, text=True, errors="replace")
    if result.returncode not in (0, 1):
        print(result.stdout[-3000:])
        sys.exit(f"gagal menjalankan: {' '.join(command)}")


def output_name() -> str:
    source = (REPORT / f"{JOB}.tex").read_text(encoding="utf-8")
    match = re.search(r"\\newcommand\{\\ReportTitle\}\{Laporan (.*?)\}\s*$", source, re.M | re.S)
    title = match.group(1) if match else "Laporan"
    title = title.replace("\\\\", " ").replace(":", " -").replace("\n", " ")
    slug = re.sub(r"[^0-9A-Za-z]+", "-", title).strip("-").lower()
    return f"Laporan-{slug}.pdf"


def main() -> int:
    tools = [str(MIKTEX / "pdflatex"), str(MIKTEX / "bibtex")]
    if not Path(f"{tools[0]}.exe").exists():
        tools = ["pdflatex", "bibtex"]
    pdflatex, bibtex = tools
    run([pdflatex, "-interaction=nonstopmode", f"{JOB}.tex"])
    run([bibtex, JOB])
    run([pdflatex, "-interaction=nonstopmode", f"{JOB}.tex"])
    run([pdflatex, "-interaction=nonstopmode", f"{JOB}.tex"])

    target = REPORT / output_name()
    shutil.copyfile(REPORT / f"{JOB}.pdf", target)
    for pattern in ("*.aux", "*.log", "*.toc", "*.lof", "*.lot", "*.blg"):
        for path in REPORT.glob(pattern):
            path.unlink()
    print(f"PDF: {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
