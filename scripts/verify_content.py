#!/usr/bin/env python3
"""Validate a Neurosurgery Digest HTML fragment against _build/articles_data.json.

Usage:
    python3 scripts/verify_content.py                 # default paths
    python3 scripts/verify_content.py <html_path>     # custom fragment path

Run BEFORE scripts/add_post.py (see SKILL.md "Pre-deploy validation").
Exit 0 = PASS, exit 1 = FAIL (each issue is printed with a "FAIL ..." line).

Copy this into /root/neurosurgery-digest/scripts/ if not already present.
"""
import json
import re
import sys
from pathlib import Path

PROJECT = Path("/root/neurosurgery-digest")
HTML = PROJECT / "_build/today_content.html"
JSON = PROJECT / "_build/articles_data.json"


def main() -> int:
    html_path = Path(sys.argv[1]) if len(sys.argv) > 1 else HTML
    if not html_path.exists():
        print(f"FAIL: fragment not found: {html_path}")
        return 1

    html = html_path.read_text(encoding="utf-8")
    data = json.loads(JSON.read_text(encoding="utf-8"))
    arts = data["articles"]
    json_dois = {a["doi"] for a in arts}
    json_titles = {a["title"] for a in arts}

    fails: list[str] = []
    SECTIONS = ["YAFTEHAYE KELIDI", "NATIJEH GIRI", "KARBORD BALINI"]

    # 1. Exactly 10 article cards
    cards = re.findall(r'<div class="article-card">', html)
    if len(cards) != 10:
        fails.append(f"card count {len(cards)} != 10")

    # 2. Unique h2 slugs
    slugs = re.findall(r'<h2 id="([^"]+)"', html)
    if len(slugs) != 10:
        fails.append(f"h2 count {len(slugs)} != 10")
    dupes = [s for s in slugs if slugs.count(s) > 1]
    if dupes:
        fails.append(f"duplicate slugs: {sorted(set(dupes))}")

    # 3. en-title verbatim match
    ent = re.findall(r'<div class="article-en-title">(.*?)</div>', html)
    for t in ent:
        if t not in json_titles:
            fails.append(f"en-title not verbatim in JSON: {t[:60]}")

    # 4. DOIs real + exactly 10 distinct
    dois = re.findall(r"https://doi\.org/([^\" ]+)", html)
    for d in dois:
        if d not in json_dois:
            fails.append(f"DOI not in JSON: {d}")
    if len(set(dois)) != 10:
        fails.append(f"distinct DOIs {len(set(dois))} != 10")

    # 5. Each of the 3 sections present exactly 10x and inside every card
    for sec in SECTIONS:
        if html.count(f"<h3>{sec}</h3>") != 10:
            fails.append(f"{sec} count != 10")
    for i, c in enumerate(html.split('<div class="article-card">')[1:], start=1):
        for sec in SECTIONS:
            if sec not in c:
                fails.append(f"card {i} missing {sec}")

    # 6. intro + tip box
    for cls in ("digest-intro", "tip-box"):
        if f'<div class="{cls}">' not in html:
            fails.append(f"missing {cls}")

    # 7. No placeholder junk
    if "article-slug" in html:
        fails.append("placeholder id 'article-slug' present")
    if "نام مجله" in html:
        fails.append("journal placeholder text 'نام مجله' present")
    if ">Link</a>" in html:
        fails.append("English 'Link' anchor present (should be Persian 'لینک')")

    # 8. Balanced div tags
    if html.count("<div") != html.count("</div>"):
        fails.append(
            f"div imbalance: open={html.count('<div')} close={html.count('</div>')}"
        )

    print(
        f"cards:{len(cards)} | distinct slugs:{len(set(slugs))} | "
        f"distinct DOIs:{len(set(dois))} | div balance:{html.count('<div') == html.count('</div>')}"
    )
    if fails:
        print("RESULT: FAIL " + "; ".join(fails))
        return 1
    print("RESULT: PASS all structural checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())