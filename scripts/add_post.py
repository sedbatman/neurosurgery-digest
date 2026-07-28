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

# Article HTML template
ARTICLE_TEMPLATE = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | neurosurgery.digest</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    {content}
</body>
</html>
"""


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


def create_post_html(content_file: Path, output_path: Path, title: str) -> None:
    """Create the article HTML file."""
    # Read the content file
    with open(content_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Generate the full HTML
    html = ARTICLE_TEMPLATE.format(title=title, content=content)
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the HTML file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
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
    post_data = {
        "slug": args.slug,
        "title": args.title,
        "summary": args.summary,
        "date": args.date,
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
    
    # Create/update the HTML file
    output_path = POSTS_DIR / f"{args.slug}.html"
    create_post_html(content_file, output_path, args.title)
    
    # Update posts.json
    update_posts_json(posts)
    
    # Run build_index to regenerate index.html
    print("\n🔄 Regenerating index.html...")
    import subprocess
    build_index_script = SCRIPT_DIR / "build_index.py"
    if build_index_script.exists():
        subprocess.run([sys.executable, str(build_index_script)], check=True)
    else:
        print("⚠️  build_index.py not found, skipping index regeneration")


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