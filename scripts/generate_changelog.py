#!/usr/bin/env python3
import os
import re
import subprocess
from datetime import datetime
from typing import List, Dict, Tuple

CONV_TYPES = [
    ("feat", "Features"),
    ("fix", "Bug Fixes"),
    ("perf", "Performance"),
    ("refactor", "Refactoring"),
    ("docs", "Documentation"),
    ("test", "Tests"),
    ("build", "Build"),
    ("ci", "CI"),
    ("chore", "Chores"),
]

def run(cmd: List[str]) -> str:
    out = subprocess.check_output(cmd, text=True)
    return out.strip()

def get_tags() -> List[Tuple[str, str]]:
    # returns list of (tag, date) sorted by date asc
    try:
        tags = run(["git", "for-each-ref", "--sort=creatordate", "--format=%(refname:strip=2)|%(creatordate:short)", "refs/tags"]).splitlines()
        out = []
        for t in tags:
            if not t:
                continue
            name, date = t.split("|", 1)
            out.append((name, date))
        return out
    except subprocess.CalledProcessError:
        return []

def commits_between(a: str, b: str) -> List[str]:
    # a..b, exclusive a inclusive b
    rng = f"{a}..{b}" if a else b
    try:
        raw = run(["git", "log", "--no-merges", "--pretty=%H|%ad|%s", "--date=short", rng])
    except subprocess.CalledProcessError:
        return []
    return [line for line in raw.splitlines() if line]


def parse_commits(lines: List[str]) -> Dict[str, List[str]]:
    buckets: Dict[str, List[str]] = {k: [] for k, _ in CONV_TYPES}
    buckets["other"] = []
    for line in lines:
        _, date, subj = line.split("|", 2)
        m = re.match(r"^(\w+)(\(.+\))?(!)?:\s*(.+)", subj)
        if m:
            typ = m.group(1).lower()
            text = m.group(4)
            if typ in buckets:
                buckets[typ].append(f"- {text} ({date})")
            else:
                buckets["other"].append(f"- {subj} ({date})")
        else:
            buckets["other"].append(f"- {subj} ({date})")
    return buckets

def render_section(title: str, date: str, buckets: Dict[str, List[str]]) -> str:
    lines = [f"## {title} - {date}"]
    for key, heading in CONV_TYPES:
        items = buckets.get(key, [])
        if items:
            lines.append(f"### {heading}")
            lines.extend(items)
            lines.append("")
    other = buckets.get("other", [])
    if other:
        lines.append("### Other")
        lines.extend(other)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"

def main():
    tags = get_tags()
    content = ["# Changelog", ""]
    if not tags:
        # entire history as Unreleased
        commits = commits_between("", "HEAD")
        buckets = parse_commits(commits)
        today = datetime.utcnow().strftime("%Y-%m-%d")
        content.append(render_section("Unreleased", today, buckets))
    else:
        # Build sections per tag; latest section includes commits from previous tag (exclusive) to tag (inclusive)
        # Also include Unreleased (prev_tag..HEAD) if HEAD is beyond latest tag
        tag_names = [t[0] for t in tags]
        pairs = []
        prev = None
        for t, date in tags:
            pairs.append((prev, t, date))
            prev = t
        # Unreleased at top if there are commits after latest tag
        head_commits = commits_between(tag_names[-1], "HEAD")
        if head_commits:
            buckets = parse_commits(head_commits)
            today = datetime.utcnow().strftime("%Y-%m-%d")
            content.append(render_section("Unreleased", today, buckets))
        # Tag sections newest first
        for a, b, date in reversed(pairs):
            lines = commits_between(a or "", b)
            if not lines:
                continue
            buckets = parse_commits(lines)
            content.append(render_section(b, date, buckets))

    changelog = "\n".join(content).rstrip() + "\n"
    with open("CHANGELOG.md", "w", encoding="utf-8") as f:
        f.write(changelog)
    print("Wrote CHANGELOG.md")

if __name__ == "__main__":
    main()
