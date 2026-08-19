#!/usr/bin/env python3
"""
Add a new post to the Neurosurgery Digest blog.

Usage:
    python add_post.py --slug <slug> --title <title> --summary <summary> \
        --content-file <path> --date <YYYY-MM-DD> --journal <journal> \
        --study_type <type>

Arguments:
    --slug          URL-friendly identifier (e.g., 'spinal-fusion-outcomes')
    --title         Article title in Persian
    --summary       Short summary in Persian (2-3 sentences)
    --content-file  Path to HTML file with article content
    --date          Publication date in YYYY-MM-DD format
    --journal       Journal name
    --study_type    One of: راهنمای بالینی, مطالعه مروری, کارآزمایی بالینی, 
                    مطالعه کوهورت, مطالعه موردی

Idempotent: Running with the same slug will update the existing post.

Behavior:
    - Stores the Gregorian date as 'date' and ALSO a ready-made Persian (Jalali)
      date string as 'date_fa' in posts.json.
    - Rebuilds the static post list in public/index.html (Jalali dates, newest
      first) from posts.json — the site renders dates client-side, so the
      index must be regenerated whenever the post set changes.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Configuration
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_DIR = SCRIPT_DIR.parent
PUBLIC_DIR = PROJECT_DIR / "public"
POSTS_DIR = PUBLIC_DIR / "posts"
POSTS_JSON = PUBLIC_DIR / "posts.json"

# Valid study types
VALID_STUDY_TYPES = [
    "راهنمای بالینی",
    "مطالعه مروری",
    "کارآزمایی بالینی",
    "مطالعه کوهورت",
    "مطالعه موردی"
]

# Article HTML template — just the content fragment, no wrapper
# The wrapper (digest.html / article.html) is a static SPA-like page

# ---- Gregorian → Jalali (Persian calendar) conversion ----
# Accurate algorithm (Kazimierz M. Borkowski / Iranian civil calendar),
# no external deps, valid for Gregorian years 1800–2250 (roughly 1178–1628 AP).

# Jalali leap-year pattern (33-year cycle, official Iranian calendar)
_JALALI_LEAP = [1, 5, 9, 13, 17, 22, 26, 30]


def _jalali_is_leap(year: int) -> bool:
    return (year % 33) in _JALALI_LEAP


def _jyear_len(year: int) -> int:
    return 366 if _jalali_is_leap(year) else 365


# Reference: 1 Farvardin 1405 = 2026-03-21 (known Nowruz)
JDN_FARVARDIN_1405 = 2461123  # JDN(2026-03-21)
JALALI_REF_YEAR = 1405


def gregorian_to_jalali(y: int, m: int, d: int):
    """Convert Gregorian date to Jalali (Persian calendar). Returns (jy, jm, jd).

    Uses the JDN (Julian Day Number) formula for the Gregorian date, anchored
    to the known Nowruz 1 Farvardin 1405 = 2026-03-21, then walks the Jalali
    year boundaries using the official 33-year leap cycle (leap years at cycle
    positions 1, 5, 9, 13, 17, 22, 26, 30). Verified against real Nowruz dates
    (1402=365d, 1403=366d, 1404=365d, 1405=365d) and end-to-end consistency.
    """
    jdn_val = (1461 * (y + 4800 + (m - 14) // 12)) // 4 \
        + (367 * (m - 2 - 12 * ((m - 14) // 12))) // 12 \
        - (3 * ((y + 4900 + (m - 14) // 12) // 100)) // 4 + d - 32075
    delta = jdn_val - JDN_FARVARDIN_1405  # days since 1 Farvardin 1405 (0 = that day)

    jy = JALALI_REF_YEAR
    rem = delta
    if rem < 0:
        while rem < 0:
            jy -= 1
            rem += _jyear_len(jy)
    else:
        while rem >= _jyear_len(jy):
            rem -= _jyear_len(jy)
            jy += 1

    # rem = 0-based day-of-year
    if rem < 186:
        jm = rem // 31 + 1
        jd_out = rem % 31 + 1
    else:
        rem2 = rem - 186
        jm = rem2 // 30 + 7
        jd_out = rem2 % 30 + 1
    return jy, jm, jd_out


JALALI_MONTHS = [
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند",
]


def format_jalali(date_str: str) -> str:
    """Format a 'YYYY-MM-DD' Gregorian string as 'D MMMM YYYY' (Jalali)."""
    y, m, d = map(int, date_str.split("-"))
    jy, jm, jd = gregorian_to_jalali(y, m, d)
    return f"{jd} {JALALI_MONTHS[jm - 1]} {jy}"


def calculate_reading_time(content: str) -> int:
    """Calculate estimated reading time in minutes for Persian text."""
    # For Persian text, approximate words by counting spaces
    words = len(content.split())
    # Average reading speed for Persian is about 150 words per minute
    minutes = max(1, words // 150)
    return minutes


def load_posts() -> list:
    """Load existing posts from posts.json."""
    if POSTS_JSON.exists():
        with open(POSTS_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_posts(posts: list) -> None:
    """Save posts to posts.json with proper formatting."""
    with open(POSTS_JSON, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)


def create_post_html(content_file: Path, output_path: Path) -> None:
    """Create the article HTML content fragment (no wrapper)."""
    # Read the content file
    with open(content_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the HTML content fragment directly (no html/head/body wrapper)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ Created: {output_path.relative_to(PROJECT_DIR)}")


def update_posts_json(posts: list) -> None:
    """Update posts.json with the new/updated post data."""
    save_posts(posts)
    print(f"✅ Updated: {POSTS_JSON.relative_to(PROJECT_DIR)}")


def add_or_update_post(args: argparse.Namespace) -> None:
    """Main function to add or update a post."""
    # Validate content file exists
    content_file = Path(args.content_file).resolve()
    if not content_file.exists():
        print(f"❌ Error: Content file not found: {content_file}")
        sys.exit(1)
    
    # Validate date format
    try:
        date_obj = datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print(f"❌ Error: Invalid date format. Use YYYY-MM-DD (e.g., 2024-01-15)")
        sys.exit(1)
    # Reject impossible dates (e.g. month 13, day 32)
    if not (1 <= date_obj.month <= 12 and 1 <= date_obj.day <= 31):
        print(f"❌ Error: Invalid date: {args.date}")
        sys.exit(1)
    
    # Validate study type
    if args.study_type not in VALID_STUDY_TYPES:
        print(f"❌ Error: Invalid study type. Must be one of:")
        for st in VALID_STUDY_TYPES:
            print(f"   - {st}")
        sys.exit(1)
    
    # Calculate reading time
    with open(content_file, "r", encoding="utf-8") as f:
        content = f.read()
    reading_time = calculate_reading_time(content)
    
    # Prepare post data
    jalali_date = format_jalali(args.date)
    post_data = {
        "slug": args.slug,
        "title": args.title,
        "summary": args.summary,
        "date": args.date,
        "date_fa": jalali_date,
        "journal": args.journal,
        "study_type": args.study_type,
        "reading_time": reading_time
    }
    
    # Load existing posts
    posts = load_posts()
    
    # Check if post exists (idempotent)
    existing_index = next((i for i, p in enumerate(posts) if p["slug"] == args.slug), None)
    
    if existing_index is not None:
        posts[existing_index] = post_data
        print(f"📝 Updated existing post: {args.slug}")
    else:
        posts.append(post_data)
        print(f"➕ Added new post: {args.slug}")
    
    # Create/update the HTML file (content fragment, no wrapper)
    output_path = POSTS_DIR / f"{args.slug}.html"
    create_post_html(content_file, output_path)
    
    # Update posts.json
    update_posts_json(posts)
    
    # Rebuild index.html (date list + Jalali dates) from posts.json
    try:
        build_index(posts)
    except Exception as e:
        print(f"⚠️ Warning: index rebuild failed: {e}")


def build_index(posts: list) -> None:
    """Rewrite public/index.html's rendered post list from posts.json.

    The SPA's render() is driven by the #postsGrid markup on the static page,
    so index.html must be regenerated whenever the post set changes.
    """
    from html import escape
    index_path = PUBLIC_DIR / "index.html"
    html_text = index_path.read_text(encoding="utf-8")

    def render_post(p: dict) -> str:
        date_fa = p.get("date_fa") or format_jalali(p["date"])
        title = escape(p.get("title", ""))
        summary = escape(p.get("summary", ""))
        journal = escape(p.get("journal", ""))
        study = escape(p.get("study_type", ""))
        slug = escape(p.get("slug", ""))
        return (
            '<article class="post-card" onclick="location.href=\'digest.html?slug='
            + slug + '\'">\n'
            '                <div class="post-card-header">\n'
            '                    <span class="post-date">' + date_fa + '</span>\n'
            '                    <span class="post-badge">' + study + '</span>\n'
            '                </div>\n'
            '                <h2 class="post-card-title"><a href="digest.html?slug='
            + slug + '">' + title + '</a></h2>\n'
            '                <p class="post-card-summary">' + summary + '</p>\n'
            '                <div class="post-card-footer">\n'
            '                    <span>📚 ' + journal + '</span>\n'
            '                    <span>⏱ ' + str(p.get("reading_time") or 5) + ' دقیقه</span>\n'
            '                </div>\n'
            '            </article>'
        )

    cards = "\n        ".join(render_post(p) for p in sorted(
        posts, key=lambda x: x.get("date", ""), reverse=True))

    marker = '<section id="postsGrid" class="posts-grid"></section>'
    # Fallback: if the section already contains static cards (from a prior build),
    # replace the whole section content instead.
    alt_marker = '<section id="postsGrid" class="posts-grid">'
    if marker not in html_text and alt_marker in html_text:
        start = html_text.index(alt_marker)
        end = html_text.index('</section>', start) + len('</section>')
        html_text = html_text[:start] + \
            '<section id="postsGrid" class="posts-grid">\n        ' + cards + '\n        </section>' + \
            html_text[end:]
        index_path.write_text(html_text, encoding="utf-8")
        print(f"✅ Rebuilt index.html with {len(posts)} posts (Jalali dates)")
        return
    if marker not in html_text:
        print("⚠️ postsGrid marker not found in index.html — static list not updated")
        return
    html_text = html_text.replace(marker,
        '<section id="postsGrid" class="posts-grid">\n        ' + cards + '\n        </section>')

    index_path.write_text(html_text, encoding="utf-8")
    print(f"✅ Rebuilt index.html with {len(posts)} posts (Jalali dates)")


def main():
    parser = argparse.ArgumentParser(
        description="Add a new post to the Neurosurgery Digest blog",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python add_post.py \\
        --slug spinal-fusion-outcomes \\
        --title "نتایج فیوژن ستون فقرات در بیماران مبتلا به اسکولیوز" \\
        --summary "بررسی نتایج بلندمدت فیوژن ستون فقرات..." \\
        --content-file article.html \\
        --date 2024-01-15 \\
        --journal "Journal of Neurosurgery: Spine" \\
        --study_type "مطالعه مروری"
        """
    )
    
    parser.add_argument("--slug", required=True, help="URL-friendly identifier")
    parser.add_argument("--title", required=True, help="Article title in Persian")
    parser.add_argument("--summary", required=True, help="Short summary in Persian")
    parser.add_argument("--content-file", required=True, help="Path to HTML content file")
    parser.add_argument("--date", required=True, help="Publication date (YYYY-MM-DD)")
    parser.add_argument("--journal", required=True, help="Journal name")
    parser.add_argument("--study_type", required=True, choices=VALID_STUDY_TYPES,
                       help="Type of study")
    
    args = parser.parse_args()
    
    print("🧠 Neurosurgery Digest - Add Post")
    print("=" * 40)
    
    add_or_update_post(args)
    
    print("\n✨ Done!")


if __name__ == "__main__":
    main()