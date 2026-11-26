#!/usr/bin/env python3
"""Checks the site before it ships: local links resolve, nothing private is named, every public project is listed."""
import json
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRIVATE = ["agent-host", "agent-security-range", "taumatix/dev", "chat-archive", "chat-history"]
PAGES = [p for p in ROOT.rglob("*.html") if "tools" not in p.relative_to(ROOT).parts]
LINK = re.compile(r'(?:href|src)="([^"#?]+)')

errors = []
for page in PAGES:
    text = page.read_text()
    rel = page.relative_to(ROOT)
    for name in PRIVATE:
        if name in text:
            errors.append(f"{rel}: names private repo {name!r}")
    for target in LINK.findall(text):
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        path = ROOT / target.lstrip("/")
        if path.is_dir():
            path = path / "index.html"
        if not path.is_file():
            errors.append(f"{rel}: broken link {target}")
    for tag in ("<title>", 'name="viewport"', 'rel="icon"'):
        if tag not in text:
            errors.append(f"{rel}: missing {tag}")

def public_repos():
    url = "https://api.github.com/orgs/taumatix/repos?per_page=100&type=public"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            return [r["name"] for r in json.load(resp) if not r["archived"] and not r["fork"]]
    except Exception as exc:
        print(f"warning: could not list public repos ({exc}); skipping the landing-page coverage check")
        return []

NOT_PROJECTS = {".github", "taumatix.github.io"}
landing = (ROOT / "index.html").read_text()
for name in public_repos():
    if name not in NOT_PROJECTS and f"github.com/taumatix/{name}" not in landing:
        errors.append(f"index.html: public repo {name!r} is not on the landing page")

cname = (ROOT / "CNAME").read_text().strip()
if cname != "taumatix.dev":
    errors.append(f"CNAME is {cname!r}, want 'taumatix.dev'")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"ok: {len(PAGES)} pages")
