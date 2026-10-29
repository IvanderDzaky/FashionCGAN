"""Build cleaned OpenCode transcripts for evidence folders.

Usage: python tools/clean_evidence.py
Reads raw OpenCode JSON exports and writes structured Markdown with full prompts
and assistant text responses only (tool calls and metadata are summarized away).
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"


def clean_session(path: Path, title: str, member: str) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    info = data.get("info", {})
    messages = data.get("messages", [])
    turns = []
    tools: list[str] = []
    for message in messages:
        role = message["info"]["role"]
        parts = message.get("parts", [])
        text = "\n\n".join(p["text"] for p in parts if p.get("type") == "text" and p.get("text"))
        for part in parts:
            if part.get("type") == "tool":
                tools.append(part.get("tool", "unknown"))
        if role in ("user", "assistant") and text:
            turns.append({"role": role, "text": text})
    return {
        "title": info.get("title") or title,
        "member": member,
        "model": _model_name(info),
        "created": info.get("time", {}).get("created") if isinstance(info.get("time"), dict) else None,
        "turns": turns,
        "tool_counts": {name: tools.count(name) for name in sorted(set(tools))},
        "messages": len(messages),
    }


def _model_name(info: dict) -> str:
    for key in ("model", "modelID"):
        value = info.get(key)
        if isinstance(value, dict):
            provider, model = value.get("providerID", ""), value.get("id", "")
            return f"{provider}/{model}".strip("/")
        if isinstance(value, str) and value:
            return value
    return "tidak tersedia"


def render(session: dict, source: str) -> str:
    lines = [
        f"# Bukti Sesi OpenCode - {session['member']}",
        "",
        f"- Judul: {session['title']}",
        f"- Platform/Model: OpenCode / {session['model']}",
        f"- Sumber asli: `{source}`",
        f"- Jumlah pesan: {session['messages']}",
        "- Format: transkrip terstruktur dari ekspor JSON OpenCode. Prompt pengguna dikutip penuh; "
        "respons asisten berisi teks saja, pemanggilan tool diringkas pada tabel di akhir.",
        "",
        "## Ringkasan pemakaian tool",
        "",
        "| Tool | Jumlah panggilan |",
        "|---|---|",
    ]
    for name, count in session["tool_counts"].items():
        lines.append(f"| `{name}` | {count} |")
    lines += ["", "## Transkrip", ""]
    number = 0
    pending: list[str] = []

    def flush() -> None:
        nonlocal pending
        if pending:
            lines.extend(["**Respons asisten**", "", "\n\n".join(pending), ""])
            pending = []

    for turn in session["turns"]:
        if turn["role"] == "user":
            flush()
            number += 1
            lines += [f"### Prompt {number}", "", "```text", turn["text"].strip(), "```", ""]
        else:
            pending.append(turn["text"].strip())
    flush()
    return "\n".join(lines).rstrip() + "\n"


SESSIONS = [
    ("ivander-dzaky-khairullah", "session-001-planning.json", "Inisialisasi dan perencanaan proyek"),
    ("ivander-dzaky-khairullah", "session-002-generator-discriminator.json", "Generator dan Discriminator"),
    ("ivander-dzaky-khairullah", "session-004-preprocessing-training.json", "Preprocessing, training, dan generate"),
]


def main() -> None:
    for member, filename, title in SESSIONS:
        source = EVIDENCE / member / filename
        session = clean_session(source, title, member)
        output = source.with_name(source.stem + ".md")
        output.write_text(render(session, f"evidence/{member}/{filename}"), encoding="utf-8")
        print(f"wrote {output.relative_to(ROOT)} ({len(session['turns'])} turns)")


if __name__ == "__main__":
    main()
