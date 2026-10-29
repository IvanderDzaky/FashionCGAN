"""Check LaTeX report layout constraints without a TeX installation.

Verifies every table's longest row stays within the text width and every
includegraphics width/height stays within the page text block.
"""

import re
from pathlib import Path

LATEX = Path(__file__).resolve().parents[1] / "laporan"
TEXT_WIDTH_CM = 15.9  # a4paper 21 cm - 4 cm - 3 cm, margin of safety
TEXT_HEIGHT_CM = 23.7  # a4paper 29.7 cm - 3 cm - 3 cm
CM_PER_INCH = 2.54


def wrap_words(text: str, width: float, font_cm: float = 0.42) -> int:
    """Greedy word wrap; returns number of lines at roughly font_cm per glyph."""
    per_line = max(1, int(width // font_cm))
    lines, current = 1, 0
    for word in text.split():
        length = len(word) + (1 if current else 0)
        if current + length > per_line:
            lines += 1
            current = len(word)
        else:
            current += length
    return lines


def check_tables() -> list[str]:
    problems = []
    for path in sorted(LATEX.glob("*.tex")):
        source = path.read_text(encoding="utf-8")
        for match in re.finditer(r"\\begin\{tabular\}\{(.*?)\}\n(.*?)\\end\{tabular\}", source, re.S):
            spec, body = match.group(1), match.group(2)
            spec = spec.replace(" ", "")
            if spec.startswith("|"):
                spec = spec[1:]
            found = re.findall(r"L\{([\d.]+)cm\}|([cm])", spec)
            widths = [float(c[0]) for c in found if c[0]] + [0.0 for c in found if not c[0]]
            if not widths:
                continue
            border = spec.count("|") * 0.02
            total = sum(widths) + 2 * len(widths) * 0.3515 + border  # \tabcolsep = 6pt
            if total > TEXT_WIDTH_CM:
                problems.append(f"{path.name}: lebar tabel {total:.2f} cm > {TEXT_WIDTH_CM} cm")
            for row in re.findall(r"^(?!\s*\\(?:begin|end|caption|label))(.+?)\\\\\s*$", body, re.M):
                row = re.sub(r"\\multicolumn\{(\d+)\}\{[^}]*\}\{([^}]*)\}", lambda m: "&".join([m.group(2)] * int(m.group(1))), row)
                cells = [c.strip() for c in row.split("&")]
                if len(cells) != len(widths):
                    problems.append(f"{path.name}: jumlah sel {len(cells)} != kolom {len(widths)} pada baris: {row[:60]}")
                    continue
                for cell, width in zip(cells, widths):
                    text = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", cell)
                    text = re.sub(r"\\[a-zA-Z]+", "", text)
                    if width and wrap_words(text, width - 0.7) > 6:
                        problems.append(f"{path.name}: sel terlalu panjang untuk {width} cm: {text[:50]}")
    return problems


def check_figures() -> list[str]:
    problems = []
    for path in sorted(LATEX.glob("*.tex")):
        source = path.read_text(encoding="utf-8")
        for match in re.finditer(r"\\includegraphics\[([^\]]*)\]\{([^}]+)\}", source):
            options, name = match.group(1), match.group(2)
            width = re.search(r"width=([\d.]+)\\(?:textwidth|linewidth)", options)
            height = re.search(r"height=([\d.]+)\\textheight", options)
            if width and float(width.group(1)) > 1.0:
                problems.append(f"{path.name}: {name} width {width.group(1)} textwidth > 1")
            if height and float(height.group(1)) > 1.0:
                problems.append(f"{path.name}: {name} height {height.group(1)} textheight > 1")
            image = LATEX / name
            if not image.exists():
                image = LATEX / f"{name}.png"
            if not image.exists():
                problems.append(f"{path.name}: gambar tidak ditemukan: {name}")
                continue
            from PIL import Image

            with Image.open(image) as im:
                w, h = im.size
            scale_match = re.search(r"scale=([\d.]+)", options)
            if scale_match:
                scale = float(scale_match.group(1))
                textwidth_cm = float(width.group(1)) * TEXT_WIDTH_CM if width else None
                # 96 dpi assumption for PNG pixel size
                px_w = float(width.group(1)) * TEXT_WIDTH_CM if width else None
                if px_w is None:
                    continue
    return problems


def main() -> int:
    problems = check_tables() + check_figures()
    for problem in problems:
        print("MASALAH:", problem)
    print("OK: tata letak sesuai batas" if not problems else f"{len(problems)} masalah ditemukan")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
