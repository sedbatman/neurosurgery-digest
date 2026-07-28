#!/usr/bin/env python3
"""
Build index.html from posts.json template.

This script reads posts.json and generates a new index.html file.
It uses a template-based approach to maintain the original design
while dynamically inserting post data.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Configuration
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_DIR = SCRIPT_DIR.parent
PUBLIC_DIR = PROJECT_DIR / "public"
POSTS_JSON = PUBLIC_DIR / "posts.json"
INDEX_HTML = PUBLIC_DIR / "index.html"

# HTML Template (the main structure of index.html)
INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>neurosurgery.digest | مروری بر مهم‌ترین مقالات نوروسرجری</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Decorative Background Elements -->
    <div class="bg-decoration">
        <div class="neuron neuron-1"></div>
        <div class="neuron neuron-2"></div>
        <div class="neuron neuron-3"></div>
    </div>

    <!-- Header -->
    <header class="site-header">
        <div class="header-content">
            <div class="logo">
                <span class="logo-icon">🧠</span>
                <div class="logo-text">
                    <h1 class="site-name">neurosurgery.digest</h1>
                    <p class="site-subtitle">مروری بر مهم‌ترین مقالات نوروسرجری</p>
                </div>
            </div>
            <div class="header-decoration">
                <span class="spine-icon">🦴</span>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="main-container">
        <!-- Search and Filter Section -->
        <section class="search-section">
            <div class="search-container">
                <input type="text" id="searchInput" class="search-input" placeholder="جستجو در مقالات...">
                <button id="searchBtn" class="search-btn">🔍</button>
            </div>
            <div class="filter-container">
                <select id="studyTypeFilter" class="filter-select">
                    <option value="">همه انواع مطالعه</option>
                    <option value="راهنمای بالینی">راهنمای بالینی</option>
                    <option value="مطالعه مروری">مطالعه مروری</option>
                    <option value="کارآزمایی بالینی">کارآزمایی بالینی</option>
                    <option value="مطالعه کوهورت">مطالعه کوهورت</option>
                    <option value="مطالعه موردی">مطالعه موردی</option>
                </select>
            </div>
        </section>

        <!-- Posts Grid -->
        <section id="postsGrid" class="posts-grid">
            {posts_html}
        </section>

        <!-- No Results Message -->
        <div id="noResults" class="no-results" style="display: none;">
            <p>مقاله‌ای با این مشخصات یافت نشد.</p>
        </div>
    </main>

    <!-- Footer -->
    <footer class="site-footer">
        <div class="footer-content">
            <p class="copyright">© ۱۴۰۵ neurosurgery.digest | ساخته شده با ❤️ برای علاقه‌مندان به نوروسرجری</p>
            <p class="doctor-credit">دکتر علیرضا | آینده جراح ستون فقرات</p>
        </div>
    </footer>

    <script>
        // Posts data (embedded from posts.json)
        const posts = {posts_json};
        
        // Calculate reading time
        function calculateReadingTime(text) {{
            const wordsPerMinute = 150;
            const words = text.split(/\\s+/).length;
            const minutes = Math.ceil(words / wordsPerMinute);
            return minutes;
        }}

        // Get badge class based on study type
        function getBadgeClass(studyType) {{
            const types = {{
                'راهنمای بالینی': 'badge-guideline',
                'مطالعه مروری': 'badge-review',
                'کارآزمایی بالینی': 'badge-rct',
                'مطالعه کوهورت': 'badge-cohort',
                'مطالعه موردی': 'badge-case'
            }};
            return types[studyType] || 'badge-default';
        }}

        // Format Persian date
        function formatDate(dateStr) {{
            const months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'];
            const date = new Date(dateStr);
            const persianYear = date.getFullYear() + 621;
            const persianMonth = months[date.getMonth()];
            const persianDay = date.getDate();
            return `${{persianDay}} ${{persianMonth}} ${{persianYear}}`;
        }}

        // Search functionality
        function filterPosts() {{
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const studyType = document.getElementById('studyTypeFilter').value;
            
            const filtered = posts.filter(post => {{
                const matchesSearch = post.title.toLowerCase().includes(searchTerm) || 
                                     post.summary.toLowerCase().includes(searchTerm);
                const matchesType = !studyType || post.study_type === studyType;
                return matchesSearch && matchesType;
            }});
            
            renderPosts(filtered);
        }}

        // Render posts
        function renderPosts(postsToRender) {{
            const grid = document.getElementById('postsGrid');
            const noResults = document.getElementById('noResults');
            
            if (postsToRender.length === 0) {{
                grid.innerHTML = '';
                noResults.style.display = 'block';
                return;
            }}
            
            noResults.style.display = 'none';
            
            grid.innerHTML = postsToRender.map(post => `
                <article class="post-card" data-slug="${{post.slug}}">
                    <div class="card-header">
                        <span class="post-date">${{formatDate(post.date)}}</span>
                        <span class="study-badge ${{getBadgeClass(post.study_type)}}">${{post.study_type}}</span>
                    </div>
                    <h2 class="post-title">
                        <a href="post.html?slug=${{post.slug}}">${{post.title}}</a>
                    </h2>
                    <p class="post-summary">${{post.summary}}</p>
                    <div class="card-footer">
                        <span class="journal-name">📚 ${{post.journal}}</span>
                        <span class="reading-time">⏱️ ${{post.reading_time || 5}} دقیقه</span>
                    </div>
                </article>
            `).join('');

            // Add click handlers
            document.querySelectorAll('.post-card').forEach(card => {{
                card.addEventListener('click', () => {{
                    const slug = card.dataset.slug;
                    window.location.href = `post.html?slug=${{slug}}`;
                }});
            }});
        }}

        // Event listeners
        document.getElementById('searchInput').addEventListener('input', filterPosts);
        document.getElementById('studyTypeFilter').addEventListener('change', filterPosts);
        document.getElementById('searchBtn').addEventListener('click', filterPosts);

        // Initialize - render posts from embedded data
        renderPosts(posts);
    </script>
</body>
</html>"""


