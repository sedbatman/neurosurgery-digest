NEUROSURGERY DIGEST — Final State

Pages (static SPA):
  /index.html       → لیست دایجست‌ها (کارت‌های مقاله) با جستجو و فیلتر
  /digest.html?slug=xxx → نمایش کامل یک دایجست با سایدبار سمت چپ:
                          - TOC (فهرست مطالب)
                          - لینک به مقالات جداگانه
  /article.html?digest=xxx&article=yyy → نمایش یک مقاله به صورت جداگانه
  /posts/2026-07-28.html → content fragment (توسط digest.html و article.html fetch می‌شه)

Layout:
  - صفحه اصلی: grid of article cards (responsive 3-2-1 cols)
  - صفحه دایجست: page-layout = page-content (flex:1) + page-sidebar (280px, sticky)
  - صفحه مقاله: article-page (max-width 800px, centered)

Data flow:
  SPA pages → fetch('posts.json') + fetch('posts/{slug}.html') → client-side render
  No server-side build_index.py needed anymore.
  add_post.py writes only content fragment + updates posts.json.

Files:
  public/style.css          ~13KB
  public/index.html         ~5.6KB
  public/digest.html        ~7KB
  public/article.html       ~5.3KB
  public/posts.json         auto
  public/posts/*.html       auto (fragments, not full HTML docs)
  scripts/add_post.py       simplified (no wrapper, no build_index call)
  scripts/fetch_digest_articles.py  10 query categories covering all NSGY subspecialties