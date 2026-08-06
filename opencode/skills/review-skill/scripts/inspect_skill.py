#!/usr/bin/env python3
"""Inspect an Agent/Claude/OpenCode skill folder and report structural signals.

This script intentionally uses only the Python standard library so it can run in
most agent environments without setup. It performs mechanical checks only; use
the review rubric for the final qualitative judgment.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


RESOURCE_DIRS = ("references", "reference", "scripts", "assets", "examples")
IGNORED_DIR_NAMES = {"__pycache__", ".git"}
IGNORED_FILE_SUFFIXES = {".pyc", ".pyo", ".skill"}
IGNORED_FILE_NAMES = {".DS_Store"}
UNWANTED_SUPPORT_FILES = {
    "README.md",
    "INSTALLATION_GUIDE.md",
    "QUICK_REFERENCE.md",
    "CHANGELOG.md",
}
# 汎用語（「使用」「確認」「when」など）はほぼ全文書に出現し検査が常に通過してしまうため、
# トリガー・安全ルールを宣言する文に固有の語だけを使う。
TRIGGER_HINTS = (
    "時に使用",
    "で起動する",
    "トリガー",
    "Use when",
    "use when",
    "Use this skill when",
    "use this skill when",
    "Trigger",
    "trigger",
    "際に",
    "使わない",
    "使用しない",
    "Do NOT",
    "do not use",
    "instead of",
    "not for",
    "use /",
    "ではなく",
)
GOTCHA_HINTS = (
    "Gotchas",
    "gotchas",
    "注意点",
    "注意事項",
    "落とし穴",
    "失敗例",
    "失敗しやすい",
    "footgun",
    "アンチパターン",
    "してはいけない",
)
SAFETY_HINTS = (
    "事前確認",
    "事前に確認",
    "ユーザーに確認",
    "ユーザーへ確認",
    "確認後",
    "確認してから",
    "承認",
    "dry-run",
    "dry run",
    "安全",
    "guardrail",
    "AskUserQuestion",
    "permission",
)
# 名詞での言及（「削除フラグ」）や成果物の整理手順（「不要な例ファイルは削除する」）を
# 拾わないよう、対象を取って実行する形に限定する。
DESTRUCTIVE_HINTS = (
    "rm -rf",
    "force-push",
    "force push",
    "push --force",
    "DROP TABLE",
    "kubectl delete",
    "delete_project",
    "delete_issue",
    "を削除する",
    "削除を実行",
    "デプロイする",
    "デプロイを実行",
    "pushする",
    "pushして",
    "git push",
    "push origin",
)
SECRET_PATTERNS = (
    re.compile(r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect a skill directory")
    parser.add_argument("path", help="Path to a skill directory or SKILL.md")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    return parser.parse_args()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_frontmatter(text: str) -> tuple[dict[str, str], str, list[str]]:
    warnings: list[str] = []
    if not text.startswith("---\n"):
        return {}, text, ["missing YAML frontmatter"]

    # 行全体が `---` の行だけを終端とみなす。`----` や `--- xxx` を誤検出しない。
    closing = re.search(r"^---[ \t]*$", text[4:], flags=re.MULTILINE)
    if closing is None:
        return {}, text, ["unterminated YAML frontmatter"]

    raw = text[4 : 4 + closing.start()].strip("\n")
    body = text[4 + closing.end() :]
    if body.startswith("\n"):
        body = body[1:]
    return parse_simple_yaml(raw, warnings), body, warnings


def parse_simple_yaml(raw: str, warnings: list[str]) -> dict[str, str]:
    """Parse the small subset of YAML used by SKILL.md frontmatter."""
    result: dict[str, str] = {}
    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        if ":" not in line:
            warnings.append(f"unparsed frontmatter line: {line}")
            i += 1
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value in {">", ">-", ">+", "|", "|-", "|+"}:
            block: list[str] = []
            i += 1
            while i < len(lines):
                next_line = lines[i]
                if next_line and not next_line.startswith((" ", "\t")):
                    break
                block.append(next_line.strip())
                i += 1
            result[key] = " ".join(part for part in block if part).strip()
            continue

        result[key] = value.strip().strip('"\'')
        i += 1
    return result


def line_count(path: Path) -> int | None:
    try:
        return len(read_text(path).splitlines())
    except UnicodeDecodeError:
        return None


def is_ignored_path(path: Path) -> bool:
    return (
        any(part in IGNORED_DIR_NAMES for part in path.parts)
        or path.name in IGNORED_FILE_NAMES
        or path.suffix in IGNORED_FILE_SUFFIXES
    )


def list_files(skill_dir: Path) -> list[dict[str, Any]]:
    files: list[dict[str, Any]] = []
    for path in sorted(p for p in skill_dir.rglob("*") if p.is_file() and not is_ignored_path(p.relative_to(skill_dir))):
        rel = path.relative_to(skill_dir).as_posix()
        files.append({"path": rel, "lines": line_count(path), "bytes": path.stat().st_size})
    return files


def strip_fenced_code_blocks(text: str) -> str:
    """Drop fenced code blocks so example links inside them are not checked."""
    lines: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        match = re.match(r"^([`~]{3,})", line.lstrip())
        if fence is None:
            if match:
                fence = match.group(1)
                continue
            lines.append(line)
        elif match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence):
            fence = None
    return "\n".join(lines)


def extract_relative_links(skill_dir: Path, text: str) -> list[dict[str, Any]]:
    links: list[dict[str, Any]] = []
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", strip_fenced_code_blocks(text)):
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
            continue
        clean_target = target.split("#", 1)[0].strip()
        if not clean_target:
            continue
        links.append({"target": target, "exists": (skill_dir / clean_target).exists()})
    return links


def add_finding(findings: list[dict[str, str]], severity: str, code: str, message: str) -> None:
    findings.append({"severity": severity, "code": code, "message": message})


def inspect(path_arg: str) -> dict[str, Any]:
    input_path = Path(path_arg).expanduser().resolve()
    skill_md = input_path if input_path.name == "SKILL.md" else input_path / "SKILL.md"
    skill_dir = skill_md.parent

    report: dict[str, Any] = {
        "input": path_arg,
        "skill_dir": str(skill_dir),
        "skill_md": str(skill_md),
        "exists": skill_md.exists(),
        "frontmatter": {},
        "metrics": {},
        "resources": {},
        "links": [],
        "files": [],
        "findings": [],
    }
    findings: list[dict[str, str]] = report["findings"]

    if not skill_md.exists():
        add_finding(findings, "Critical", "missing-skill-md", "SKILL.md が見つかりません。")
        return report

    text = read_text(skill_md)
    frontmatter, body, warnings = split_frontmatter(text)
    report["frontmatter"] = frontmatter
    report["metrics"] = {
        "skill_md_lines": len(text.splitlines()),
        "body_lines": len(body.splitlines()),
        "description_chars": len(frontmatter.get("description", "")),
    }
    report["files"] = list_files(skill_dir)
    report["links"] = extract_relative_links(skill_dir, text)

    for name in RESOURCE_DIRS:
        resource_path = skill_dir / name
        if resource_path.exists():
            report["resources"][name] = {
                "exists": True,
                "file_count": sum(
                    1
                    for p in resource_path.rglob("*")
                    if p.is_file() and not is_ignored_path(p.relative_to(skill_dir))
                ),
            }
        else:
            report["resources"][name] = {"exists": False, "file_count": 0}

    for warning in warnings:
        add_finding(findings, "High", "frontmatter-parse", warning)

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if not name:
        add_finding(findings, "Critical", "missing-name", "frontmatter に name がありません。")
    elif name != skill_dir.name:
        add_finding(
            findings,
            "Critical",
            "name-directory-mismatch",
            f"name `{name}` とディレクトリ名 `{skill_dir.name}` が一致しません。",
        )

    if not description:
        add_finding(findings, "Critical", "missing-description", "frontmatter に description がありません。")
    else:
        if len(description) < 80:
            add_finding(findings, "Low", "description-too-short", "description が短めです。短いこと自体は問題ありませんが、トリガー条件・成果物・使わないケースが含まれているか確認してください。")
        if not any(hint in description for hint in TRIGGER_HINTS):
            add_finding(findings, "High", "description-no-trigger", "description にモデル向けの起動条件が見当たりません。")
        if len(description) > 700:
            add_finding(findings, "Low", "description-long", "description が長めです。トリガー判断に必要な語へ圧縮できるか確認してください。")

    if report["metrics"]["body_lines"] > 500:
        add_finding(findings, "Medium", "body-too-long", "SKILL.md本文が500行を超えています。詳細をreferencesへ分離してください。")

    if not any(hint in text for hint in GOTCHA_HINTS):
        add_finding(findings, "Low", "no-gotchas", "Gotchas/注意/失敗例の節が見当たりません。実運用での失敗回避知識を追加できるか確認してください。")

    existing_resource_dirs = [name for name in RESOURCE_DIRS if report["resources"][name]["exists"]]
    if not existing_resource_dirs:
        add_finding(findings, "Low", "no-bundled-resources", "references/scripts/assets がありません。純粋な手順Skillとして十分か確認してください。")

    for resource_name in existing_resource_dirs:
        if report["resources"][resource_name]["file_count"] == 0:
            add_finding(findings, "Medium", "empty-resource-dir", f"{resource_name}/ が空です。不要なら削除してください。")

    linked_targets = {link["target"].split("#", 1)[0] for link in report["links"]}
    for resource_name in RESOURCE_DIRS:
        if report["resources"][resource_name]["exists"] and resource_name not in " ".join(linked_targets) and resource_name not in text:
            add_finding(findings, "Low", "resource-not-discoverable", f"{resource_name}/ の参照条件がSKILL.mdから発見しづらい可能性があります。")

    for link in report["links"]:
        if not link["exists"]:
            add_finding(findings, "Medium", "broken-relative-link", f"相対リンク `{link['target']}` の参照先が見つかりません。")

    top_level_files = {p.name for p in skill_dir.iterdir() if p.is_file()}
    for unwanted in sorted(UNWANTED_SUPPORT_FILES & top_level_files):
        add_finding(findings, "Low", "unneeded-support-file", f"{unwanted} はSkill本体に必須でなければ削除または統合してください。")

    # 回答例として書かれる引用ブロック（`> DROP TABLE ...` など）は実行指示ではないため除外する。
    prose = "\n".join(
        line for line in strip_fenced_code_blocks(text).splitlines() if not line.lstrip().startswith(">")
    )
    if any(hint in prose for hint in DESTRUCTIVE_HINTS) and not any(hint in text for hint in SAFETY_HINTS):
        add_finding(findings, "High", "destructive-without-safety", "破壊的/外部反映系の操作語がありますが、確認・dry-run・安全ルールが弱い可能性があります。")

    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            add_finding(findings, "Critical", "possible-secret", "APIキー、トークン、パスワードらしき値が本文に含まれている可能性があります。")

    return report


def format_markdown(report: dict[str, Any]) -> str:
    fm = report["frontmatter"]
    metrics = report["metrics"]
    lines = [
        "# Skill inspection",
        "",
        f"- Path: `{report['skill_dir']}`",
        f"- SKILL.md exists: `{report['exists']}`",
        f"- name: `{fm.get('name', '')}`",
        f"- description chars: `{metrics.get('description_chars', 0)}`",
        f"- SKILL.md lines: `{metrics.get('skill_md_lines', 0)}`",
        "",
        "## Resources",
    ]
    for name, value in report["resources"].items():
        lines.append(f"- {name}/: exists={value['exists']}, files={value['file_count']}")

    lines.extend(["", "## Findings"])
    if report["findings"]:
        for finding in report["findings"]:
            lines.append(f"- [{finding['severity']}] {finding['code']}: {finding['message']}")
    else:
        lines.append("- No mechanical findings.")

    lines.extend(["", "## Relative links"])
    if report["links"]:
        for link in report["links"]:
            lines.append(f"- `{link['target']}`: exists={link['exists']}")
    else:
        lines.append("- No relative markdown links found.")

    lines.extend(["", "## Files"])
    for file_info in report["files"]:
        lines.append(f"- `{file_info['path']}` ({file_info['lines']} lines, {file_info['bytes']} bytes)")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    report = inspect(args.path)
    if args.format == "markdown":
        print(format_markdown(report))
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["exists"] else 2


if __name__ == "__main__":
    sys.exit(main())