def format_persian_date(date_str: str) -> str:
    """Format date string to Persian date."""
    try:
        months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 
                  'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        persian_year = date_obj.year + 621
        persian_month = months[date_obj.month - 1]
        persian_day = date_obj.day
        return f"{persian_day} {persian_month} {persian_year}"
    except:
        return date_str


def generate_post_card(post: dict) -> str:
    """Generate HTML for a single post card."""
    badge_classes = {
        'راهنمای بالینی': 'badge-guideline',
        'مطالعه مروری': 'badge-review',
        'کارآزمایی بالینی': 'badge-rct',
        'مطالعه کوهورت': 'badge-cohort',
        'مطالعه موردی': 'badge-case'
    }
    
    badge_class = badge_classes.get(post.get('study_type', ''), 'badge-default')
    date_display = format_persian_date(post.get('date', ''))
    reading_time = post.get('reading_time', 5)
    
    return f"""            <article class="post-card" data-slug="{post['slug']}">
                <div class="card-header">
                    <span class="post-date">{date_display}</span>
                    <span class="study-badge {badge_class}">{post.get('study_type', '')}</span>
                </div>
                <h2 class="post-title">
                    <a href="post.html?slug={post['slug']}">{post['title']}</a>
                </h2>
                <p class="post-summary">{post.get('summary', '')}</p>
                <div class="card-footer">
                    <span class="journal-name">📚 {post.get('journal', '')}</span>
                    <span class="reading-time">⏱️ {reading_time} دقیقه</span>
                </div>
            </article>"""


def build_index():
    """Main function to build index.html."""
    print("🏗️  Building index.html...")
    
    # Load posts
    if not POSTS_JSON.exists():
        print(f"⚠️  {POSTS_JSON} not found, creating empty file")
        POSTS_JSON.write_text("[]", encoding="utf-8")
    
    with open(POSTS_JSON, "r", encoding="utf-8") as f:
        posts = json.load(f)
    
    print(f"📚 Found {len(posts)} posts")
    
    # Sort posts by date (newest first)
    posts.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    # Generate post cards HTML
    posts_html = "\n".join(generate_post_card(post) for post in posts)
    
    # Create JSON string for embedding
    posts_json = json.dumps(posts, ensure_ascii=False, indent=8)
    
    # Generate the index.html
    index_html = INDEX_TEMPLATE.format(
        posts_html=posts_html,
        posts_json=posts_json
    )
    
    # Write the file
    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(index_html)
    
    print(f"✅ Generated: {INDEX_HTML.relative_to(PROJECT_DIR)}")


if __name__ == "__main__":
    build_index()